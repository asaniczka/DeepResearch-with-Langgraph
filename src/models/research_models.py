from pydantic import BaseModel


class SerpResult(BaseModel):
    url: str
    title: str
    description: str
    rank: int


class PageCrawlResult(BaseModel):
    url: str
    page: str


class SearchQueries(BaseModel):
    search_queries: list[str]
