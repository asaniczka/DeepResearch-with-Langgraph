"""
Module to define Pydantic models for research-related data structures.
"""

from pydantic import BaseModel, Field


class SerpResult(BaseModel):
    """
    Represents a search engine results page entry.

    Attributes:
    - url: The URL of the result.
    - title: The title of the result.
    - description: A brief description of the result.
    - rank: The rank of the result in the search results.
    """

    url: str
    title: str
    description: str
    rank: int


class PageCrawlResult(BaseModel):
    """
    Represents the result of a web page crawl.

    Attributes:
    - url: The URL of the crawled page.
    - page: The content of the crawled page.
    """

    url: str
    page: str


class SearchQueries(BaseModel):
    """
    Represents a collection of search queries. Used to store and manage a list of search strings for querying purposes.
    """

    search_queries: list[str]


class ResearchExtentionTopics(BaseModel):
    """
    Defines topics for further research based on user goals and information gaps.
    It helps structure atomic research themes, ensuring each topic is self-contained and unique.
    """

    what_is_the_goal_of_the_user: str
    what_information_are_missing_in_bundle: str
    query_for_crawler: list[str] = Field(
        description="Only a maximum of 1 item is supported"
    )
