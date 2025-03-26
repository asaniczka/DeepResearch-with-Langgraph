from langchain_openai import ChatOpenAI

from src.models.research_models import ResearchExtentionTopics
from src.prompts.research_controller_prompt import RESEARCH_CONTROLLER_PROMPT

LLM = ChatOpenAI(model="o3-mini", reasoning_effort="high")


RESEARCH_CONTROLLER_CHAIN = RESEARCH_CONTROLLER_PROMPT | LLM.bind_tools(
    tools=[ResearchExtentionTopics]
)
