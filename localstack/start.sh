#!/bin/bash
echo "creating the host_net docker network ..."
docker network create host_net
echo "starting the localstack environment.."
docker-compose up -d
echo "creating a dummy bucket in the local env..."
aws --endpoint-url=http://localhost:4566 s3 mb s3://local-bucket
echo "modify the bucket acl"
aws --endpoint-url=http://localhost:4566 s3api put-bucket-acl --bucket local-bucket --acl public-read
echo "verifying the bucket was created successfully..."
aws --endpoint-url=http://localhost:4566 s3 ls
echo "adding a local file  from the directory localstack/..."
aws --endpoint-url=http://localhost:4566 s3 cp local-patent.pdf s3://local-bucket
echo "listing all objects..."
aws --endpoint-url=http://localhost:4566 s3 ls s3://local-bucket
echo "done starting the localstack env."
