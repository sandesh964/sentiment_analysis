FROM centos:latest
MAINTAINER Amar Sandesh Bachu

# set the timezone to Australia/Sydney
RUN ln -s -f /usr/share/zoneinfo/Australia/Sydney /etc/localtime

# update to latest packages and clear out the yum cache again
RUN yum clean all && \
    yum update -y --security

# Install epel
RUN yum install -y epel-release

# Install pip
RUN yum install -y python-devel
RUN yum install -y python-pip

# Upgrade pip to be able install dependencies
RUN pip install --upgrade pip

# given most images start by flushing the cache, a clean at the end saves over 200MB in image size
RUN yum clean all
