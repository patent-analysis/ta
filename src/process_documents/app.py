import boto3
import json
import urllib
import os
import logging
LOCAL_STACK_URL='http://192.168.0.1:4566'
logger = logging.getLogger()
logger.setLevel(logging.INFO)


#  local env 
if os.getenv('LOCAL_ENV'):
    s3_client = boto3.client(service_name='s3', endpoint_url=LOCAL_STACK_URL)
else:
    s3_client = boto3.client('s3')

def parse_doc_text(bucket, key):
    logger.info("Downloading and processing document {}".format(key))
    s3_object = s3_client.get_object(Bucket=bucket, Key=key)
    
    # TODO: IMPLEMENT THE TEXT MINING STEPS HERE
    logger.info("Downloaded s3 object {}".format(key))
    return ["text1", "text2"]


def lambda_handler(event, context):
    '''
    Handles newly uploaded pattent pdf docs.
    '''
    print(s3_client)
    logger.debug("Handling event: {}".format(json.dumps(event, indent=2)));
    bucket = event['Records'][0]['s3']['bucket']['name']
    object_key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])

    try:
        response = parse_doc_text(bucket, object_key)
        logger.info("Done handling event")
        return 'Success'

    except Exception as e:
        logger.error("Error processing object {} from bucket {}. Event {} Error: {}".format(object_key, bucket, json.dumps(event, indent=2),  e))
        raise e