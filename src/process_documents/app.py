import boto3
import json
import urllib
import os
import logging
import textract
import PyPDF2
import re
import io
LOCAL_STACK_URL = 'http://host.docker.internal:4566' # mac specific setting, windows look elsewhere
DOC_NUMBER_REGEX = '((US|us)\s?([,|\/|\s|\d|&])+\s?([a-zA-Z]\d))'
logger = logging.getLogger()
logger.setLevel(logging.INFO)

#  local env
if os.getenv('LocalEnv'):
    s3_client = boto3.client(service_name='s3', endpoint_url=LOCAL_STACK_URL)
else:
    s3_client = boto3.client('s3')

# TODO: add client for patents S3 bucket
s3_patent_client = None #boto3.client('')

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
    raw_patent_id = re.sub('[us|US|,|&|\s|/]', '',raw_patent_id).strip('0')
    patent_id = re.sub('\w\d$', '', raw_patent_id)
    return patent_id


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
    
    #s3_patent_object = s3_patent_client.get_object(Bucket=bucket, Key=patent_id)
    return ''#s3_patent_object['Body'].read()


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
        logger.debug(response)
        return 'Success'

    except Exception as e:
        logger.error("Error processing key {} Event {} Error: {}".format(
            object_key, json.dumps(event, indent=2),  e))
        raise e
