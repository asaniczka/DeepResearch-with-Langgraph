from typing import Sequence

from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langgraph.graph import END, MessageGraph
from rich import print

reflection_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are twitter message optimizer. Generate critique and recommendations for the users tweets. "
            "Include recommendation on the length, virality, style and other stuff",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)


genetation_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "Based on the provided recommendations, Improve the original tweet"),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

llm = ChatOpenAI(model="gpt-4o")

generation_chain = genetation_prompt | llm
reflection_chain = reflection_prompt | llm

REFLECT = "reflect"
GENERATE = "generate"


def generation_node(state: Sequence[BaseMessage]) -> BaseMessage:
    return generation_chain.invoke({"messages": state})


def reflection_node(state: Sequence[BaseMessage]) -> BaseMessage:
    res = reflection_chain.invoke({"messages": state})
    return [HumanMessage(content=res.content)]


def should_continue(state: Sequence[BaseMessage]) -> str:
    if len(state) > 6:
        return END
    return REFLECT


builder = MessageGraph()
builder.add_node(GENERATE, generation_node)
builder.add_node(REFLECT, reflection_node)

builder.set_entry_point(GENERATE)
builder.add_conditional_edges(GENERATE, should_continue)
builder.add_edge(REFLECT, GENERATE)

graph = builder.compile()
if __name__ == "__main__":
    print(graph.get_graph().draw_mermaid())

    res = graph.invoke(HumanMessage(content="I'm new to twitter. Not liking it so far"))
    print(res)
