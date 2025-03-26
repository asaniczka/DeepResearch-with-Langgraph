"""
This module fetches search engine results from Google.
"""

# pylint:disable=logging-fstring-interpolation
import logging
from urllib.parse import quote

from dotenv import load_dotenv
from langchain_core.runnables import chain
from wrapworks import cwdtoenv

cwdtoenv()
load_dotenv()

from src.crawlers.crawl_page import get_page

LOGGER = logging.getLogger(__name__)


@chain
def get_serp(query: str) -> dict:
    """
    Fetches search engine results for a given query.

    Args:
        query (str): The search query string.

    Returns:
        dict: Parsed data from the search results page.
    """
    base_url = "https://www.google.com/search?client=firefox-b-lm&channel=entpr&q="
    full_url = base_url + quote(query)

    page = get_page.invoke({"url": full_url})
    return page


if __name__ == "__main__":
    get_serp("AI Tools")
