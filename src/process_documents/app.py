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
from collections import Counter

LOCAL_STACK_URL = 'http://host.docker.internal:4566' # mac specific setting, windows look elsewhere
DOC_NUMBER_REGEX = '((US|us)\s?([,|\/|\s|\d|&])+\s?([a-zA-Z]\d))'
PAT_ID_PATTERN = "US\s?\d*[A-B][0-9]"
BASE_URL = 'https://uspto-documents-storage.s3.amazonaws.com/docs/'
FULL_PDF_PATH = 'full_pdf_temp.pdf'
FIRST_PAGE_PATH = 'page_one_pdf_temp.pdf'

doc_num_matcher = re.compile(DOC_NUMBER_REGEX)
logger = logging.getLogger()
logger.setLevel(logging.INFO)


#  local env
if os.getenv('LocalEnv'):
    s3_client = boto3.client(service_name='s3', endpoint_url=LOCAL_STACK_URL)
else:
    s3_client = boto3.client('s3')


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


def extract_first_page():
    reader = PyPDF2.PdfFileReader(FULL_PDF_PATH)
    # extract first page and save
    page = reader.getPage(0)
    page_writer = PyPDF2.PdfFileWriter()
    page_writer.addPage(page)
    with open(FIRST_PAGE_PATH, "wb") as writer_stream:
        page_writer.write(writer_stream)


def extract_patent_id():
    parsed_text = textract.process(FULL_PDF_PATH).decode('utf-8')
    if parsed_text.startswith('\x0c\x0c\x0c'):
        extract_first_page()
        parsed_text = textract.process(FIRST_PAGE_PATH, method='tesseract').decode('utf-8')

    pat_num_matches = doc_num_matcher.findall(parsed_text)
    pat_num_count = Counter(pat_num_matches)
    raw_pat_id = pat_num_count.most_common(1)[0]

    while (isinstance(raw_pat_id, tuple)):
        raw_pat_id = raw_pat_id[0]

    # extract patent id
    patent_id = re.sub('[,|&|\s|/]', '',raw_pat_id).strip('0')
    return patent_id


def parse_doc_text(bucket, key):
    logger.info("Downloading and processing document {}".format(key))
    # grab pdf object from s3 bucket
    s3_object = s3_client.get_object(Bucket=bucket, Key=key)
    pdf_object = s3_object['Body'].read()
    with open(FULL_PDF_PATH, 'wb') as f:
        f.write(pdf_object)
    logger.info("Downloaded s3 object {}".format(key))

    # extract patent id from first page
    patent_id = extract_patent_id()
    
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
            for field in response.__dict__:
                if field != 'description':
                    logger.info(field + ':' + str(response.__dict__[field]))
            return 'Success'

    except Exception as e:
        logger.error("Error processing key {} Event {} Error: {}".format(
            object_key, json.dumps(event, indent=2),  e))
        raise e
