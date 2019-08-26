# Dashboard - Twitter Sentiment Summary

Docker Image for hosting flask web-app to display twitter sentiment summary. This application
uses Flask and JQuery to display the sentiment analysis results as a bar chart.

## Localisations
* Add python dependencies and setup the image for use.
* Deploy and start the application

## Building the custom Image

To build the image run the invoke task `build-image`:
```bash
$ invoke build-image -d . -t dashboard
```
![Alt](screenshots/bake-image.png?raw=true)

- List the images to check if the updated image is present

```bash
docker images
```
![Alt](screenshots/docker-images.png?raw=true)

# Testing the image
Execute the following command to test the dashboard image
```
invoke test-dashboard
```
![Alt](screenshots/docker-img-test.png?raw=true)

**TBD:** Setup a Local registry and push the tested images to local docker registry

# CI PIPELINE
The project is enabled with gitlab-ci pipeline and below is the pipeline summary and description:

![Alt](screenshots/ci-pipeline.png?raw=true)

![Alt](screenshots/ci-pipeline-expanded.png?raw=true)
