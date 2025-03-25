from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from wrapworks import cwdtoenv

from src.crawlers.crawl_serp import get_serp
from src.models.research_models import SearchQueries
from src.parsers.serp_parser import parse_serp_page
from src.prompts.generate_search_queries_prompt import SEARCH_QUERY_GENERATOR
from src.prompts.page_summerizer_prompt import SUMMERIZE_PAGE_PROMPT

cwdtoenv()

from src.crawlers.crawl_page import get_page
from src.parsers.page_cleaner import clean_html

LLM = ChatOpenAI(model="o3-mini")


STRUCTURED_LLM = LLM.with_structured_output(SearchQueries, method="json_schema")
QUERY_GENERATOR_CHAIN = SEARCH_QUERY_GENERATOR | STRUCTURED_LLM

GET_SERP_CHAIN = get_serp | parse_serp_page

PAGE_SUMMARY_CHAIN = (
    get_page | clean_html | SUMMERIZE_PAGE_PROMPT | LLM | StrOutputParser()
)


if __name__ == "__main__":
    r = PAGE_SUMMARY_CHAIN.invoke(
        {"url": "https://www.getdbt.com/", "summarization_target": "what is dbt"}
    )
    print(r)

    r = QUERY_GENERATOR_CHAIN.invoke({"summarization_target": "What is DBT used for"})
    print(r)
