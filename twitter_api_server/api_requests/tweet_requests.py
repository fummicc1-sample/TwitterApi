from pydantic import BaseModel


class StartStreamItemBody(BaseModel):
    word: str

class SearchBuzzItemBody(BaseModel):
    word: str