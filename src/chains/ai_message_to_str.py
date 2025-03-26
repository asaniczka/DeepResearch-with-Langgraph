from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda

AI_MESSAGE_TO_STR = RunnableLambda(lambda x: x[-1]) | StrOutputParser()
