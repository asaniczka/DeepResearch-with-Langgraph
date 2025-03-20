from pydantic import BaseModel


class SerpResult(BaseModel):
    url: str
    title: str
    description: str
    rank: int
