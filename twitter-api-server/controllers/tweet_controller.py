import json
import marshal
import os
from pstats import StatsProfile
from threading import Thread
from typing import List
from services.twitter_client import TwitterClient
import tweepy
from tweepy import StreamResponse, OAuth1UserHandler, API, models

_twitter_client_v2 = TwitterClient(os.environ["TWITTER_API_BEARER_TOKEN"])
_twitter_client_v1_1 = API(
    OAuth1UserHandler(
        consumer_key=os.environ["TWITTER_CONSUMER_KEY"],
        consumer_secret=os.environ["TWITTER_CONSUMER_SECRET"],
        access_token=os.environ["TWITTER_ACCESS_TOKEN"],
        access_token_secret=os.environ["TWITTER_ACCESS_TOKEN_SECRET"]
    )
)

class TweetStreamRule:
    id: int

class Tweet:
    id: int
    text: str
    rules: List[TweetStreamRule]


def _on_response_tweet(response: StreamResponse):
    tweet: Tweet = response.data
    print(tweet.id)

def start_listening_word(word: str):
    _ = _twitter_client_v2.start_listening(word, _on_response_tweet)

def search_buzz_tweets(word: str) -> List:
    total = []
    try:
        popular: List = _twitter_client_v1_1.search_tweets(
            q=word,
            result_type="popular",
            lang="ja"
        )
        f = open("popular.json", "w")
        f.write("")
        f.close()
        for res in popular:
            with open("popular.json", "a") as file:
                json.dump(res._json, file)
        total += popular
    except Exception as e:
        print(e)
    try:
        response: List = _twitter_client_v1_1.search_full_archive(
            label="development",
            query=word,
            maxResults=10
        )
        f = open("response.json", "w")
        f.write("")
        f.close()
        for res in response:
            with open("response.json", "a") as file:
                json.dump(res._json, file)
        total += response
    except Exception as e:
        print(e)
    return total

