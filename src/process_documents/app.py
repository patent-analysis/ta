import boto3
import json
import urllib
import os
import logging
LOCAL_STACK_URL = 'http://192.168.0.1:4566'
logger = logging.getLogger()
logger.setLevel(logging.INFO)


#  local env
if os.getenv('LocalEnv'):
    s3_client = boto3.client(service_name='s3', endpoint_url=LOCAL_STACK_URL)
else:
    s3_client = boto3.client('s3')


def parse_doc_text(bucket, key):
    logger.info("Downloading and processing document {}".format(key))
    # s3_object =
    s3_client.get_object(Bucket=bucket, Key=key)
    # TODO: IMPLEMENT THE TEXT MINING STEPS HERE
    logger.info("Downloaded s3 object {}".format(key))
    return ["text1", "text2"]


def persist_patent_record_to_db(response):
    dynamodb = boto3.resource('dynamodb')

    patents_table = dynamodb.Table('patents-dev')
    biomolecules_table = dynamodb.Table('bioMolecules-dev')

    # Extract patent data from the response and persist to patents_table
    # TODO: REPLACE 'dummy' VALUES BELOW WITH THE CORRECT LOGIC TO EXTRACT THE VALUES FROM response
    patents_table.put_item(
        Item={
            'patentNumber': 'dummy',
            'patentName': 'dummy',
            'proteinId': 'dummy',
            'claimedResidues': 'dummy',
            'applicants': 'dummy',
            'patentAssignees': 'dummy',
            'inventors': 'dummy',
            'examiners': 'dummy',
            'legalStatus': 'dummy',
            'appNumber': 'dummy',
            'appDate': 'dummy',
            'claimsCount': 'dummy',
            'sequenceCount': 'dummy',
            'patentFileDate': 'dummy',
            'createdDate': 'dummy',
            'patentDocPath': 'dummy'
        }
    )

    # Extract biomolecule data from the response and persist to biomolecules_table
    # TODO: REPLACE 'dummy' VALUES BELOW WITH THE CORRECT LOGIC TO EXTRACT THE VALUES FROM response AND
    #  ADD ADDITIONAL KEYS AS NEEDED
    biomolecules_table.put_item(
        Item={
            'name': 'dummy',
            'sequence': 'dummy'
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
        response = parse_doc_text(bucket, object_key)
        logger.info("Done handling event")
        logger.debug(response)

        persist_patent_record_to_db(response)

        return 'Success'

    except Exception as e:
        logger.error("Error processing key {} Event {} Error: {}".format(
            object_key, json.dumps(event, indent=2),  e))
        raise e
