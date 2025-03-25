from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

LLM = ChatOpenAI(model="o3-mini")


class SearchQueries(BaseModel):
    search_queries: list[str]


SEARCH_QUERY_GENERATOR = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a google search query generator. When provided with a information goal, your task is to reply with 3-5 queries that would"
            " help discover information related to the infromation goal. A different agent willl go, search, and extract information based on"
            " queries provided by you. Each query shoudl not contain more than 3-6 words",
        ),
        (
            "user",
            "Here is what to focus on the query generation: {summarization_target}",
        ),
    ]
)

STRUCTURED_LLM = LLM.with_structured_output(SearchQueries, method="json_schema")
SUMMERIZER_CHAIN = SEARCH_QUERY_GENERATOR | STRUCTURED_LLM


if __name__ == "__main__":
    from rich import print

    res = SUMMERIZER_CHAIN.invoke({"summarization_target": "What is DBT used for"})
    print(res)
