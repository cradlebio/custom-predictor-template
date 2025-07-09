import pytest


@pytest.fixture
def test_params() -> dict[str, bool | int | float | str]:
    return {
        "subseq": "E",
        "factor": 1.2,
    }
