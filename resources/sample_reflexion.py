import json
from typing import Sequence

from langchain.tools import Tool
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import AIMessage, BaseMessage, ToolMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_openai.output_parsers import JsonOutputToolsParser, PydanticToolsParser
from langgraph.graph import END, MessageGraph
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
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)


def travality_search(query: str):
    tool = TavilySearchResults()
    res = tool.invoke(query)
    return {"query": query, "result": res}


travily_executor = Tool(name="", description="", func=travality_search)
TOPIC_ANALYSER = "topic_analyser"
ESSAY_WRITER = "essay_writer"
ONLINE_SEARCH = "online_search"
MAX_ITERATIONS = 2


def invoke_tools(state: Sequence[BaseMessage]) -> list:

    tool_requests: AIMessage = state[-1]
    print(tool_requests)
    parsed_tool_calls = parser_json.invoke(tool_requests)

    call_id = tool_requests.additional_kwargs["tool_calls"][0]["id"]
    queries = []
    for tool_call in parsed_tool_calls:
        for query in tool_call["args"]["search_queries"]:
            queries.append(query)

    results = travily_executor.batch(queries)
    return ToolMessage(content=json.dumps(results), tool_call_id=call_id)


def what_to_do(state: list[BaseMessage]) -> str:

    last_message: AIMessage = state[-1]
    parsed_message: SearchQueries = parser_pydantic.invoke(last_message)[0]

    if len(state) > 10 or parsed_message.no_missing_info:
        return ESSAY_WRITER

    return ONLINE_SEARCH


def state_cleaner(state: list[BaseMessage]) -> list[BaseMessage]:
    state.pop()
    return state


topic_analyser = topic_analyser_template | llm.bind_tools(
    tools=[SearchQueries], tool_choice="SearchQueries"
)
essay_writer = state_cleaner | essay_generator_template | llm


builder = MessageGraph()
builder.add_node(TOPIC_ANALYSER, topic_analyser)
builder.add_node(ONLINE_SEARCH, invoke_tools)
builder.add_node(ESSAY_WRITER, essay_writer)
builder.set_entry_point(TOPIC_ANALYSER)
builder.add_conditional_edges(TOPIC_ANALYSER, what_to_do)
builder.add_edge(ONLINE_SEARCH, TOPIC_ANALYSER)
builder.add_edge(ESSAY_WRITER, END)


if __name__ == "__main__":

    print(builder.compile().get_graph().draw_mermaid())

    graph = builder.compile()
    res = graph.invoke(
        "List out all tools,frameworks, langauges used by data engineers at atlassian"
    )

    print(res)
