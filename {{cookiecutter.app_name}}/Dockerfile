FROM python:3.6.4-jessie

# Add node 7 repo to apt-get
RUN curl --silent --location https://deb.nodesource.com/setup_7.x | bash -

# Install languages via package manager
RUN apt-get install -y nodejs python-dev

# Install npm dependencies
RUN npm install -g markdown-magic

# Install Python Dependencies
ARG pypi_config
RUN mkdir /root/.pip/ && echo "$pypi_config" > /root/.pip/pip.conf
ENV PIP_CONFIG_FILE=/root/.pip/pip.conf

RUN pip install pipenv
COPY Pipfile /pip/Pipfile
RUN cd /pip && pipenv install --dev
RUN pip install virtualenvwrapper
