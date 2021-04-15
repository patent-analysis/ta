import boto3
import json
import urllib
import os
import logging
import textract
import re
import requests
import json
import fitz
from patent import Patent
from seqlisting import SeqListing
from collections import Counter

LOCAL_STACK_URL = 'http://host.docker.internal:4566' # mac specific setting, windows should use localhost
DOC_NUMBER_REGEX = '((US|us)\s?([,|\/|\s|\d|&])+\s?([a-zA-Z]\d))'
PATENT_BASE_URL = 'https://uspto-documents-storage.s3.amazonaws.com/docs/'
LISTINGS_BASE_URL = 'https://uspto-documents-storage.s3.amazonaws.com/seq/'
FULL_PDF_PATH = 'full_pdf_temp.pdf'
TMP_IMAGE_PATH = 'img_temp.png'

doc_num_matcher = re.compile(DOC_NUMBER_REGEX)
logger = logging.getLogger()
logger.setLevel(logging.INFO)


#  local env
if os.getenv('LocalEnv'):
    s3_client = boto3.client(service_name='s3', endpoint_url=LOCAL_STACK_URL)
else:
    s3_client = boto3.client('s3')


def fetch_seq_listing(patent_id):
    listing_path = patent_id + '.xml'
    logger.info("requesting " + LISTINGS_BASE_URL + listing_path)
    response = requests.get(LISTINGS_BASE_URL + listing_path)
    logger.info("remote request status: " + str(response.status_code))

    if response.status_code == 200:
        with open(listing_path, 'wb') as f:
            f.write(response.content)
        return SeqListing(patent_id)
    else:
        return None


def fetch_patent_data(patent_id):
    patent_path = patent_id + '.xml'
    logger.info("requesting " + PATENT_BASE_URL + patent_path)
    response = requests.get(PATENT_BASE_URL + patent_path)
    logger.info("remote request status: " + str(response.status_code))

    if response.status_code == 200:
        with open(patent_path, 'wb') as f:
            f.write(response.content)
        return Patent(patent_id)
    else:
        return None    


def extract_patent_id():
    doc = fitz.open(FULL_PDF_PATH)
    page = doc.loadPage(0)
    pix = page.getPixmap(matrix=fitz.Matrix(5, 5))
    pix.writePNG(TMP_IMAGE_PATH)
    parsed_text = textract.process(TMP_IMAGE_PATH, method='tesseract').decode('utf-8')

    # extract patent id
    raw_pat_id = re.search(DOC_NUMBER_REGEX, parsed_text).group(0)
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

    # extract and return patent metadata and sequence listing
    patent = fetch_patent_data(patent_id)
    seq_listing = fetch_seq_listing(patent_id)
    return patent, seq_listing


def persist_patent_record_to_db(patent, seq_listing):
    dynamodb = boto3.resource('dynamodb')

    patents_table = dynamodb.Table('patents-dev')
    biomolecules_table = dynamodb.Table('bioMolecules-dev')

    # Extract patent data from the response and persist to patents_table
    patents_table.put_item(
        Item={
            'patentNumber': patent.patentNumber,
            'patentName': patent.patentName,
            'proteinId': '',
            'claimedResidues': patent.claimedResidues,
            'applicants': ' '.join(patent.applicants),
            'patentAssignees': ' '.join(patent.patentAssignees),
            'inventors': ' '.join(patent.inventors),
            'examiners': patent.examiners,
            'legalStatus': '',
            'appNumber': patent.appNumber,
            'appDate': patent.appDate,
            'claimsCount': patent.claimsCount,
            'sequenceCount': '',
            'patentFileDate': '',
            'createdDate': '',
            'patentDocPath': ''
        }
    )

    # Extract biomolecule data from the response and persist to biomolecules_table
    #  ADD ADDITIONAL KEYS AS NEEDED
    biomolecules_table.put_item(
        Item={
            'name': seq_listing.patentNumber,
            'sequence':  seq_listing.sequences
        }
    )


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
        patent, seq_listing = parse_doc_text(bucket, object_key)
        logger.info("Done handling event")
        result = 'Success'

        if patent and seq_listing:
            logger.info("Patent Name: " + patent.patentName)
            logger.info("SeqListing count: " + seq_listing.seqCount)
            persist_patent_record_to_db(patent, seq_listing)
            return result
        else:
            result = ''

        if patent == None:
            logger.error('unable to fetch patent data')
            result += 'Patent Failure'
        if seq_listing == None:
            logger.error('unable to fetch seq_listing data')
            result += ' SeqListing Failure'
        return result.lstrip()

    except Exception as e:
        logger.error("Error processing key {} Event {} Error: {}".format(
            object_key, json.dumps(event, indent=2),  e))
        raise e
