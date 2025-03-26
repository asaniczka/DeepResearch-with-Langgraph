from dotenv import load_dotenv
from langchain_core.messages import AIMessage, BaseMessage
from langchain_openai.output_parsers import PydanticToolsParser
from langgraph.graph import END, MessageGraph
from wrapworks import cwdtoenv

cwdtoenv()
load_dotenv()

from src.chains.research_controller import RESEARCH_CONTROLLER_CHAIN
from src.chains.research_queries import get_research
from src.models.research_models import ResearchExtentionTopics

PYDANTIC_PARSER = PydanticToolsParser(tools=[ResearchExtentionTopics])


CONTROLLER = "controller"
RESEACH_CRAWLER = "research_crawller"


def tool_executor(state: list[BaseMessage]) -> list:
    parsed_message: ResearchExtentionTopics = PYDANTIC_PARSER.invoke(state[-1])[0]

    print(parsed_message)
    researches = get_research.batch(parsed_message.topics_to_research)
    print(researches)
    return researches


def what_to_do(state: list[BaseMessage]) -> str:

    last_message: AIMessage = state[-1]
    try:
        parsed_message: ResearchExtentionTopics = PYDANTIC_PARSER.invoke(last_message)[
            0
        ]
        return RESEACH_CRAWLER
    except ValueError:
        return END


BUILDER = MessageGraph()
BUILDER.add_node(RESEACH_CRAWLER, tool_executor)
BUILDER.add_node(CONTROLLER, RESEARCH_CONTROLLER_CHAIN)
BUILDER.set_entry_point(CONTROLLER)
BUILDER.add_conditional_edges(CONTROLLER, what_to_do)
BUILDER.add_edge(RESEACH_CRAWLER, CONTROLLER)
BUILDER.add_edge(CONTROLLER, END)

GRAPH = BUILDER.compile()


if __name__ == "__main__":
    print(GRAPH.get_graph().draw_mermaid())
