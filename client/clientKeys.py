import os

class ClientKeys():

    def __init__(self):
        self.consumer_token =        os.environ['CONSUMER_TOKEN']
        self.consumer_secret =       os.environ['CONSUMER_SECRET']
        self.access_key =            os.environ['ACCESS_KEY']
        self.access_secret =         os.environ['ACCESS_SECRET']

    def get_consumer_token(self):
        """Returns Twitter consumer token"""
        return self.consumer_token

    def get_consumer_secret(self):
        """Returns Twitter consumer secret"""
        return self.consumer_secret

    def get_access_key(self):
        """Returns Twitter access key"""
        return self.access_key

    def get_access_secret(self):
        """Returns Twitter access secret"""
        return self.access_secret