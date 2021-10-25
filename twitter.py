'''
@author: Souvik Das
Institute: University at Buffalo
'''

import tweepy
import requests
import json
import collections
import time

class Twitter:
    def __init__(self):
        self.auth = tweepy.OAuthHandler("BpO0ya2w3qXn0RCRdqjfjy8K4", "A6Jex6tMiXMdwd7SHa6M4oZtaL8rJwSDhapIt1lE5vvnQuRO5N")
        self.auth.set_access_token("1432452858348244999-BjIWNdfCLObUCGf085MegSPHrB6tHY", "ZYfxMwKeTLv6OirrUaoedDfXHuzZ8ReSQoIel5aXQLbPg")
        self.api = tweepy.API(self.auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    def _meet_basic_tweet_requirements(self):
        '''
        Add basic tweet requirements logic, like language, country, covid type etc.
        :return: boolean
        '''
        raise NotImplementedError

    def get_tweets_by_poi_screen_name(self, name, count):
        '''
        Use user_timeline api to fetch POI related tweets, some postprocessing may be required.
        :return: List
        '''
        tweets = []
        api = self.api
        for tweet in tweepy.Cursor(api.user_timeline, screen_name=name,count=100, tweet_mode="extended", include_rts=False).items(count):
            tweets.append(tweet)
        return tweets
            #print(tuit.text)

    def get_tweets_by_lang_and_keyword(self, keyword, count, lang):
        '''
        Use search api to fetch keywords and language related tweets, use tweepy Cursor.
        :return: List
        '''
        tweets = []
        api = self.api
        search_word = keyword + " -filter:retweets"
        for tweet in tweepy.Cursor(api.search, q=search_word, count=100, lang=lang, tweet_mode="extended").items(count):
            tweets.append(tweet)
        return tweets


    def bearer_oauth(self, r):
        bearer_token = "AAAAAAAAAAAAAAAAAAAAAB65TgEAAAAAPEYeY6B0HoMnkAxjTD4fckegEsc%3DhkFTEcDQho79cWygNZQZVa4UwYl8F6hHkVx2RBMzCxREpCXDKr"
        r.headers["Authorization"] = f"Bearer {bearer_token}"
        return r

    def connect_to_endpoint(self, url, params):
        response = requests.get(url, auth=self.bearer_oauth, params=params)
        print(response.status_code)
        if response.status_code != 200:
            raise Exception(response.status_code, response.text)
        return response.json()

    def get_replies(self, tweet_ids, name):
        '''
        Get replies for a particular tweet_id, use max_id and since_id.
        For more info: https://developer.twitter.com/en/docs/twitter-api/v1/tweets/timelines/guides/working-with-timelines
        :return: List
        '''
        api = self.api
        replies = []
        #count = 1
        for tweet in tweepy.Cursor(api.search, q='to:'+name, result_type='recent', tweet_mode="extended", include_rts=False, timeout=999999).items(1000):
            if not hasattr(tweet, 'retweeted_status'):
                replies.append(tweet)
            # conversation = "conversation_id:"+id
            # query_params = {'query': conversation, 'tweet.fields': 'id'}
            # search_url = "https://api.twitter.com/2/tweets/search/recent"
            # json_response = self.connect_to_endpoint(search_url, query_params)
            # print(json_response)
            # if "data" in json_response:
            #     for response in json_response['data']:
            #         tweet = api.get_status(response['id'], tweet_mode="extended", include_rts=False)
            #         if not hasattr(tweet, 'retweeted_status'):
            #             replies.append(tweet)
            #             if len(replies) > 100:
            #                 return replies
        return replies
