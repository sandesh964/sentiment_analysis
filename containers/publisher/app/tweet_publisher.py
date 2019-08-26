"""
Twitter app to scrap the tweets using twitter rest-api and publish the tweets to google pubsub topic
"""
#!/usr/bin/env python2

import json
import os
import sys
import traceback

import configparser
from dateutil.parser import parse
from google.cloud import pubsub_v1
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener


class StdOutListener(StreamListener):
    """
    Tweet stream listener, Reads the twitter stream and prints the tweets to stdout.
    This listener is useful for smoke tests, to see if the we are able to fetch the actual tweets
    from twitter using the provided secrets.
    """

    def on_data(self, data):
        print data
        return True

    def on_error(self, status):
        print status


class PubSubListener(StreamListener):
    """
    PubSubListener - Reads the twitter stream and pushes the tweets to pubsub topic
    """

    def __init__(self, conf):
        super(StreamListener, self).__init__()

        # Configure the connection
        self.publisher = pubsub_v1.PublisherClient()
        self.topic_path = self.publisher.topic_path(conf.get('GOOGLE', 'project'), conf.get('PUBSUB', 'topic'))

    def on_data(self, raw_data):
        """
        Called when raw data is received from connection.
        overriden method super().on_data(), for custom implementation to push the data to pubsub topic
        :param raw_data: raw data from twitter
        :return:
        """
        tweet = json.loads(raw_data.encode('utf-8'))
        print tweet
        try:
            # skip msgs without text.. e.g.: {u'limit': {u'track': 10, u'timestamp_ms': u'1506431715917'}}
            self.publisher.publish(self.topic_path, data=json.dumps(
                {
                    "text": tweet['text'],
                    "author": tweet['user']['screen_name'],
                    "id": tweet['id'],
                    "created_at": str(parse(tweet['created_at']))
                }), tweet_id=str(tweet['id']).encode('utf-8')) if 'text' in tweet else None
        except Exception as exception_obj:
            print exception_obj
            traceback.print_exc(file=sys.stdout)
            return False
        return True

    def on_error(self, status_code):
        print status_code
        print 'Error received in Publshing to topic'
        if status_code == 420:
            print 'rate limit active'
            return False
        return True  # True to avoid the stream from being terminated

    def on_timeout(self):
        print 'Connection Timeout, will retry......'
        return True  # True to avoid the stream from being terminated


if __name__ == "__main__":
    # Fetch the credentials from conf
    CONFIG = configparser.ConfigParser()
    CONFIG.read('{0}/app.conf'.format(os.environ['PYTHONPATH']))
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '{0}/{1}'.format(os.environ['PYTHONPATH'],
                                                                    CONFIG.get('GOOGLE', 'credentials'))
    CONSUMER_KEY = CONFIG.get('TWITTER', 'consumer_key')
    CONSUMER_SECRET = CONFIG.get('TWITTER', 'consumer_secret')
    ACCESS_TOKEN = CONFIG.get('TWITTER', 'access_token')
    ACCESS_TOKEN_SECRET = CONFIG.get('TWITTER', 'access_token_secret')

    # Twitter authentication
    AUTH = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    AUTH.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    # Create Stream and bind it StdOutListener
    # console_listener = StdOutListener()
    # stream = Stream(auth, console_listener, tweet_mode='extended')

    # Create Stream and bind it to PubSubListener
    PUBSUB_LISTENER = PubSubListener(CONFIG)
    STREAM = Stream(AUTH, PUBSUB_LISTENER, tweet_mode='extended')

    # Filter Twitter Streams to capture data by the keywords: 'ashes'
    TRACK_LIST = (os.environ['TRACKLIST']).split(',')
    if TRACK_LIST:
        STREAM.filter(track=TRACK_LIST, languages=['en'])
    else:
        STREAM.filter(track=['cricket', 'india', '#got', '#cwc2019', '#ashes', 'trump'], languages=['en'])
    # stream.filter(locations=[-180, -90, 180, 90])
