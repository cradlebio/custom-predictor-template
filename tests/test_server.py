import threading
import urllib.request
import json
from typing import Callable
import itertools

from predictor import create_server, Processor, CustomPredictorMetadata


TEST_SEQUENCES = ["C", "CR", "CRAD", "CRADLE"]


def _test_server(batch_size: int, processor: Callable[[list[str], int], list[tuple[float, ...]]], sequences: list[str]):
    server = create_server(("127.0.0.1", 0), batch_size, processor)
    thread = threading.Thread(target=server.serve_forever)
    thread.start()

    try:
        host = server.server_address[0]
        port = server.server_address[1]
        url = f"http://{host}:{port}/predict"

        request_data = {
            "sequences": sequences,
            "random-seed": 42,
        }

        request = urllib.request.Request(url=url, method="POST", data=json.dumps(request_data).encode("utf-8"))

        with urllib.request.urlopen(request) as f:
            response = json.loads(f.read().decode("utf-8"))

        assert "scores" in response
        assert len(response["scores"]) == len(sequences)
        return response["scores"]
    finally:
        server.shutdown()
        thread.join()


def test_server_only():
    TEST_SCORES = [(0.0, 1.0, 2.0), (3.0, 4.0, 5.0), (6.0, 7.0, 8.0), (9.0, 10.0, 11.0)]

    def _dummy_processor(sequences: list[str], random_seed: int) -> list[tuple[float, ...]]:
        assert random_seed == 42
        assert sequences == TEST_SEQUENCES
        return TEST_SCORES

    scores = _test_server(24, _dummy_processor, TEST_SEQUENCES)
    assert scores == [list(x) for x in TEST_SCORES]


def test_server_with_processor(test_params: dict[str, bool | int | float | str]):
    metadata = CustomPredictorMetadata()
    batch_size = metadata.batch_size
    print(batch_size)

    processor = Processor(test_params)
    input_iter = itertools.batched(itertools.cycle(TEST_SEQUENCES), batch_size)
    sequences = list(next(input_iter))
    print(sequences)
    assert len(sequences) == batch_size

    scores = _test_server(batch_size, processor, sequences)

    assert len(scores) == len(sequences)
    for result in scores:
        assert len(result) == len(metadata.outputs)
        assert all(isinstance(x, float) for x in result)
