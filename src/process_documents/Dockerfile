FROM amazon/aws-lambda-python:3.8

COPY . ./

RUN yum -y install poppler-utils flac swig tesseract

# RUN rpm -Uvh https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm
# RUN yum -y update
# RUN yum -y install tesseract

RUN pip install --upgrade pip

RUN pip install -r requirements.txt -t .

RUN pip install -U pymupdf

# # This is a workaround SAM caching and reusing the docker layers after making changes.
# # This line gurantee that any layer after this line will be rebuilt with every sam build invocation
# ADD "https://www.random.org/cgi-bin/randbyte?nbytes=10&format=h" skipcache



CMD ["app.lambda_handler"]
