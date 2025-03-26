import json

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, BaseMessage, ToolMessage
from langchain_openai.output_parsers import PydanticToolsParser
from langgraph.graph import END, MessageGraph
from pydantic import ValidationError
from rich import print
from wrapworks import cwdtoenv

cwdtoenv()
load_dotenv()

from src.chains.ai_message_to_str import AI_MESSAGE_TO_STR
from src.chains.research_controller import RESEARCH_CONTROLLER_CHAIN
from src.chains.research_queries import get_research
from src.models.research_models import ResearchExtentionTopics

PYDANTIC_PARSER = PydanticToolsParser(tools=[ResearchExtentionTopics])

CONTROLLER = "controller"
RESEACH_CRAWLER = "research_crawler"


def tool_executor(state: list[BaseMessage]) -> ToolMessage:
    message: AIMessage = state[-1]
    parsed_message: ResearchExtentionTopics = PYDANTIC_PARSER.invoke(message)[0]

    tool_call_id = message.additional_kwargs["tool_calls"][0]["id"]

    researches = get_research.batch(parsed_message.new_topics_to_research)
    return ToolMessage(content=json.dumps(researches), tool_call_id=tool_call_id)


def what_to_do(state: list[BaseMessage]) -> str:

    last_message: AIMessage = state[-1]
    try:
        parsed_message: ResearchExtentionTopics = PYDANTIC_PARSER.invoke(last_message)[
            0
        ]
        return RESEACH_CRAWLER
    except (ValueError, ValidationError, IndexError):
        return END


BUILDER = MessageGraph()
BUILDER.add_node(RESEACH_CRAWLER, tool_executor)
BUILDER.add_node(CONTROLLER, RESEARCH_CONTROLLER_CHAIN)
BUILDER.set_entry_point(CONTROLLER)
BUILDER.add_conditional_edges(CONTROLLER, what_to_do, [RESEACH_CRAWLER, END])
BUILDER.add_edge(RESEACH_CRAWLER, CONTROLLER)

GRAPH = BUILDER.compile()


if __name__ == "__main__":

    GRAPH.get_graph().draw_mermaid_png(
        output_file_path="resources/graphics/research_graph.png"
    )
    r = GRAPH.invoke("Scala vs Java")
    print(AI_MESSAGE_TO_STR.invoke(r))
