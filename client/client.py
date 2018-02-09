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

import tweepy

from my_stream_listener import MyStreamListener

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

hashtag = args.t

# Get needed information for authorization from environment variables
consumer_token =        os.environ['CONSUMER_TOKEN']
consumer_secret =       os.environ['CONSUMER_SECRET']
access_key =            os.environ['ACCESS_KEY']
access_secret =         os.environ['ACCESS_SECRET']

auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
auth.set_access_token(access_key, access_secret)

api = tweepy.API(auth)

# Testing to make sure valid connection to Twitter, will fail if keys, etc. not working
user = 'theasianchris1'
api.get_user(user)
# End Testing

# Using info from http://docs.tweepy.org/en/v3.5.0/streaming_how_to.html
myStreamListener = MyStreamListener(hashtag=hashtag)
myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)

track_list = []
track_list.append(hashtag)

myStream.filter(track=track_list)   # if we want a separate thread, add async=True

print('Finished')