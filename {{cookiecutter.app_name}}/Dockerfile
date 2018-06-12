# Get python dependencies as extra build step to hide credentials
FROM python:3.6.4 as python

# Add node 7 repo to apt-get
RUN curl --silent --location https://deb.nodesource.com/setup_7.x | bash -

# Install npm dependencies
RUN npm install -g markdown-magic

ARG PIP_INDEX_URL
ARG PIP_EXTRA_INDEX_URL=https://pypi.python.org/simple/

RUN pip install pipenv virtualenvwrapper
COPY Pipfile /pip/Pipfile
RUN cd /pip && pipenv install --dev

FROM python:3.6.4-jessie

# Install npm dependencies
RUN npm install -g markdown-magic

RUN pip install pipenv virtualenvwrapper
COPY --from=python /root/.virtualenvs /root/.local/share/virtualenvs
