import os
from threading import Thread
from typing import List
from services.twitter_client import TwitterClient
from tweepy import StreamResponse

_twitter_client = TwitterClient(os.environ["TWITTER_API_BEARER_TOKEN"])


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
    _ = _twitter_client.start_listening(word, _on_response_tweet)