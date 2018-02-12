#!/usr/bin/env python3

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

from clientKeys import ClientKeys


def checkpoint(message):
    """Prints [Checkpoint] <message>"""
    print("[Checkpoint] {}".format(message))

def speak(message):
    """Speaks given message"""
    checkpoint("Speaking: {}".format(message))

def process_response(data):
    """Processes received data"""
    # Print received data
    checkpoint("Received data: {}".format(data))

    # TODO check checksum
    md5 = "TODO"
    checkpoint("Checksum is {}".format(md5))

    # TODO Decrypt
    key = "TODO"
    plaintext = "TODO"
    checkpoint("Decrypt: Using Key: {} | Plaintext: {}".format(key, plaintext))

    # TODO Speak Answer
    speak(plaintext)

def encrypt_data(data):
    """Encrypts data and returns key, ciphertext, and md5sum"""
    key = "TODO"
    ciphertext = "TODO"
    md5 = "TODO"

    return key, ciphertext, md5


class MyStreamListener(tweepy.StreamListener):
    """Overides Tweepy's StreamListener 
        https://github.com/tweepy/tweepy/blob/c8e473ed7b939e09a485d0eaa2390554
        f009a56b/tweepy/streaming.py
    """ 
    
    def __init__(self, host, port, size, hashtag):
        """See https://github.com/tweepy/tweepy/blob/c8e473ed7b939e09a485d0eaa
            2390554f009a56b/tweepy/streaming.py
        """
        self.host = host
        self.port = port
        self.size = size
        self.hashtag = hashtag
        # Keep this, needed for status = Status.parse(self.api, data)
        super().__init__()

    def on_status(self, status):
        """Send query to server and receive answer """
        checkpoint("New Tweet: {} | User: {}".format(status.text, status.user.name))

        # Parse out hashtag
        question = status.text.replace(self.hashtag, '').strip()

        # TODO Need to add encrpytion
        key, ciphertext, md5 = encrypt_data(question)
        checkpoint("Encrypt: Generated Key: {} | Ciphertext: {}".format(key, ciphertext))
        checkpoint("Generated MD5 Checksum: {}".format(md5))
        
        # Try to send query to server
        try:
            checkpoint("Connecting to {} on port {}".format(self.host, self.port))

            # https://github.com/Microsoft/vscode/issues/39149#issuecomment-
            #    347260954
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.host,self.port))
      
            # Send to server
            send_data = bytearray()
            send_data.extend(map(ord, question))
            s.send(send_data)
            checkpoint("Sending data: {}".format(send_data))
            
            # Receive & process server response
            recv_data = s.recv(self.size)
            process_response(recv_data)

            s.close() 

        except Exception as ex:                                                              
            print(ex)  

def authenticate(consumer_token, consumer_secret, access_key, access_secret,
        host, port, size, hashtag):
    """Authenticates with Twitter and listens for hashtag"""
    # "Log in"
    auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
    auth.set_access_token(access_key, access_secret)

    # Start tracking the stream
    try:
        api = tweepy.API(auth)

        # Using info from http://docs.tweepy.org/en/v3.5.0/
        #   streaming_how_to.html
        myStreamListener = MyStreamListener(host=host, port=port, size=size, hashtag=hashtag)
        myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)

        # Start listening for tweets with given hashtag
        # If we want a separate thread, add ", async=True" after track_list
        myStream.filter(track=[hashtag])
    
    except KeyboardInterrupt:
        print('Keyboard interrupt')
        sys.exit(0)

def main():
    """Main function to manage the client"""
    # Parse command line args
    parser = argparse.ArgumentParser(description='Processes arguments')
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

    # Copy args into vars
    try:
        hashtag = args.t
        host = args.s
        size = int(args.z)
        port = int(args.p)
    
    except Exception as ex:
        print(ex)
        sys.exit(1)

    checkpoint("Listening for Tweets that contain: {}".format(hashtag))
    
    # Get needed information for authorization
    api_keys = ClientKeys() 
    consumer_token = api_keys.get_consumer_token()
    consumer_secret = api_keys.get_consumer_secret()
    access_key = api_keys.get_access_key()
    access_secret = api_keys.get_access_secret()

    authenticate(consumer_token, consumer_secret, access_key, \
        access_secret, host, port, size, hashtag)

main()
