"""
    Client side of Assignment 1 for ECE 4564. 
    Handles:
    1. Capturing tweet given hashtag argument.
    2. Sending question from tweet to server. 
    3. Speaks Answer from server. 
"""

import sys
import argparse
import os
import socket

import tweepy
from tweepy.api import API

from clientKeys import ClientKeys

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
        tweet_words = status.text.split()
        print(tweet_words)
        question_words = [str(word) for word in tweet_words if word not in self.hashtags]
        question = ' '.join(word for word in question_words)
        try:
            print('Question: ' + str(question.encode('utf8')))                              # this sometimes throws an OSError on Windows... microsoft can't hang.
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                           # https://github.com/Microsoft/vscode/issues/39149#issuecomment-347260954
            s.connect((host,port))
            
            # Need to add encrpytion

            b = bytearray()
            b.extend(map(ord, question))
            s.send(b)
            data = s.recv(size)
            s.close() 
            print ('Received:', data) 

        except Exception as ex:                                                              
            print(ex)  

parser = argparse.ArgumentParser(description='Prossesses arguments for client.')
parser.add_argument('-s', help='Set the server ip address.')
parser.add_argument('-p', help='Set the server port.')
parser.add_argument('-z', help='Set the socket size')
parser.add_argument('-t', help='Set the hashtag being searched.')

args = parser.parse_args()

if args.s == None:
    print('Please set server ip address with the -s flag.')
    sys.exit(1)
if args.p == None:
    print('Please set server port with the -p flag.')
    sys.exit(1)
if args.z == None:
    print('Please set socket size with the -z flag.')
    sys.exit(1)
if args.t == None:
    print('Please set hastag with the -t flag.')
    sys.exit(1)

try:
    hashtag = args.t
    host = args.s
    size = int(args.z)
    port = int(args.p)
except Exception as ex:
    print(ex)
    sys.exit(1)

track_list = []
track_list.append(hashtag)

# Get needed information for authorization from environment variables
api_keys = ClientKeys() 
consumer_token = api_keys.get_consumer_token()
consumer_secret = api_keys.get_consumer_secret()
access_key = api_keys.get_access_key()
access_secret = api_keys.get_access_secret() 

auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
auth.set_access_token(access_key, access_secret)

try:
    api = tweepy.API(auth)

    # Using info from http://docs.tweepy.org/en/v3.5.0/streaming_how_to.html
    myStreamListener = MyStreamListener(hashtag=hashtag)
    myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)

    myStream.filter(track=track_list)   # if we want a separate thread, add ", async=True" after track_list

except KeyboardInterrupt:
    print('Keyboard interrupt')
    sys.exit(0)