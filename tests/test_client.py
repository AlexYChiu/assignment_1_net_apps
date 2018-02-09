import unittest
import os

import tweepy

class TestClient(unittest.TestCase):

    def test_twitter_api_connection(self):
        consumer_token =        os.environ['CONSUMER_TOKEN']
        consumer_secret =       os.environ['CONSUMER_SECRET']
        access_key =            os.environ['ACCESS_KEY']
        access_secret =         os.environ['ACCESS_SECRET']

        auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
        auth.set_access_token(access_key, access_secret)

        api = tweepy.API(auth)
        user = 'theasianchris1'
        api.get_user(user)

if __name__ == '__main__':
    unittest.main()