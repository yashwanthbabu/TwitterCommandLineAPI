import twitter
import os
import sys
import re
import json


class TwitterCommandLineAPI(object):

    def __init__(self):
        consumer_key = None
        consumer_secret = os.environ.get('CONSUMER_SECRET')
        access_token = os.environ.get('ACCESS_TOKEN')
        access_secret_token = os.environ.get('ACCESS_SECRET_TOKEN')

        # read the credentials from text file if exists
        json_file = open('credentials.txt', 'a+')
        json_data = json_file.read()

        # Enter the access tokens if no token exists
        if not consumer_key or not consumer_secret or \
           not access_token or not access_secret_token:
            if json_data:
                credentials = json.loads(json_data)
                consumer_key = credentials['consumer_key']
                consumer_secret = credentials['consumer_secret']
                access_token = credentials['access_token']
                access_secret_token = credentials['access_secret_token']
            else:
                consumer_key = raw_input("please enter your"
                                         "twitter consumer key")
                consumer_secret = raw_input("Please enter your"
                                            "twitter consumer secret")
                access_token = raw_input("Please enter your"
                                         "twitter access token")
                access_secret_token = raw_input("Please enter your"
                                                "twitter access secret token")

        # Twitter api initialization
        self.api = twitter.Api(consumer_key=consumer_key,
                               consumer_secret=consumer_secret,
                               access_token_key=access_token,
                               access_token_secret=access_secret_token)

        # if no credentials, create and store in a text file
        if not json_data:
            self.api.VerifyCredentials()
            json_data = {'consumer_key': consumer_key,
                         'consumer_secret': consumer_secret,
                         'access_token': access_token,
                         'access_secret_token': access_secret_token}
            json_str = json.dumps(json_data)
            json_file.write(json_str)
        json_file.close()

    # Displays all the list of friends
    def show_friends_list(self):
        friends_list = self.api.GetFriends()
        print friends_list
        for friend in friends_list:
            print friend.name

    def timeline_tweets(self, tweet_number):
        tweets = self.api.GetHomeTimeline(count=10)
        print len(tweets)

if __name__ == '__main__':
    twitter_command_line_api = TwitterCommandLineAPI()
    try:
        twitter_command_line_api.api.VerifyCredentials()

        tweet_number = re.match('\d+', sys.argv[1])

        if tweet_number:
            tweet_number = tweet_number.group(0)
            twitter_command_line_api.timeline_tweets(tweet_number)

        # python twitter_command_line_api.py list_of_friends
        # The above command will display list of friends
        if sys.argv[1] == 'list_of_friends':
            twitter_command_line_api.show_friends_list()

    except twitter.TwitterError as errors:
        print errors.message[0]['message']
