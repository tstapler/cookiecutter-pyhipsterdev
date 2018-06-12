# Get python dependencies as extra build step to hide credentials
FROM python:3.6.4 as build

# Add node 7 repo to apt-get
RUN curl --silent --location https://deb.nodesource.com/setup_8.x | bash -

# Install languages via package manager
RUN apt-get install -y nodejs

# Install npm dependencies
RUN npm install -g markdown-magic

ARG PIP_INDEX_URL
ARG PIP_EXTRA_INDEX_URL=https://pypi.python.org/simple/

COPY requirements_dev.txt requirements_dev.txt
RUN pip install -r requirements_dev.txt
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
