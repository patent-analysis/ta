FROM amazon/aws-lambda-python:3.8

COPY . ./

RUN yum -y install poppler-utils flac swig wget yum-utils
RUN cat /etc/os-release

# Install tesseract v4 and it's dependencies
RUN yum -y update
RUN yum-config-manager --add-repo https://download.opensuse.org/repositories/home:/Alexander_Pozdnyakov/RHEL_7/
RUN rpm --import https://build.opensuse.org/projects/home:Alexander_Pozdnyakov/public_key
RUN yum -y install tesseract 
RUN yum -y install tesseract-langpack-deu

RUN tesseract --version
RUN pip install --upgrade pip
RUN pip install -r requirements.txt -t .
RUN pip install -U pymupdf

# # This is a workaround SAM caching and reusing the docker layers after making changes.
# # This line gurantee that any layer after this line will be rebuilt with every sam build invocation
# ADD "https://www.random.org/cgi-bin/randbyte?nbytes=10&format=h" skipcache

CMD ["app.lambda_handler"]
