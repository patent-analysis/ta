FROM amazon/aws-lambda-python:3.8

COPY requirements.txt ./

RUN python3.8 -m pip install -r requirements.txt -t .

# This is a workaround SAM caching and reusing the docker layers after making changes.
# This line gurantee that any layer after this line will be rebuilt with every sam build invocation
ADD "https://www.random.org/cgi-bin/randbyte?nbytes=10&format=h" skipcache

COPY app.py ./

CMD ["app.lambda_handler"]
