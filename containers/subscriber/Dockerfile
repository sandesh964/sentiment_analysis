FROM python:latest
LABEL maintainer="Amar Sandesh Bachu"
LABEL subscriber="0.1"

# set Environment variables
ENV PYTHONPATH /subscriber

# Create project directory
RUN mkdir /subscriber

# Set working directory
WORKDIR /subscriber

# COPY Credentials
RUN mkdir /subscriber/credentials
COPY credentials /subscriber/credentials

# COPY app configs
COPY credentials/app.conf /subscriber

# COPY python requriements.
COPY requirements.txt /subscriber
COPY app /subscriber

# Install python dependencies
RUN pip install -r requirements.txt

# START PUBLISHER
CMD ["python", "/subscriber/tweet_subscriber.py"]
