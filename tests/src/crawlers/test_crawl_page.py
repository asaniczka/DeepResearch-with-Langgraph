import pytest
from dotenv import load_dotenv
from wrapworks import cwdtoenv

load_dotenv()
cwdtoenv()
from src.crawlers.crawl_page import get_page


class TestCrawlPage:

    def test_get_page(self):

        url = "https://google.com"
        page, return_url = get_page(url)

        assert return_url == url
        assert isinstance(page, str)
        assert len(page) > 1000


if __name__ == "__main__":
    pytest.main([__file__, "-vs"])
