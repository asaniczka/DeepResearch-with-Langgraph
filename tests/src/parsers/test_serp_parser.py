import pytest
from wrapworks import cwdtoenv

cwdtoenv()

from src.models.research_models import SerpResult
from src.parsers.serp_parser import parse_serp_page


@pytest.fixture()
def get_sample_page() -> str:

    with open("tests/fixtures/google_serp.html") as rf:
        file = rf.read()

    return file


class TestSerpParser:

    def test_parse_serp_page(self, get_sample_page: str):

        result = parse_serp_page(get_sample_page)

        assert isinstance(result, list)
        for x in result:
            assert isinstance(x, SerpResult)


if __name__ == "__main__":
    pytest.main([__file__, "-vs"])
