"""Holds MyStreamListner class."""

import tweepy

class MyStreamListener(tweepy.StreamListener):
    '''Overides Tweepy's StreamListener 
        |
        --> https://github.com/tweepy/tweepy/blob/c8e473ed7b939e09a485d0eaa2390554f009a56b/tweepy/streaming.py
    '''
    
    '''
    def __init__(self, hashtag):
       self.hashtags = [hashtag]
       print('Hashtag 2:' + hashtag)
    '''

    def on_status(self, status):
        """Prints incoming statuses with hashtag ommitted"""
        #tweet_words = status.text.encode('utf8').split()
        #question_words = [word for word in tweet_words if word not in self.hashtags]
        #question = ' '.join(question_words)
        #print(question)
        print(status.text.encode('utf8'))  # simple printing of tweet text
