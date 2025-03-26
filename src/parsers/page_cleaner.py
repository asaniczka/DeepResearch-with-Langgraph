"""
This module provides functionality to clean HTML content.
"""

from bs4 import BeautifulSoup
from langchain_core.runnables import chain
from markdownify import markdownify as md


@chain
def clean_html(state: dict) -> str:
    """
    Cleans the HTML content by removing unwanted tags and returns the modified state.

    Args:
        state (dict): Contains the HTML page to be cleaned.
    """
    page = state["page"]
    soup = BeautifulSoup(page, "html.parser")

    tags_to_remove = {"header", "script", "style", "nav", "footer", "img"}
    for tag in tags_to_remove:
        for el in soup.find_all(tag):
            el.decompose()

    state["page"] = md(soup.prettify())
    return state


if __name__ == "__main__":
    page = open("tests/fixtures/google_serp.html").read()
    print(clean_html(page))
