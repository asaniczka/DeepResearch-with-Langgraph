from pydantic import BaseModel, Field


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


class ResearchExtentionTopics(BaseModel):
    what_is_the_goal_of_the_user: str
    what_information_are_missing_in_bundle: str
    new_topics_to_research: list[str] = Field(
        description="Each topic is atomic. One research topic won't have access to other topics. Each item should contain all info related to that."
        "Do not duplicate any previous tool call topics"
    )
