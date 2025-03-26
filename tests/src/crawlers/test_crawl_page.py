"""
Test module for `get_page` function.
"""

import pytest
from dotenv import load_dotenv
from wrapworks import cwdtoenv

load_dotenv()
cwdtoenv()
from src.crawlers.crawl_page import get_page


class TestCrawlPage:
    """
    TestCrawlPage handles testing the get_page function to ensure it returns the expected output for a given URL.
    """

    def test_get_page(self):
        """
        Test the functionality of get_page. Verifies that the URL returns a valid page and checks the returned page's type and length.
        """
        url = "https://google.com"
        page, return_url = get_page(url)

        assert return_url == url
        assert isinstance(page, str)
        assert len(page) > 1000


if __name__ == "__main__":
    pytest.main([__file__, "-vs"])
