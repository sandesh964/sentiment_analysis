FROM python:latest
LABEL maintainer="Amar Sandesh Bachu"
LABEL dashboard="0.1"

# set Environment variables
ENV PYTHONPATH /dashboard

# Create project directory
RUN mkdir /dashboard

# Set working directory
WORKDIR /dashboard

# COPY python requriements.
COPY requirements.txt /dashboard
COPY web-app /dashboard

# Install python dependencies
RUN pip install -r requirements.txt

# Bind container application port 3527 to the docker host
EXPOSE 3527

# START PUBLISHER
CMD ["python", "/dashboard/app.py"]
