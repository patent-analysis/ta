# Patent Text Analysis Pipeline
[![.github/workflows/main.yaml](https://github.com/patent-analysis/ta/actions/workflows/main.yaml/badge.svg)](https://github.com/patent-analysis/ta/actions/workflows/main.yaml)
This is a serverless stack that will be triggered to mine the patent pdf documents once they are uploaded to the storage S3 bucket.


## Project structure
Below is the project structure.
```bash
.
├── README.md                       <-- This is the readme file
├── src                             <-- Source code for the Lambda functions
│   └── process_documents           <-- Source code for the Text Mining Lambda function
│       ├── __init__.py
│       │── app.py                  <-- Lambda function code
│       └── Dockerfile              <-- Docker file used to build the function.
│
├── tests
│   ├── __init__.py
│   └── test_process_documents.py   <-- Tests for the process_documents  function.
│
├── localstack                      <-- This is a local AWS environment that can be started locally.
│   ├── start.sh                    <-- Script to start the local aws environment.
│   ├── docker-compose.yaml         <-- Docker compose file to start the build and run the docker environment.
│   └── local-patent.pdf            <-- Dummy text document disguised as pdf for testing.
│
├── events                          <-- Directory containing mock events to use for testing.
│   └── ....                        <-- Test events
│
├── requirements_*.txt              <-- Python requirements files
├── Makefile                        <-- Make file to bootstrap the project scripts           
└── template.yaml                   <-- AWS Environment SAM template
```


## Requirements
* AWS CLI
* [Python 3.8 installed](https://www.python.org/downloads/)
* [Docker installed](https://www.docker.com/community-edition)
* [make](https://www.docker.com/community-edition)
* [sam] (https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html)

## How to build and run the stack locally

### Running the unit tests
After installing all the prerequisites, you should be able to install the test requirements using:

```bash
make init
```

### Start a mock aws environment locally
We use [localstack](https://github.com/localstack/localstack) to install and run a mock aws environment locally. All you have to do to get the environment started is run the command below to build and start a docker container that hosts multiple aws services:

```bash
make stack-up
```
To stop the container and delete it run:

```bash
make stack-down
```

### Invoke the lambda
To invoke the process_document lambda function using a mock s3 event, run the command below.

```bash
make run-local
```

To run the function again in debug mode, run:

```bash
make debug-local
```

### Build the stack
TODO

### Deploy the stack
TODO
