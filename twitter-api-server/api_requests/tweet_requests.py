from pydantic import BaseModel


class StartStreamItemBody(BaseModel):
    word: str