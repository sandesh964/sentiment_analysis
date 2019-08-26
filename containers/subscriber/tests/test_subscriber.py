"""
Test case to validate pubsub app functionality
"""
from subscriber.app.tweet_subscriber import *


# Scenario: Check the sentiment classification
def test_sentiment_classification():
    """
    Test case to verify sentiment classification.
    :return:
    """
    expected_sentiment = ['Clearly Negative', 'Clearly Negative', 'Clearly Negative', 'Clearly Negative',
                          'Clearly Negative', 'Clearly Negative', 'Clearly Negative', 'Clearly Negative',
                          'Clearly Negative', 'Clearly Negative', 'Clearly Negative', 'Mixed', 'Neutral',
                          'Clearly Positive', 'Clearly Positive', 'Clearly Positive', 'Clearly Positive',
                          'Clearly Positive', 'Clearly Positive', 'Clearly Positive', 'Clearly Positive',
                          'Clearly Positive']
    actual_sentiment = []
    for score in [-1.0, -0.9, -0.8, -0.7, -0.6, -0.7, -0.5, -0.4, -0.3, -0.2, -0.1, 0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6,
                  0.7, 0.8, 0.9, 1.0]:
        actual_sentiment.append(classify_sentiment(score))

    # TEST: check if the sentiment classification generates the same classification text for each score in accordance
    # to our assumption presented in expected_sentiment
    assert expected_sentiment == actual_sentiment


# Scenario: Check publish metrics to dashboard
def test_send_to_dashboard():
    """
    Test case to verify publishing metrics to dashboard
    :return:
    """
    aggregated_result = {'Clearly Positive': 1, 'Clearly Negative': 1, 'Mixed': 1, 'Neutral': 1}
    response = requests.Response()
    response.status_code = 201
    post_request_data = dict(data='[1, 1, 1, 1]', label= "['Mixed', 'Neutral', 'Clearly Positive', 'Clearly Negative']")
    flexmock(requests).should_receive('post').with_args(url=WEB_APP_UPDATE_URL, data=post_request_data).\
        and_return(response)

    # TEST: check if the send_to_dashboard returns 201 if an aggregated sentiment summary is passed to the Flask APP
    assert send_to_dashboard(aggregated_result).status_code == 201

    # TEST: check if the send_to_dashboard returns 400 if an aggregated sentiment summary is passed to the Flask APP
    response = requests.Response()
    response.status_code = 400
    flexmock(requests).should_receive('post').with_args(url=WEB_APP_UPDATE_URL, data={'data': '[]', 'label': '[]'}). \
        and_return(response)
    assert send_to_dashboard({}).status_code == 400


# Scenario: Check the result of Sentiment Analysis
def test_analyze_sentiment():
    """
    Test case to validate the results of sentiment Analysis API
    :return:
    """
    input_messages = ['I am happy', 'I am sad']
    expected_summary = {'Clearly Positive': [0], 'Clearly Negative': [1]}
    for input_msg in input_messages:
        analyze_sentiment(json.dumps({'id': input_messages.index(input_msg), 'text': input_msg}))
    assert expected_summary == TWEET_SUMMARY
