FROM python:latest
LABEL maintainer="Amar Sandesh Bachu"
LABEL publisher="0.1"

# set Environment variables
ENV PYTHONPATH /publisher

# Create project directory
RUN mkdir /publisher

# Set working directory
WORKDIR /publisher

# COPY Credentials, The credentials directory contains app.conf and GCP credentials
RUN mkdir /publisher/credentials
COPY credentials /publisher/credentials

# COPY app configs
COPY credentials/app.conf /publisher

# COPY python requriements.
COPY requirements.txt /publisher
COPY app /publisher

# Install python dependencies
RUN pip install -r requirements.txt

# START PUBLISHER
CMD ["python", "/publisher/tweet_publisher.py"]
