import boto3
import json
import urllib
import os
import logging
import textract
import PyPDF2
import re
import io
import requests
import json
from patent import Patent

LOCAL_STACK_URL = 'http://host.docker.internal:4566' # mac specific setting, windows look elsewhere
DOC_NUMBER_REGEX = '((US|us)\s?([,|\/|\s|\d|&])+\s?([a-zA-Z]\d))'
BASE_URL = 'https://uspto-documents-storage.s3.amazonaws.com/docs/'
logger = logging.getLogger()
logger.setLevel(logging.INFO)

#  local env
if os.getenv('LocalEnv'):
    s3_client = boto3.client(service_name='s3', endpoint_url=LOCAL_STACK_URL)
else:
    s3_client = boto3.client('s3')


def extract_first_page(pdf_object, pdf_file_path):
    # convert byte array to stream object for pdf
    with io.BytesIO(pdf_object) as pdf:
        reader = PyPDF2.PdfFileReader(pdf)
        # extract first page and save
        page = reader.getPage(0)
        page_writer = PyPDF2.PdfFileWriter()
        page_writer.addPage(page)
        with open(pdf_file_path, "wb") as writer_stream:
            page_writer.write(writer_stream)


def extract_patent_id(pdf_file_path):
    # extract patent id
    scanned_text = textract.process(pdf_file_path, method='tesseract').decode('utf-8')
    raw_patent_id = re.search(DOC_NUMBER_REGEX, scanned_text).group(1)
    patent_id = re.sub('[,|&|\s|/]', '',raw_patent_id).strip('0')
    return patent_id


def fetch_patent_data(patent_id):
    patent_path = patent_id + '.xml'
    logger.info("requesting " + BASE_URL + patent_path)
    response = requests.get(BASE_URL + patent_path)
    logger.info("remote request status: " + str(response.status_code))
    if response.status_code == 200:
        with open(patent_path, 'wb') as f:
            f.write(response.content)
        return Patent(patent_id)
    else:
        return None    


def parse_doc_text(bucket, key):
    logger.info("Downloading and processing document {}".format(key))
    # grab pdf object from s3 bucket
    s3_object = s3_client.get_object(Bucket=bucket, Key=key)
    pdf_object = s3_object['Body'].read()
    logger.info("Downloaded s3 object {}".format(key))

    # Write the first page to the tmp dir (to save time)
    extract_first_page(pdf_object, key)

    # extract patent id from first page
    patent_id = extract_patent_id(key)
    
    return fetch_patent_data(patent_id)


def lambda_handler(event, context):
    '''
    Handles newly uploaded pattent pdf docs.
    '''
    print(s3_client)
    logger.debug("Handling event: {}".format(json.dumps(event, indent=2)))
    bucket = event['Records'][0]['s3']['bucket']['name']
    object_key = urllib.parse.unquote_plus(
        event['Records'][0]['s3']['object']['key'])

    try:
        response = parse_doc_text(bucket, object_key)
        logger.info("Done handling event")
        if response == None:
            logger.error('unable to fetch patent data')
            return 'Failure'
        else:
            logger.info(json.dumps(response.__dict__))
            return 'Success'

    except Exception as e:
        logger.error("Error processing key {} Event {} Error: {}".format(
            object_key, json.dumps(event, indent=2),  e))
        raise e
