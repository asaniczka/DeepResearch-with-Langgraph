from bs4 import BeautifulSoup
from markdownify import markdownify as md


def clean_html(page: str) -> str:

    soup = BeautifulSoup(page, "html.parser")

    tags_to_remove = {"header", "script", "style", "nav", "footer", "img"}
    for tag in tags_to_remove:
        for el in soup.find_all(tag):
            el.decompose()

    return md(soup.prettify())


if __name__ == "__main__":
    page = open("tests/fixtures/google_serp.html").read()
    print(clean_html(page))
