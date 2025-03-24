from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

SUMMERIZE_PAGE_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are page summerizer for a researcher. You'll be provided with the markdown page and the target information to extract in the summerizations. Reply back with a full summary and don't exclude any requried info. Maintain any related or important urls. Include citations",
        ),
        ("user", "Here is what to focus on the summerization: {summarization_target}"),
        ("user", "{page}"),
    ]
)

LLM = ChatOpenAI(model="o3-mini")

SUMMERIZER_CHAIN = SUMMERIZE_PAGE_PROMPT | LLM | StrOutputParser
