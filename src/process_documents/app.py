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
import datetime
from classes.patent import Patent
from classes.seqlisting import SeqListing
from collections import Counter

LOCAL_STACK_URL = 'http://host.docker.internal:4566' # mac specific setting, windows should use localhost
DOC_NUMBER_REGEX = "((US|us)\\s?([,|\\/|\\s|\\d|&])+\\s?([a-zA-Z]\\d))"
PATENT_BASE_URL = 'https://uspto-documents-storage.s3.amazonaws.com/docs/'
LISTINGS_BASE_URL = 'https://uspto-documents-storage.s3.amazonaws.com/seq/'
TMP_DIR_PATH = '/tmp/'


logger = logging.getLogger()
logger.setLevel(logging.INFO)


if os.getenv('LocalEnv') == 'true':
    """ Use the localstack instead of aws services when running locally """
    s3_client = boto3.client(service_name='s3', endpoint_url=LOCAL_STACK_URL, region_name='us-east-1')
    dynamodb = boto3.resource(service_name='dynamodb', endpoint_url=LOCAL_STACK_URL, region_name='us-east-1')
else:
    s3_client = boto3.client('s3', region_name='us-east-1')
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')


def extract_seq_info(patent_id):
    listing_path = patent_id + '.xml'
    logger.info("requesting " + LISTINGS_BASE_URL + listing_path)
    response = requests.get(LISTINGS_BASE_URL + listing_path)
    logger.info("response status code: " + str(response.status_code))
    full_document_path =  TMP_DIR_PATH + 'seq_' + listing_path

    if response.status_code == 200:
        with open(full_document_path, 'wb') as f:
            f.write(response.content)
            return SeqListing(full_document_path, patent_id)
    else:
        return None


def extract_document_info(patent_id):
    patent_path = patent_id + '.xml'
    logger.info("requesting " + PATENT_BASE_URL + patent_path)
    response = requests.get(PATENT_BASE_URL + patent_path)
    logger.info("response status code: " + str(response.status_code))

    full_document_path = TMP_DIR_PATH + patent_path
    if response.status_code == 200:
        with open(full_document_path, 'wb') as f:
            f.write(response.content)
        return Patent(full_document_path, patent_id)
    else:
        return None    


def extract_document_id(key):
    full_pdf_file_path = TMP_DIR_PATH + key
    full_image_path = TMP_DIR_PATH + key.replace('pdf', 'png')
    doc = fitz.open(full_pdf_file_path)
    page = doc.loadPage(0)
    logger.info('Loaded the first document page')
    pix = page.getPixmap(matrix=fitz.Matrix(5, 5))
    pix.writePNG(full_image_path)
    logger.info('Parsing the first document page text ...')
    parsed_text = textract.process(full_image_path, method='tesseract').decode('utf-8')
    logger.info('First page parsed Text: {}'.format(parsed_text).replace('\n', '\\n')) # flatten the text for logging
    # extract the patent id
    raw_pat_id = re.search(DOC_NUMBER_REGEX, parsed_text)
    raw_pat_id = raw_pat_id.group()
    doc_number = re.sub('[us|US|,|&|\\s|/]', '',raw_pat_id).strip('0')
    return 'US' + doc_number


def process_document(bucket, key, protein_name):
    logger.info("Downloading and processing document {}".format(key))
    # grab the pdf object from s3 bucket
    s3_object = s3_client.get_object(Bucket=bucket, Key=protein_name + '/' + key)
    pdf_object = s3_object['Body'].read()
    full_pdf_file_path = TMP_DIR_PATH + key
    with open(full_pdf_file_path, 'wb') as f:
        f.write(pdf_object)
    logger.info("Downloaded s3 object {} to file {}".format(key, full_pdf_file_path))

    # extract patent id from first page
    document_id = extract_document_id(key)
    logger.info('Extracted Document ID {} from pdf file'.format(document_id))

    # extract and return patent metadata and sequence listing
    patent = extract_document_info(document_id)
    seq_listing = extract_seq_info(document_id)
    return patent, seq_listing

def get_sequences_list(patent, seq_listing):
    sequences_list = []
    for mentioned_residue in patent.mentionedResidues:
        seq = mentioned_residue['seqId']
        seq_value = seq_listing.sequences[int(seq) - 1]
        seq_obj = {}
        seq_obj['seqIdNo'] = seq
        seq_obj['value'] = seq_value
        sequences_list.append(seq_obj)
    return sequences_list

def persist_doc_records(patent, seq_listing, protein_name):
    # TODO: FIX THE TABLE NAMES
    patents_table = dynamodb.Table('patents-dev')
    biomolecules_table = dynamodb.Table('bioMolecules-dev')
    # Extract patent data from the response and persist to patents_table
    # TODO: Add the claimed seq id nos and the actual sequences to this object
    # TODO: fix the text font!
    # logger.info('The patent object is {}'.format(json.dumps(patent)))
    # logger.info('The seq_listing object is {}'.format(json.dumps(seq_listing)))
    # logger.info('The patent sequences to save to the db are {}'.format(json.dumps(get_sequences_list(patent, seq_listing))))
    # logger.info('The patent sequences to save to the db are {}'.format(json.dumps(get_sequences_list(patent, seq_listing))))
    # logger.info('The patent mentionedResidues to save to the db are {}'.format(json.dumps(patent.mentionedResidues)))

    patents_table.put_item(
        Item={
            'patentNumber': patent.patentNumber,
            'docId': patent.patentNumber,
            'patentName': patent.patentName,
            'proteinId': protein_name,
            'mentionedResidues': patent.mentionedResidues,
            'sequences': get_sequences_list(patent, seq_listing),
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
            'createdDate': datetime.datetime.now().isoformat(),
            'patentDocPath': ''
        }
    )

    # TODO: Use this table to save the protein names!!!
    # Hmm, no need to store the seq data separetly...
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
    Process the pdf documents.
    '''
    logger.debug("Handling event: {}".format(json.dumps(event, indent=2)))
    bucket = event['Records'][0]['s3']['bucket']['name']
    object_key = urllib.parse.unquote_plus(
        event['Records'][0]['s3']['object']['key'])

    try:
        protein_name = object_key.split('/')[0]
        key = object_key.split('/')[1]
        patent, seq_listing = process_document(bucket, key, protein_name)
        logger.info("Completed processing the pdf document..")
        result = 'Success'
        if patent and seq_listing:
            logger.info("Patent Name: " + patent.patentName)
            logger.info("SeqListing count: " + str(seq_listing.seqCount))
            persist_doc_records(patent, seq_listing, protein_name)
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
            object_key, json.dumps(event, indent=None),  e))
        raise e
