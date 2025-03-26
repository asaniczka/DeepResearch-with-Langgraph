"""
This module provides functionality for generating research queries,
retrieving research data, and summarizing it.
"""

import sys

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, chain
from langchain_core.runnables.passthrough import RunnablePick
from langchain_openai import ChatOpenAI
from wrapworks import cwdtoenv

cwdtoenv()

from src.crawlers.crawl_page import get_page
from src.crawlers.crawl_serp import get_serp
from src.models.research_models import SearchQueries
from src.parsers.page_cleaner import clean_html
from src.parsers.serp_parser import parse_serp_page
from src.prompts.generate_search_queries_prompt import SEARCH_QUERY_GENERATOR
from src.prompts.group_summerizer_prompt import SUMMERIZE_GROUP_PROMPT
from src.prompts.page_summerizer_prompt import SUMMERIZE_PAGE_PROMPT

LLM = ChatOpenAI(model="o3-mini")


STRUCTURED_LLM = LLM.with_structured_output(SearchQueries, method="json_mode")
QUERY_GENERATOR_CHAIN = (
    SEARCH_QUERY_GENERATOR
    | STRUCTURED_LLM
    | RunnableLambda(lambda x: x.model_dump())
    | RunnablePick(keys="search_queries")
)

GET_SERP_CHAIN = (
    get_serp | parse_serp_page | RunnableLambda(lambda x: [y.url for y in x[:2]])
)

PAGE_SUMMARY_CHAIN = (
    get_page | clean_html | SUMMERIZE_PAGE_PROMPT | LLM | StrOutputParser()
)

GROUP_SUMMARY_CHAIN = SUMMERIZE_GROUP_PROMPT | LLM | StrOutputParser()


@chain
def get_research(summarization_target: str) -> str:
    """
    Retrieve and summarize research data based on a specified target. Handles errors during the process.
    """
    try:
        queries = QUERY_GENERATOR_CHAIN.invoke(
            {"summarization_target": summarization_target}
        )

        serps = GET_SERP_CHAIN.batch(queries)

        page_urls = []
        for x in serps:
            page_urls.extend(x)

        summaries = PAGE_SUMMARY_CHAIN.batch(
            [
                {"url": x, "summarization_target": summarization_target}
                for x in page_urls
            ]
        )
        group_summary = GROUP_SUMMARY_CHAIN.invoke(
            {"summarization_target": summarization_target, "all_pages": summaries}
        )
        return group_summary
    except Exception as e:
        print(type(e), e)
        return f"Chain Failed with type e {type(e)} and e: {e}"


if __name__ == "__main__":

    if sys.argv > 1:
        query = sys.argv[0]
    else:
        query = "what is snowflake used for"
    get_research.invoke(query)
