from typing import Sequence

from langchain.tools import Tool
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_openai.output_parsers import JsonOutputToolsParser, PydanticToolsParser
from pydantic import BaseModel
from rich import print


class SearchQueries(BaseModel):
    missing_information: str
    search_queries: list[str]
    no_missing_info: bool


llm = ChatOpenAI(model="gpt-4o")
parser_json = JsonOutputToolsParser()
parser_pydantic = PydanticToolsParser(tools=[SearchQueries])


topic_analyser_template = ChatPromptTemplate(
    [
        (
            "system",
            "When provided with a topic or existing set of information, figure out what information is missinge and suggest some search queries to help find the missing information. If not information is missing, set no_missing_info to True",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

essay_generator_template = ChatPromptTemplate(
    [
        (
            "system",
            "Based on the provided info, please write a detailed response to the user on the requested topic. You'll see multiple chat messages, these are info provided by different agents to help to write the final answer",
        )
    ]
)


def travality_search(query: str):
    tool = TavilySearchResults()
    res = tool.invoke(query)
    return {"query": query, "result": res}


travily_executor = Tool(name="", description="", func=travality_search)
topic_analyser = "topic_analyser"
ESSAY = "essay"


def invoke_tools(state: Sequence[BaseMessage]):

    tool_requests: AIMessage = state[-1]
    parsed_tool_calls = parser_json.invoke(tool_requests)

    queries = []
    for tool_call in parsed_tool_calls:
        for query in tool_call["args"]["search_queries"]:
            queries.append(query)

    return travily_executor.batch(queries)


def what_to_do(state: Sequence[BaseMessage]) -> str:

    return ESSAY


topic_analyser = topic_analyser_template | llm.bind_tools(
    tools=[SearchQueries], tool_choice="SearchQueries"
)
essay_writer = essay_generator_template | llm

if __name__ == "__main__":
    human_message = HumanMessage(
        content="THE TOPIC I WANT INFO ABOUT is: What is Databricks and what are some opensource alternatives to it"
    )

    res = topic_analyser.invoke({"messages": [human_message]})
    print(res)
    r2 = invoke_tools([res])
    print(r2)
