import os

from predictor import CustomPredictorMetadata


def top_level_path():
    if __package__ is None:
        raise ValueError("top_level_path() must be called from within a package")

    packages = __package__.split(".")
    cur_dir = os.path.dirname(__file__)
    for _ in packages:
        cur_dir = os.path.dirname(cur_dir)
    return cur_dir


def build():
    metadata = CustomPredictorMetadata()
    args = ["docker", "build", top_level_path(), "-t", metadata.name]
    print(" ".join(args))

    os.execvp("docker", ["docker", "build", top_level_path(), "-t", metadata.name])


if __name__ == "__main__":
    build()
