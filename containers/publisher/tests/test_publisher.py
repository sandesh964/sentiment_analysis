"""
Test case to validate pubsub app functionality
"""
import json

import configparser
import mock
from google.cloud import pubsub_v1
from publisher.app.tweet_publisher import PubSubListener
from publisher.tests.pubsub import PubSubRunner


def mock_tweet():
    """Generate some random tweet text."""
    tweet_str = """{"created_at":"Wed Aug 07 13:28:00 +0000 2019","id":1159093838364983296,"id_str":"1159093838364983296","text":"test_tweet","source":"Twitter for Android","truncated":false,"in_reply_to_status_id":null,"in_reply_to_status_id_str":null,"in_reply_to_user_id":null,"in_reply_to_user_id_str":null,"in_reply_to_screen_name":null,"user":{"id":4186465095,"id_str":"4186465095","name":"test_name","screen_name":"test_scrname","location":null,"url":null,"description":"test_description","translator_type":"none","protected":false,"verified":false,"followers_count":301,"friends_count":979,"listed_count":9,"favourites_count":54190,"statuses_count":57192,"created_at":"Sat Nov 14 13:10:41 +0000 2015","utc_offset":null,"time_zone":null,"geo_enabled":false,"lang":null,"contributors_enabled":false,"is_translator":false,"profile_background_color":"C0DEED","profile_background_image_url":"bg.png","profile_background_image_url_https":"bg.png","profile_background_tile":false,"profile_link_color":"1DA1F2","profile_sidebar_border_color":"C0DEED","profile_sidebar_fill_color":"DDEEF6","profile_text_color":"333333","profile_use_background_image":true,"profile_image_url":"wDdrz-Xh_normal.jpg","profile_image_url_https":"Ddrz-Xh_normal.jpg","default_profile":true,"default_profile_image":false,"following":null,"follow_request_sent":null,"notifications":null},"geo":null,"coordinates":null,"place":null,"contributors":null,"retweeted_status":{"created_at":"Fri Jul 26 16:14:59 +0000 2019","id":1154787205094805509,"id_str":"1154787205094805509","text":"SUPREME COURT ON THE LINE: Trump has his eyes set on naming two more right-wing judges like Brett Kavanaugh to the...","source":"Twitter Ads Composer","truncated":true,"in_reply_to_status_id":null,"in_reply_to_status_id_str":null,"in_reply_to_user_id":null,"in_reply_to_user_id_str":null,"in_reply_to_screen_name":null,"user":{"id":939091,"id_str":"939091","name":"Joe Biden","screen_name":"JoeBiden","location":"Wilmington, DE","url":"http://joebiden.com","description":"Senator, Vice President, 2020 candidate for President of the United States, husband to @DrBiden, proud father & grandfather. Loves ice cream, aviators & @Amtrak","translator_type":"none","protected":false,"verified":true,"followers_count":3655177,"friends_count":22,"listed_count":14033,"favourites_count":16,"statuses_count":2273,"created_at":"Sun Mar 11 17:51:24 +0000 2007","utc_offset":null,"time_zone":null,"geo_enabled":false,"lang":null,"contributors_enabled":false,"is_translator":false,"profile_background_color":"565959","profile_background_image_url":"bg.png","profile_background_image_url_https":"/bg.png","profile_background_tile":true,"profile_link_color":"233F94","profile_sidebar_border_color":"FFFFFF","profile_sidebar_fill_color":"EBEBFF","profile_text_color":"323232","profile_use_background_image":true,"profile_image_url":"f4GqlaQL_normal.png","profile_image_url_https":"f4GqlaQL_normal.png","profile_banner_url":"1558224273","default_profile":false,"default_profile_image":false,"following":null,"follow_request_sent":null,"notifications":null},"geo":null,"coordinates":null,"place":null,"contributors":null,"is_quote_status":false,"extended_tweet":{"full_text":"SUPREME COURT ON THE LINE: Trump has his eyes set on naming two more right-wing judges like Brett Kavanaugh to the Supreme Court. The only way to stop him is to beat him in 2020, but we cant do it without support from people like you. We need to know: Do you want to beat Trump?","display_text_range":[0,279],"entities":{"hashtags":[],"urls":[],"user_mentions":[],"symbols":[]}},"quote_count":461,"reply_count":3310,"retweet_count":2335,"favorite_count":9319,"entities":{"hashtags":[],"urls":[{"url":"","expanded_url":"","display_url":"","indices":[116,139]}],"user_mentions":[],"symbols":[]},"favorited":false,"retweeted":false,"scopes":{"followers":false},"filter_level":"low","lang":"en"},"is_quote_status":false,"quote_count":0,"reply_count":0,"retweet_count":0,"favorite_count":0,"entities":{"hashtags":[],"urls":[],"user_mentions":[{"screen_name":"JoeBiden","name":"Joe Biden","id":939091,"id_str":"939091","indices":[3,12]}],"symbols":[]},"favorited":false,"retweeted":false,"filter_level":"low","lang":"en","timestamp_ms":"1565184480645"}"""

    # count = random.randint(70, 140)
    # return ''.join([random.choice(string.ascii_letters) for _ in range(count)])
    return tweet_str


def test_publisher():
    """
    Test case to verify the tweet publilsher functionality
    :return: None
    """
    # Initialize pubsub emulator
    pubsub_instance = PubSubRunner()

    # start pubsub emulator - on standard kafka port :) - My liking for Kafka ;)
    pubsub_instance.start('6667')
    print 'PID:', pubsub_instance.process.pid

    # create an instance of PubSubListener that posts messages/tweets to pubsub topic
    config = configparser.ConfigParser()

    # create client objects
    publisher = pubsub_v1.PublisherClient()
    subscriber = pubsub_v1.SubscriberClient()

    with mock.patch.dict(config, {'PUBSUB': {'topic': 'tweet'}, 'GOOGLE': {'project': 'test_project'}}):
        topic_name = 'projects/{project_id}/topics/{topic}'.format(
            project_id=config.get('GOOGLE', 'project'),
            topic=config.get('PUBSUB', 'topic'),  # Set this to something appropriate.
        )
        subscription_name = 'projects/{project_id}/subscriptions/{sub}'.format(
            project_id=config.get('GOOGLE', 'project'),
            sub='TEST_SUBSCRIPTION_NAME',  # Set this to something appropriate.
        )

        # create topic
        publisher.create_topic(topic_name)
        listener = PubSubListener(conf=config)
        listener.on_data(mock_tweet())

        # validate the message - Pulling a subscription synchronously
        subscriber.create_subscription(name=subscription_name, topic=topic_name)
        subscription_path = subscriber.subscription_path(config.get('GOOGLE', 'project'), 'TEST_SUBSCRIPTION_NAME')
        response = subscriber.pull(subscription_path, max_messages=1)
        # print response, len(response.received_messages)

        # Acknowledges the received messages so they will not be sent again.
        ack_ids = [msg.ack_id for msg in response.received_messages]
        subscriber.acknowledge(subscription_path, ack_ids)

        # TEST: All messages should have been processed exactly once. i.e., INPUT_MSG_COUNT == OUTPUT_MSG_COUNT
        assert len(response.received_messages) == 1

        # TEST: Validate the contets of the processed message, since i am posting only one message, have used the list
        # index, if not we need to use the iterator
        msg = json.loads(response.received_messages[0].message.data)
        assert msg['text'] == 'test_tweet'
        assert msg['created_at'] == '2019-08-07 13:28:00+00:00'
        assert msg['id'] == 1159093838364983296
        assert msg['author'] == 'test_scrname'

        # cleanup
        publisher.delete_topic(topic_name)
        subscriber.delete_subscription(subscription_name)

    # stop pubsub and
    pubsub_instance.kill()
