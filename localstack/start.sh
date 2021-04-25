#!/bin/bash
docker network create host_network && 
echo "starting the localstack environment.."
docker-compose up -d
echo "waiting for the localstack services to start ..."
sleep 30s
echo "creating a dummy bucket in the local env..."
aws --endpoint-url=http://localhost:4566 s3 mb s3://local-bucket
echo "modify the bucket acl"
aws --endpoint-url=http://localhost:4566 s3api put-bucket-acl --bucket local-bucket --acl public-read
echo "verifying the bucket was created successfully..."
aws --endpoint-url=http://localhost:4566 s3 ls
echo "adding a local file  from the directory localstack/..."
aws --endpoint-url=http://localhost:4566 s3 cp local-patent.pdf s3://local-bucket/test/
echo "listing all objects..."
aws --endpoint-url=http://localhost:4566 s3 ls s3://local-bucket/test/
echo "create db"
aws --endpoint-url=http://localhost:4566  dynamodb create-table \
    --table-name patents-dev \
    --attribute-definitions AttributeName=patentNumber,AttributeType=S \
    --key-schema AttributeName=patentNumber,KeyType=HASH\
    --provisioned-throughput ReadCapacityUnits=10,WriteCapacityUnits=5\

echo "done starting the localstack env."