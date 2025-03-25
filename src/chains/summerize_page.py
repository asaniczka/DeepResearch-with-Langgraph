from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from wrapworks import cwdtoenv

cwdtoenv()

from src.crawlers.crawl_page import get_page
from src.parsers.page_cleaner import clean_html

LLM = ChatOpenAI(model="o3-mini")

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


SUMMERIZER_CHAIN = (
    get_page | clean_html | SUMMERIZE_PAGE_PROMPT | LLM | StrOutputParser()
)

if __name__ == "__main__":
    r = SUMMERIZER_CHAIN.invoke(
        {"url": "https://www.getdbt.com/", "summarization_target": "what is dbt"}
    )
    print(r)
