import pytest


@pytest.fixture
def test_params() -> dict[str, bool | int | float | str]:
    return {
        "greeting": "you",
        "factor": 1.2,
    }
