import itertools
import pytest

from predictor import CustomPredictorMetadata, Processor

METADATA = CustomPredictorMetadata()


@pytest.mark.parametrize("batch_size", [1, METADATA.batch_size // 2, METADATA.batch_size])
def test_predictor(batch_size: int):
    TEST_PARAMS = {
        "greeting": "Hello",
        "factor": 1.2,
    }

    TEST_SEQUENCES = {
        "HLSEFQHALLETPCNTERMLMQICWIAAMN",
        "HLSEFQHARLETPCNTERMLMQICWIAAMN",
        "NLSEFQHALLETPCNTERMLMQICWIAAMN",
        "NLSEFQHARLETPCNTERMLMQICWIAAMN",
        "NLSEFQHARLETPCNTKRMLMQICWIAAMN",
        "NLSEFQHARLETPCNTNRMLMQICWIAAMN",
    }

    processor = Processor(TEST_PARAMS)
    input_iter = itertools.batched(itertools.cycle(TEST_SEQUENCES), batch_size)
    sequences = list(next(input_iter))
    assert len(sequences) == batch_size

    values = processor(sequences=sequences, random_seed=1024)

    assert len(values) == len(sequences)
    for result in values:
        assert len(result) == len(METADATA.outputs)
        assert all(isinstance(x, float) for x in result)
