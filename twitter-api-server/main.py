from typing import Union
from fastapi import FastAPI
from dotenv import load_dotenv
from api_requests.tweet_requests import StartStreamItemBody

app = FastAPI()

load_dotenv()

from controllers import tweet_controller

@app.get("/")
def root():
    return "Hello World!"


@app.post("/stream/start")
def start_stream(body: StartStreamItemBody):
    try:
        tweet_controller.start_listening_word(body.word)
    except Exception as err:
        print(err)
    return "Succeed!"
