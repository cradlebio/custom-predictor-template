from ._metadata import CustomPredictorMetadata

import dataclasses
import subprocess
import json
from pathlib import Path


def _json_normalize(x):
    TYPEMAP = {int: "INT64", str: "STRING", float: "FLOAT64", bool: "BOOL"}
    if dataclasses.is_dataclass(x):
        return dataclasses.asdict(x)  # pyright: ignore[reportArgumentType]
    if isinstance(x, type):
        return TYPEMAP[x]
    raise TypeError(x)


def build(metadata: CustomPredictorMetadata, output_directory: Path):
    output_directory.mkdir(parents=True, exist_ok=True)
    cwd = Path(__file__).parents[1]

    out = subprocess.run(["uv", "run", "pytest"], cwd=cwd)
    if out.returncode != 0:
        raise ValueError("Not all tests are passing")

    with open(output_directory / "metadata.json", "w") as f:
        json.dump(metadata, f, indent=4, default=_json_normalize)

    subprocess.run(["docker", "build", ".", "--platform", "linux/amd64", "-t", metadata.name], cwd=cwd, check=True)

    subprocess.run(
        [
            "docker",
            "save",
            "--platform",
            "linux/amd64",
            metadata.name,
            "-o",
            str(output_directory / "custom-predictor.tar"),
        ],
        cwd=cwd,
        check=True,
    )
