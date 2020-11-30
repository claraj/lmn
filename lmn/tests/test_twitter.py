# from django.test import TestCase
# import mock
# from ..twitter import tweet_note, authorize, post_tweet
# import tweepy


# class MockTweepyObj(object):
#     def __init__(self, auth):
#         self.api = tweepy.API(auth)
#     def post_tweet(self, status):
#         self.api.update_status(status)


# class TestTweepyErrorChecking(TestCase):

#     @mock.patch.object(tweepy.API, 'update_status')
#     def test_tweet_made_successfully(self):
#         test = TwitterPost("fake auth")
#         ta.post_tweet("test tweet")
#         mock_update_status.assert_called_with("test tweet")