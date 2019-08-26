# Subscriber - Twitter Sentiment Summary

Docker Image for running subscriber application to consume tweets from pubsub topic, perform sentiment analysis using 
google NLP API and publish the aggregated summary to the dashboard

## Localisations
* Add python dependencies and setup the image for use.
* Deploy and start the application

## Building the custom Image

To build the image run the invoke task `build-image`:


- List the images to check if the updated image is present

```bash
docker images
```
![Alt](screenshots/docker-images.png?raw=true)

# Testing the image
Execute the following command to test the image
```
invoke test-subscriber-image
```
![Alt](screenshots/docker-img-test.png?raw=true)

**TBD:** Setup a Local registry and push the tested images to local docker registry

# CI PIPELINE
The project is enabled with gitlab-ci pipeline and below is the pipeline summary and description:

![Alt](screenshots/ci-pipeline.png?raw=true)

![Alt](screenshots/ci-pipeline-expanded.png?raw=true)

# Running container
* Execute the following command to start the container

```bash
docker run --network host -d subscriber
```
* To verify if the subscriber is actually performing any sentiment-analysis:
1. Check the Cloud NLP API Dashboard

![Alt](screenshots/nlp-api-dashboard.png?raw=true)

2. Start the dashboard container and verify the barchart. The page refreshes by itself every minute
to present the latest aggregated results. The dashboard container requires IP forwarding to be enabled 
as we bind the webapp port to the host network. GCP disables it by default to guarentee that there is no packet
loss between the source and destination. We need to enable it during instance creation, if not then perform the follwing:

```bash
$ vi /etc/sysctl.conf

# Add the following line and save the file
net.ipv4.ip_forward=1

# Verify and Reload the network service
$ systemctl restart network
$ sysctl net.ipv4.ip_forward
net.ipv4.ip_forward = 1
```
![Alt](screenshots/tweet-dashboard-1.png?raw=true)

![Alt](screenshots/tweet-dashboard-2.png?raw=true)

# Run Functional Test

* Run the following command to execute the functional test:

```bash
$ invoke test-subscriber
[gitlab-runner@docker-01 subscriber]$ invoke test-subscriber
============================= test session starts ==============================
platform linux2 -- Python 2.7.5, pytest-4.6.5, py-1.8.0, pluggy-0.12.0 -- /usr/bin/python2
cachedir: .pytest_cache
rootdir: /home/gitlab-runner/builds/UnJ8SfDw/0/anz-code-challenge/containers/subscriber, inifile: pytest.ini
plugins: cov-2.7.1, bdd-3.1.1, env-0.6.2, testinfra-3.0.6
collecting ... collected 1 item

tests/test_subscriber.py::test_sentiment_classification PASSED
```
