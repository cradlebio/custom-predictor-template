import dataclasses
import json
import sys

from custom_predictor import CustomPredictorMetadata


def _json_normalize(x):
    if dataclasses.is_dataclass(x):
        return dataclasses.asdict(x)  # pyright: ignore[reportArgumentType]
    if isinstance(x, type):
        return x.__name__
    raise TypeError(x)


def dump_metadata():
    metadata = CustomPredictorMetadata()
    json.dump(metadata, sys.stdout, indent=4, default=_json_normalize)


if __name__ == "__main__":
    dump_metadata()
