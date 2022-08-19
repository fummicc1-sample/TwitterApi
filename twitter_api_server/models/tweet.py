from typing import List, Optional

from .tweet_stream_rule import TweetStreamRule


class Tweet:
    id: int
    text: str
    rules: List[TweetStreamRule] = []
    favorite_count: Optional[int] = None

    def __init__(self, id: int, text: str, rules: List[TweetStreamRule] = [], favorite_count: Optional[int]=None):
        self.id = id
        self.text = text
        self.rules = rules
        self.favorite_count = favorite_count