# Publisher - Twitter Sentiment Analysis

Docker Image for running publisher application that scrapes twitter using its rest-api to 
filter the tweets of our interest and stream the data to pubsub topic

## Localisations
* Add python dependencies and setup the image for use.
* Deploy and start the application

## Building the custom Image

To build the image run the invoke task `build-image`:
```bash
$ invoke build-image -d . -t publisher
Sending build context to Docker daemon    149kB

Step 1/13 : FROM python:latest
 ---> bae66c845ebd
Step 2/13 : LABEL maintainer="Amar Sandesh Bachu"
 ---> Using cache
 ---> da66164da26b
Step 3/13 : LABEL publisher="0.1"
 ---> Using cache
 ---> 7204afa3978a
Step 4/13 : ENV PYTHONPATH /publisher
 ---> Using cache
 ---> 1ba03a1586ed
Step 5/13 : RUN mkdir /publisher
 ---> Using cache
 ---> 3b2504c44583
Step 6/13 : WORKDIR /publisher
 ---> Using cache
 ---> 9b7bb9be1f24
Step 7/13 : RUN mkdir /publisher/credentials
 ---> Using cache
 ---> 80ec33a56846
Step 8/13 : COPY credentials /publisher/credentials
 ---> Using cache
 ---> 8c446f81d1ad
Step 9/13 : COPY credentials/app.conf /publisher
 ---> b63fe50c9acd
Step 10/13 : COPY requirements.txt /publisher
 ---> 2c2ccc7d00b2
Step 11/13 : COPY app /publisher
 ---> b090b3ff0590
Step 12/13 : RUN pip install -r requirements.txt
 ---> Running in 4c517e8b52d7
Removing intermediate container 4c517e8b52d7
 ---> 084e71d9c0f0
Step 13/13 : CMD ["python", "/publisher/tweet_publisher.py"]
 ---> Running in f74bd58c926e
Removing intermediate container f74bd58c926e
 ---> ae2c0df67794
Successfully built ae2c0df67794
Successfully tagged publisher:latest
```

- List the images to check if the updated image is present

```bash
docker images
```
![Alt](screenshots/docker-images.png?raw=true)

# Testing the image
Execute the following command to test the image
```
invoke test-publisher-image
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
docker run -d publisher
```

# Run Functional Test

The functional test uses pubsub emulator to verify the functionality.

* Install pubsub using the instructions https://cloud.google.com/pubsub/docs/emulator
* On a GCE instance cloud sdk is disabled, so use yum install instead of gcloud update.

```bash
sudo yum install -y google-cloud-sdk-pubsub-emulator
```

* Run the following command to execute the functional test:

```bash
$ invoke test-publisher

============================= test session starts ==============================
platform linux2 -- Python 2.7.5, pytest-4.6.5, py-1.8.0, pluggy-0.12.0 -- /usr/bin/python2
cachedir: .pytest_cache
rootdir: /home/gitlab-runner/builds/UnJ8SfDw/0/anz-code-challenge/containers/publisher, inifile: pytest.ini
plugins: cov-2.7.1, bdd-3.1.1, env-0.6.2, testinfra-3.0.6
collecting ... collected 1 item

tests/test_publisher.py::test_publisher Executing: /usr/lib64/google-cloud-sdk/platform/pubsub-emulator/bin/cloud-pubsub-emulator --host=127.0.0.1 --port=6667
[pubsub] This is the Google Pub/Sub fake.
[pubsub] Implementation may be incomplete or differ from the real system.
[pubsub] Aug 13, 2019 2:34:14 PM com.google.cloud.pubsub.testing.v1.Main main
[pubsub] INFO: IAM integration is disabled. IAM policy methods and ACL checks are not supported
[pubsub] Aug 13, 2019 2:34:14 PM io.gapi.emulators.netty.NettyUtil applyJava7LongHostnameWorkaround
[pubsub] INFO: Applied Java 7 long hostname workaround.
[pubsub] Aug 13, 2019 2:34:14 PM com.google.cloud.pubsub.testing.v1.Main main
[pubsub] INFO: Server started, listening on 6667
[pubsub] Aug 13, 2019 2:34:14 PM io.gapi.emulators.grpc.GrpcServer$3 operationComplete
[pubsub] INFO: Adding handler(s) to newly registered Channel.
[pubsub] Aug 13, 2019 2:34:14 PM io.gapi.emulators.netty.HttpVersionRoutingHandler channelRead
[pubsub] INFO: Detected HTTP/2 connection.
PID: 28570
{u'quote_count': 0, u'contributors': None, u'truncated': False, u'text': u'test_tweet', u'is_quote_status': False, u'in_reply_to_status_id': None, u'reply_count': 0, u'id': 1159093838364983296, u'favorite_count': 0, u'entities': {u'user_mentions': [{u'id': 939091, u'indices': [3, 12], u'id_str': u'939091', u'screen_name': u'JoeBiden', u'name': u'Joe Biden'}], u'symbols': [], u'hashtags': [], u'urls': []}, u'retweeted': False, u'coordinates': None, u'timestamp_ms': u'1565184480645', u'source': u'Twitter for Android', u'in_reply_to_screen_name': None, u'id_str': u'1159093838364983296', u'retweet_count': 0, u'in_reply_to_user_id': None, u'favorited': False, u'retweeted_status': {u'quote_count': 461, u'contributors': None, u'truncated': True, u'text': u'SUPREME COURT ON THE LINE: Trump has his eyes set on naming two more right-wing judges like Brett Kavanaugh to the...', u'is_quote_status': False, u'in_reply_to_status_id': None, u'reply_count': 3310, u'id': 1154787205094805509, u'favorite_count': 9319, u'entities': {u'user_mentions': [], u'symbols': [], u'hashtags': [], u'urls': [{u'url': u'', u'indices': [116, 139], u'expanded_url': u'', u'display_url': u''}]}, u'retweeted': False, u'coordinates': None, u'source': u'Twitter Ads Composer', u'in_reply_to_screen_name': None, u'id_str': u'1154787205094805509', u'scopes': {u'followers': False}, u'retweet_count': 2335, u'in_reply_to_user_id': None, u'favorited': False, u'user': {u'follow_request_sent': None, u'profile_use_background_image': True, u'default_profile_image': False, u'id': 939091, u'default_profile': False, u'verified': True, u'profile_image_url_https': u'f4GqlaQL_normal.png', u'profile_sidebar_fill_color': u'EBEBFF', u'profile_text_color': u'323232', u'followers_count': 3655177, u'profile_sidebar_border_color': u'FFFFFF', u'id_str': u'939091', u'profile_background_color': u'565959', u'listed_count': 14033, u'profile_background_image_url_https': u'/bg.png', u'utc_offset': None, u'statuses_count': 2273, u'description': u'Senator, Vice President, 2020 candidate for President of the United States, husband to @DrBiden, proud father & grandfather. Loves ice cream, aviators & @Amtrak', u'friends_count': 22, u'location': u'Wilmington, DE', u'profile_link_color': u'233F94', u'profile_image_url': u'f4GqlaQL_normal.png', u'following': None, u'geo_enabled': False, u'profile_banner_url': u'1558224273', u'profile_background_image_url': u'bg.png', u'name': u'Joe Biden', u'lang': None, u'profile_background_tile': True, u'favourites_count': 16, u'screen_name': u'JoeBiden', u'notifications': None, u'url': u'http://joebiden.com', u'created_at': u'Sun Mar 11 17:51:24 +0000 2007', u'contributors_enabled': False, u'time_zone': None, u'protected': False, u'translator_type': u'none', u'is_translator': False}, u'geo': None, u'in_reply_to_user_id_str': None, u'lang': u'en', u'extended_tweet': {u'display_text_range': [0, 279], u'entities': {u'user_mentions': [], u'symbols': [], u'hashtags': [], u'urls': []}, u'full_text': u'SUPREME COURT ON THE LINE: Trump has his eyes set on naming two more right-wing judges like Brett Kavanaugh to the Supreme Court. The only way to stop him is to beat him in 2020, but we cant do it without support from people like you. We need to know: Do you want to beat Trump?'}, u'created_at': u'Fri Jul 26 16:14:59 +0000 2019', u'filter_level': u'low', u'in_reply_to_status_id_str': None, u'place': None}, u'user': {u'follow_request_sent': None, u'profile_use_background_image': True, u'default_profile_image': False, u'id': 4186465095, u'default_profile': True, u'verified': False, u'profile_image_url_https': u'Ddrz-Xh_normal.jpg', u'profile_sidebar_fill_color': u'DDEEF6', u'profile_text_color': u'333333', u'followers_count': 301, u'profile_sidebar_border_color': u'C0DEED', u'id_str': u'4186465095', u'profile_background_color': u'C0DEED', u'listed_count': 9, u'profile_background_image_url_https': u'bg.png', u'utc_offset': None, u'statuses_count': 57192, u'description': u'test_description', u'friends_count': 979, u'location': None, u'profile_link_color': u'1DA1F2', u'profile_image_url': u'wDdrz-Xh_normal.jpg', u'following': None, u'geo_enabled': False, u'profile_background_image_url': u'bg.png', u'name': u'test_name', u'lang': None, u'profile_background_tile': False, u'favourites_count': 54190, u'screen_name': u'test_scrname', u'notifications': None, u'url': None, u'created_at': u'Sat Nov 14 13:10:41 +0000 2015', u'contributors_enabled': False, u'time_zone': None, u'protected': False, u'translator_type': u'none', u'is_translator': False}, u'geo': None, u'in_reply_to_user_id_str': None, u'lang': u'en', u'created_at': u'Wed Aug 07 13:28:00 +0000 2019', u'filter_level': u'low', u'in_reply_to_status_id_str': None, u'place': None}
PASSED
```
