import json
import marshal
import os
from pstats import StatsProfile
from threading import Thread
from typing import List

import tweepy.models
from tweepy import API, OAuth1UserHandler, StreamResponse, models

from models import Tweet
from services.twitter_client import TwitterClient

# Dependecnies
_twitter_client_v2 = TwitterClient(os.environ["TWITTER_API_BEARER_TOKEN"])
_twitter_client_v1_1 = API(
    OAuth1UserHandler(
        consumer_key=os.environ["TWITTER_CONSUMER_KEY"],
        consumer_secret=os.environ["TWITTER_CONSUMER_SECRET"],
        access_token=os.environ["TWITTER_ACCESS_TOKEN"],
        access_token_secret=os.environ["TWITTER_ACCESS_TOKEN_SECRET"]
    )
)

# Class
class TwitterController:
    global _twitter_client_v1_1, _twitter_client_v2 

    on_response_tweet = None   

    def _default_on_response_tweet(self, response: StreamResponse):
        tweet: Tweet = response.data
        print(tweet.id)

    def start_listening_word(self, word: str):
        on_response_tweet = self._default_on_response_tweet
        if self.on_response_tweet is not None:
            on_response_tweet = self.on_response_tweet
        _ = _twitter_client_v2.start_listening(word, on_response_tweet)

    def search_buzz_tweets(self, word: str) -> List[Tweet]:
        total = []
        try:
            # `SearchResult ~= List[models.Status]` response type
            popular: List[models.Status] = _twitter_client_v1_1.search_tweets(
                q=word,
                result_type="popular",
                lang="ja"
            )
            f = open("popular.json", "w")
            f.write("")
            f.close()
            arr = []
            for res in popular:
                twt = Tweet(res.id, res.text, [], res.favorite_count)
                with open("popular.json", "a") as file:
                    json.dump(res._json, file)
                arr.append(twt)
            total += arr
        except Exception as e:
            print(e)
        if total:
            return total
        try:
            # `List[models.Status]` response type
            response: List[models.Status] = _twitter_client_v1_1.search_full_archive(
                label="development",
                query=f"{word} lang:ja",
                maxResults=10
            )
            f = open("response.json", "w")
            f.write("")
            f.close()
            arr = []
            for res in response:
                twt = Tweet(id=res.id, text=res.text, rules=res.matching_rules, favorite_count=res.favorite_count)
                with open("response.json", "a") as file:
                    json.dump(res._json, file)
                arr.append(twt)
            total += arr
        except Exception as e:
            print(e)
        return total

    def did_find_buzz_tweet(self, tweet: Tweet):
        print("save suruyo!")
        print("tweet:", tweet)