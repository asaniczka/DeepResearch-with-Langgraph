"""
Module for parsing Google Search Engine Results Pages (SERP).
"""

from bs4 import BeautifulSoup
from langchain_core.runnables import chain
from wrapworks import cwdtoenv

cwdtoenv()
from src.models.research_models import SerpResult


@chain
def parse_serp_page(state: dict) -> list[SerpResult]:
    """
    Parses a SERP (Search Engine Results Page) to extract search result items.

    Args:
        state (dict): A dictionary containing the HTML page content.

    Returns:
        list[SerpResult]: A list of parsed search results.
    """
    page = state["page"]
    soup = BeautifulSoup(page, "html.parser")

    serp_items = soup.select("div.asEBEc")

    results: list[SerpResult] = []
    for idx, item in enumerate(serp_items, 1):
        url = item.select_one("a[jsname=UWckNb]").get("href")
        title = item.select_one("h3.LC20lb").text
        description = item.select_one("div.VwiC3b").text

        results.append(
            SerpResult(url=url, title=title, description=description, rank=idx)
        )

    return results


if __name__ == "__main__":

    with open("tests/fixtures/google_serp.html") as rf:
        x = parse_serp_page(rf.read())

    from rich import print

    print(x)
