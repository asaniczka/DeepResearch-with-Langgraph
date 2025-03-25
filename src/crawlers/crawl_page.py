# pylint:disable=logging-fstring-interpolation
import logging
import os

import httpx
from dotenv import load_dotenv
from langchain_core.runnables import chain
from wrapworks import cwdtoenv

cwdtoenv()
load_dotenv()

from src.errors.main_errors import NoPageFetched
from src.models.research_models import PageCrawlResult

LOGGER = logging.getLogger(__name__)


@chain
def get_page(state: dict) -> dict:

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
        raise NoPageFetched("Unable to fetch page") from e
