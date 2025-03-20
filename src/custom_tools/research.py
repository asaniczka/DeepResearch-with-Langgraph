# pylint:disable=logging-fstring-interpolation
import os
import time
import logging
from urllib.parse import quote
import httpx
from wrapworks import cwdtoenv, dump_text
from dotenv import load_dotenv

cwdtoenv()
load_dotenv()

from src.errors.main_errors import NoPageFetched

LOGGER = logging.getLogger(__name__)


def get_page(url: str) -> tuple[str, str]:

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

            if api_response.status_code == 429:
                raise RuntimeError("Ratelimit on Zyte")

            api_response.raise_for_status()

            browser_html: str = api_response.json()["browserHtml"]

            return browser_html, url
        except httpx.HTTPStatusError as e:
            LOGGER.error(
                f"Http status error {e.response.status_code}: {e.response.text}"
            )
            raise NoPageFetched("Unable to fetch page") from e
        except (RuntimeError, httpx.ConnectError):
            retries += 1
            time.sleep(5)


def get_serp(query: str) -> list:

    base_url = "https://www.google.com/search?client=firefox-b-lm&channel=entpr&q="
    full_url = base_url + quote(query)

    page, _ = get_page(full_url)
    dump_text("tests/fixtures/google_serp.html", page)


if __name__ == "__main__":
    get_serp("AI Tools")
