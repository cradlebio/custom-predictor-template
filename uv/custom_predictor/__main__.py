from ._processor import Processor, METADATA
from ._scaffolding import run


if __name__ == "__main__":
    run(METADATA, Processor)
