# pylint:disable=logging-fstring-interpolation
import logging
import os
import time

import httpx
from dotenv import load_dotenv
from wrapworks import cwdtoenv

from src.models.research_models import PageCrawlResult

cwdtoenv()
load_dotenv()

from src.errors.main_errors import NoPageFetched

LOGGER = logging.getLogger(__name__)


def get_page(url: str) -> PageCrawlResult | None:

    retries = 0
    while retries < 2:
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
            return PageCrawlResult(url=url, page=browser_html)

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:
                retries += 1
                time.sleep(5)
                continue

            LOGGER.error(
                f"Http status error {e.response.status_code}: {e.response.text}"
            )
            raise NoPageFetched("Unable to fetch page") from e
        except httpx.ConnectError:
            retries += 1
            time.sleep(5)

    return None
