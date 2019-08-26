"""
Twitter subscriber to enqueue tweets from pubsub topic and use google NLP API to perform sentiment analysis.
This module publishes the analyzed sentiment metrics to a dashboard that gives a graphical representation of the
sentiment analysis interpretation. The dashboard updates by itself as long as the metrics are being published and the
dashboard container is alive.
"""
#!/usr/bin/env python2

import bisect
import json
import os
import sys
import time
import traceback
from collections import Counter
from collections import defaultdict

import configparser
import requests
from google.cloud import language_v1
from google.cloud import pubsub_v1
from google.cloud.language_v1 import enums

MSGS_PROCESSED = 0
TWEET_SUMMARY = defaultdict(list)
WEB_APP_UPDATE_URL = 'http://localhost:3527/updateData'


def classify_sentiment(score):
    """
    Classify sentiment based on the analysis score.
    :param score: Sentiment score
    :return: string
    """
    sentiment_matrix = [
        (-0.1, 'Clearly Negative'),
        (0.0, 'Mixed'),
        (0.1, 'Neutral'),
        (0.2, 'Clearly Positive')
    ]
    # sort the list
    sentiment_matrix.sort()
    pos = bisect.bisect_right(sentiment_matrix, (score,), lo=0, hi=len(sentiment_matrix) - 1)
    # print '{0}=>{1}'.format(score, sentiment_matrix[pos][1])
    return sentiment_matrix[pos][1]


# def index_to_es(document, sentiment_result):
#     """
#     Index data to elastic search for visualisation and analysis
#     :param document: tweet extracted from pubsub message
#     :param sentiment_result: result of sentiment analysis
#     :return: None
#     """
#     score = sentiment_result.document_sentiment.score
#     # To keep the usecase simple let us classify the sentiment based on the score, magnitude can be used for a
#     # deeper usecase where better decisions needs to be made based on the overall context.
#     # magnitude = sentiment_result.document_sentiment.magnitude
#     sentiment = classify_sentiment(score)
#     # print('Overall Sentiment: score of {}-{} with magnitude of {} for {}'.
#     # format(score, sentiment, magnitude, document))
#     return sentiment


def send_to_dashboard(aggregated_result):
    """
    Sends the output of the latest analysis represented to the webapp
    :param aggregated_result: dict
    :return: HTTP 201 if the update is successful
    """
    # extract the sentiment classification from the aggregated_result
    sentiment_classification = aggregated_result.keys()
    # extract the counts from dict and convert them into array
    sentiment_count = aggregated_result.values()
    # initialize and send the data through REST API
    request_data = {'label': str(sentiment_classification), 'data': str(sentiment_count)}
    response = requests.post(WEB_APP_UPDATE_URL, data=request_data)
    print response


def analyze_sentiment(received_message):
    """
    Analyze the sentiment of the incoming tweet using goolge NLP API
    :param received_message: message from the pubsub topic
    :type: google.cloud.pubsub_v1.subscriber.message.Message
    :return: None
    """
    global TWEET_SUMMARY
    tweet = json.loads(received_message)
    tweet_msg = {'type': enums.Document.Type.PLAIN_TEXT, 'content': tweet['text']}
    client = language_v1.LanguageServiceClient()
    # annotations = client.analyze_sentiment(document=tweet_msg, encoding_type=enums.EncodingType.UTF8)
    sentiment_result = client.analyze_sentiment(document=tweet_msg, encoding_type=enums.EncodingType.UTF8)
    # print 'Annotations:', annotations
    # sentiment = index_to_es(tweet, annotations)
    sentiment = classify_sentiment(sentiment_result.document_sentiment.score)
    TWEET_SUMMARY[sentiment].append(tweet['id'])


def callback(message):
    """
    Callback method to process the message
    :param message: message from the pubsub topic
    :type: google.cloud.pubsub_v1.subscriber.message.Message
    :return: None
    """
    global MSGS_PROCESSED

    # print('Received message: {}'.format(message))
    try:
        analyze_sentiment(message.data)
        # Acknowlege the message so that it will not be sent again
        message.ack()
        MSGS_PROCESSED = MSGS_PROCESSED + 1
    except Exception as exception_obj:
        # Decline to acknowldge the given message, so that the message can be delivered again
        print 'Exception Occured', exception_obj
        traceback.print_exc(file=sys.stdout)
        message.nack()
        # pass


def receive_messages(conf):
    """
    Recieves messages (tweets) from a pubsub topic using a pull subscription
    :param conf: config parser instance
    :return: None
    """

    subscriber = pubsub_v1.SubscriberClient()
    # The `subscription_path` method creates a fully qualified identifier
    # in the form `projects/{project_id}/subscriptions/{subscription_name}`
    subscription_path = subscriber.subscription_path(conf.get('GOOGLE', 'project'),
                                                     conf.get('GOOGLE', 'subscription_name'))

    # Asynchronously start receiving messages on a given subscription.
    # This method starts a background thread to begin pulling messages from a
    # Pub/Sub subscription and scheduling them to be processed using the provided ``callback``.
    # Limit the subscriber to have only 200 outstanding messages at a time. This is to avoid memory issues if there
    # is a considerable consumer/subscriber lag due to the lack of resources to process the messages at a rate that
    # cloud pubsub is sending. This number can be adjusted based on the resource availability
    # and average processing time per message so that the consumer/subscriber can
    # scale to the input rate at which pubsub is pushing the messages.

    num_messages = 200
    flow_control = pubsub_v1.types.FlowControl(max_messages=num_messages)
    subscriber.subscribe(subscription_path, callback=callback, flow_control=flow_control)

    # The subscriber is non-blocking. Keep the main thread from
    # exiting to allow it to process messages asynchronously in the background.
    print 'Listening for messages on {}'.format(subscription_path)
    aggregated_dict = Counter(defaultdict(list))
    while True:
        print 'Sleeping.... after processing {0}'.format(MSGS_PROCESSED)
        if any(TWEET_SUMMARY):
            aggregated_dict = aggregated_dict + Counter({key: len(value) for key, value in TWEET_SUMMARY.items()})
            TWEET_SUMMARY.clear()
            send_to_dashboard(aggregated_dict)
        time.sleep(60)


if __name__ == "__main__":
    # Fetch the credentials from conf
    CONFIG = configparser.ConfigParser()
    CONFIG.read('{0}/app.conf'.format(os.environ['PYTHONPATH']))
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '{0}/{1}'.format(os.environ['PYTHONPATH'],
                                                                    CONFIG.get('GOOGLE', 'credentials'))
    receive_messages(CONFIG)
