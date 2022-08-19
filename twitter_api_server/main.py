from dotenv import load_dotenv
from fastapi import FastAPI
from tweepy import StreamResponse
from tweepy.models import Status

from api_requests.tweet_requests import SearchBuzzItemBody, StartStreamItemBody
from models.tweet import Tweet

app = FastAPI()

load_dotenv()

from controllers import TwitterController

twitter_controller = TwitterController()

@app.get("/")
def root():
    return "Hello World!"


@app.post("/stream")
def start_stream(body: StartStreamItemBody):

    def on_response(response: StreamResponse):
        twitter_controller.did_find_buzz_tweet(response.data)


    twitter_controller.on_response_tweet = on_response
    try:        
        twitter_controller.start_listening_word(body.word)
    except Exception as err:
        print(err)
    return "Succeed!"


@app.post("/search/buzz")
def search_buzz(body: SearchBuzzItemBody):
    results = twitter_controller.search_buzz_tweets(body.word)    
    return {
        "tweets": results
    }