from bs4 import BeautifulSoup
from wrapworks import cwdtoenv

cwdtoenv()
from src.models.research_models import SerpResult


def parse_serp_page(page: str) -> list[SerpResult]:

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
