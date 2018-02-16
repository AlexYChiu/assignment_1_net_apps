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
from cryptography.fernet import Fernet
import hashlib
import pickle
from gtts import gTTS

import clientKeys


def checkpoint(message):
    """Prints [Checkpoint] <message>"""
    print("[Checkpoint] {}".format(message))


def speak(message):
    """Speaks given message"""
    checkpoint("Speaking: {}".format(message))

    tts = gTTS(text=message, lang='en')
    tts.save("./saythis.mp3")
    os.system("mplayer ./saythis.mp3 > /dev/null 2>&1")


def process_response(data):
    """Processes received data"""
    # Print received data
    checkpoint("Received data: {}".format(data))

    response = pickle.loads(data)

    # Check checksum
    temp = hashlib.md5()
    temp.update(response[1])
    md5 = temp.digest()

    # Checkpoint for md5
    if md5 == response[2]:
        checkpoint("Checksum is VALID")
    else:
        checkpoint("Checksum is INVALID")

    # Decrypt response
    key = response[0]
    cipher_suite = Fernet(key)
    plaintext = cipher_suite.decrypt(response[1])
    checkpoint("Decrypt: Using Key: {} | Plaintext: {}".format(key, plaintext))

    # Speak Answer
    speak(plaintext.decode())


def encrypt_data(data, key):
    """Encrypts data and returns key, ciphertext, and md5sum"""

    # Use cipher key to encrypt data
    cipher_suite = Fernet(key)
    # Defaults to utf-8
    bytedata = data.encode()
    ciphertext = cipher_suite.encrypt(bytedata)

    # Calculate the md5 of the ciphertext
    temp = hashlib.md5()
    temp.update(ciphertext)
    md5 = temp.digest()

    return ciphertext, md5


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
        checkpoint("New Tweet: {} | User: {}".format(status.text,
            status.user.screen_name))

        # Parse out hashtag
        question = status.text.replace(self.hashtag, '').strip()

        # Encrpytion
        key = Fernet.generate_key()
        ciphertext, md5 = encrypt_data(question, key)
        checkpoint("Encrypt: Generated Key: {} | Ciphertext: {}"
            .format(key, ciphertext))
        checkpoint("Generated MD5 Checksum: {}".format(md5))

        # Try to send query to server
        try:
            checkpoint("Connecting to {} on port {}"
                .format(self.host, self.port))

            # https://github.com/Microsoft/vscode/issues/39149#issuecomment-
            #    347260954
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.host,self.port))

            # Combine data
            dataTup = (key, ciphertext, md5)
            send_data = pickle.dumps(dataTup)

            # Send to server
            s.send(send_data)
            checkpoint("Sending data: {}".format(send_data))

            # Receive & process server response
            recv_data = s.recv(self.size)
            process_response(recv_data)

            s.close()

        except Exception as ex:
            print(ex)

def authenticate(consumer_key, consumer_secret, access_token, access_token_secret,
        host, port, size, hashtag):
    """Authenticates with Twitter and listens for hashtag"""
    # "Log in"
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # Start tracking the stream
    try:
        api = tweepy.API(auth)

        # Using info from http://docs.tweepy.org/en/v3.5.0/
        #   streaming_how_to.html
        myStreamListener = MyStreamListener(host=host, port=port,
            size=size, hashtag=hashtag)
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
    consumer_key = clientKeys.consumer_key
    consumer_secret = clientKeys.consumer_secret
    access_token = clientKeys.access_token
    access_token_secret = clientKeys.access_token_secret

    authenticate(consumer_key, consumer_secret, access_token, \
        access_token_secret, host, port, size, hashtag)

main()
