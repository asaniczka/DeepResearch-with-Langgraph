"""
This module contains tests for the SERP parser.

- Uses pytest for testing.
- Defines test cases for the parse_serp_page function.
- Includes a fixture to provide test HTML content.
"""

import pytest
from wrapworks import cwdtoenv

cwdtoenv()

from src.models.research_models import SerpResult
from src.parsers.serp_parser import parse_serp_page


@pytest.fixture()
def get_sample_page() -> str:
    """
    Returns the content of the 'google_serp.html' file as a string. This fixture can be used in tests that require HTML content.
    """
    with open("tests/fixtures/google_serp.html") as rf:
        file = rf.read()

    return file


class TestSerpParser:
    """
    Test parser for SERP page responses.

    Tests the output of the parse_serp_page function to ensure it returns a list of SerpResult instances.
    """

    def test_parse_serp_page(self, get_sample_page: str):
        """
        Tests the 'parse_serp_page' function to verify it returns a list of SerpResult objects.
        """
        result = parse_serp_page(get_sample_page)

        assert isinstance(result, list)
        for x in result:
            assert isinstance(x, SerpResult)


if __name__ == "__main__":
    pytest.main([__file__, "-vs"])
