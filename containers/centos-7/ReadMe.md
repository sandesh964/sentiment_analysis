# Docker Centos 7 Base Image

Stock **`Centos 7`** container with minimal localisations
to host the publisher and subscriber modules as micro-services sitting on
either side of **`pubsub`** with former scraping tweets using twitter api and
the later performing sentiment analysis on the tweets being pushed to
the subscription.

## Localisations
* Download the **`centos7:latest`** image. 

```bash
docker pull centos
```
* apply the latest patches as at the build time (yum update)
* set timezone to `Australia/Sydney`
* Add python dependencies and setup the image for use.

## Building the custom Image

To build the image run the invoke task `build-image`:
```bash
$ invoke build-image -d centos-7/
Sending build context to Docker daemon  5.632kB
Step 1/6 : FROM centos:latest
Step 2/6 : MAINTAINER Amar Sandesh Bachu
Step 3/6 : RUN ln -s -f /usr/share/zoneinfo/Australia/Sydney /etc/localtime
Step 4/6 : RUN yum clean all &&     yum update -y --security &&     yum clean all
Step 5/6 : RUN yum install -y epel-release
Step 6/8 : RUN yum install -y python-pip
Step 7/8 : RUN pip install --upgrade pip
Step 8/8 : RUN yum clean all
Complete!
Removing intermediate container 7ff85b9162c2
 ---> 167a3f9c57de
Successfully built 167a3f9c57de
Successfully tagged centos:2019-08-08_23_17_30.559035
(venv) CMM-C02Y31T1JGH6:docker d696445$ 

```

- List the images to check if the updated image is present

```bash
docker images
```
![Alt](screenshots/docker-images.png?raw=true)

# Testing the image
Execute the following command to test the centos-7 image
```
cd centos-7
invoke test-centos-image
```
![Alt](screenshots/docker-img-test.png?raw=true)

**TBD:** Setup a Local registry and push the tested images to local docker registry

# CI PIPELINE
The project is enabled with gitlab-ci pipeline and below is the pipeline summary and description:

![Alt](screenshots/gitlab-centos-pipeline.png?raw=true)

![Alt](screenshots/ci-pipeline-expanded.png?raw=true)
