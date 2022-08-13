import threading
import tweepy


class _MyStreamingClient(tweepy.StreamingClient):
    def __init__(self, bearer_token, *, return_type=..., wait_on_rate_limit=False, **kwargs):
        super().__init__(bearer_token, return_type=return_type, wait_on_rate_limit=wait_on_rate_limit, **kwargs)

    def register_on_response_handler(self, handler):
        self.handler = handler

    def on_response(self, response):
        self.handler(response)
        return super().on_response(response)



class TwitterClient:
    def __init__(self, bearer_token: str):                
        self.client = tweepy.Client(bearer_token)
        self.streaming_client = _MyStreamingClient(bearer_token)

    def start_listening(self, word: str, on_response) -> threading.Thread:
        rule = tweepy.StreamRule(value=f"{word} lang:ja")
        self.streaming_client.add_rules([rule])
        self.streaming_client.register_on_response_handler(on_response)
        return self.streaming_client.filter()