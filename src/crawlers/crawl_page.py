# pylint:disable=logging-fstring-interpolation
import logging
import os

import httpx
from dotenv import load_dotenv
from langchain_core.runnables import chain
from wrapworks import cwdtoenv

cwdtoenv()
load_dotenv()

from src.models.research_models import PageCrawlResult

LOGGER = logging.getLogger(__name__)


@chain
def get_page(state: dict) -> dict:
    """
    Fetches a web page using JavaScript rendering and updates the state with the page content.

    Args:
        state (dict): A dictionary containing the URL and state data.

    Returns:
        dict: Updated state with page content or an error message.
    """
    url = state["url"]
    try:
        print(f"Getting {url} with JS Rendering")
        api_response = httpx.post(
            "https://api.zyte.com/v1/extract",
            auth=(os.environ["ZYTE_API_KEY"], ""),
            json={
                "url": url,
                "browserHtml": True,
                "geolocation": "US",
            },
            timeout=30,
        )

        api_response.raise_for_status()
        browser_html: str = api_response.json()["browserHtml"]
        result = PageCrawlResult(url=url, page=browser_html)
        state["page"] = result.page
        return state
    except httpx.HTTPStatusError as e:
        LOGGER.error(f"Http status error {e.response.status_code}: {e.response.text}")
        state["page"] = "Unable to fetch page"
        return state
    except Exception as e:
        state["page"] = f"Unable to fetch page: type e {type(e)}: e {e}"
        return state
