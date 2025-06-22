import itertools
import pytest

from custom_predictor import Processor, METADATA


@pytest.mark.parametrize("batch_size", [1, METADATA.batch_size // 2, METADATA.batch_size])
def test_predictor(batch_size: int, test_params: dict[str, bool | int | float | str]):
    TEST_SEQUENCES = {
        "HLSEFQHALLETPCNTERMLMQICWIAAMN",
        "HLSEFQHARLETPCNTERMLMQICWIAAMN",
        "NLSEFQHALLETPCNTERMLMQICWIAAMN",
        "NLSEFQHARLETPCNTERMLMQICWIAAMN",
        "NLSEFQHARLETPCNTKRMLMQICWIAAMN",
        "NLSEFQHARLETPCNTNRMLMQICWIAAMN",
    }

    processor = Processor(test_params)
    input_iter = itertools.batched(itertools.cycle(TEST_SEQUENCES), batch_size)
    sequences = list(next(input_iter))
    assert len(sequences) == batch_size

    values = processor(sequences=sequences, random_seed=1024)

    assert len(values) == len(sequences)
    for result in values:
        assert len(result) == len(METADATA.outputs)
        assert all(isinstance(x, float) for x in result)
