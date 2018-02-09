"""Holds MyStreamListner class."""

import tweepy
from tweepy.api import API

class MyStreamListener(tweepy.StreamListener):
    '''Overides Tweepy's StreamListener 
        |
        --> https://github.com/tweepy/tweepy/blob/c8e473ed7b939e09a485d0eaa2390554f009a56b/tweepy/streaming.py
    '''
    
    def __init__(self, hashtag):
       self.hashtags = [hashtag]
       super().__init__()                       # Keep this, needed for status = Status.parse(self.api, data) (in our case)
       print('Started status streaming...')

    def on_status(self, status):
        """Prints incoming statuses with hashtag ommitted"""
        tweet_words = status.text.encode('utf8').split()
        question_words = [word for word in tweet_words if word not in self.hashtags]
        question = ' '.join(word.decode('utf-8') for word in question_words)
        print('Question: ' + str(question))
