import json
import os
import boto3
from moto import mock_s3, mock_dynamodb2
import pytest


mock_event_file = os.path.join(
    os.path.realpath('../ta'), 
    "events/mock_event.json")
mock_event_data = open(mock_event_file)
mock_event = json.load(mock_event_data)

MOCK_BUCKET_NAME = 'mock-bucket'
MOCK_OBJECT_NAME = 'mock-patent.pdf'


@pytest.fixture(scope='function')
def aws_credentials():
    """Mocked AWS Credentials"""
    os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
    os.environ['AWS_SECURITY_TOKEN'] = 'testing'
    os.environ['AWS_SESSION_TOKEN'] = 'testing'


@pytest.fixture()
def s3(aws_credentials):
    """Pytest fixture which creates a mock
    s3 bucket and yields a fake boto3 s3 client
    """
    with mock_s3():
        s3 = boto3.client("s3", region_name='us-east-1')
        s3.create_bucket(Bucket=MOCK_BUCKET_NAME)
        yield s3

def test_handle_event(s3, mocker):
    mocker.patch('app.fitz.open')
    mocker.patch('builtins.open')
    mocker.patch('os.path.exists')
    mocker.patch('app.requests.get', return_value= MockResponse())
    mocker.patch('app.SeqListing')
    mocker.patch('app.Patent')
    mocker.patch('app.dynamodb')
    mocker.patch('app.textract.process', return_value=str.encode("US800023421B2"))
    import os, sys, inspect
    currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    parentdir = os.path.dirname(currentdir)
    sys.path.insert(0,parentdir) 
    import app
    s3.put_object(Bucket=MOCK_BUCKET_NAME, Key=MOCK_OBJECT_NAME, Body="")
    handler_resp = app.lambda_handler(mock_event, context={})
    assert handler_resp == 'Success'



class MockResponse:
    def __init__(self):
        self.status_code = 200
        self.content = ""