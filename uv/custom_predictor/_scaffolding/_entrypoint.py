from ._build import build
from ._metadata import CustomPredictorMetadata
from ._server import AbstractProcessor, create_server

import argparse
from pathlib import Path
from collections.abc import Callable


def bool_parser(v):
    if v.lower() == "true":
        return True
    elif v.lower() == "false":
        return False
    else:
        raise argparse.ArgumentTypeError("Boolean value (true or false) expected.")


def serve(
    metadata: CustomPredictorMetadata, processor_factory: Callable[[dict], AbstractProcessor], args: argparse.Namespace
):
    processor = processor_factory(vars(args))
    with create_server(("", 8080), metadata.batch_size, processor) as server:
        server.serve_forever()


def run(metadata: CustomPredictorMetadata, processor_factory: Callable[[dict], AbstractProcessor]):
    parser = argparse.ArgumentParser(prog="PROG")
    subparsers = parser.add_subparsers(dest="command", required=True)

    serve_parser = subparsers.add_parser("serve")
    for inp in metadata.inputs:
        TYPEMAP = {int: int, str: str, float: float, bool: bool_parser}
        if inp.default_value is not None:
            serve_parser.add_argument(f"--{inp.name}", type=TYPEMAP[inp.type], default=inp.default_value)
        else:
            serve_parser.add_argument(f"--{inp.name}", type=TYPEMAP[inp.type], required=True)

    build_parser = subparsers.add_parser("build")
    build_parser.add_argument("output_directory", type=Path)

    args = parser.parse_args()
    if args.command == "serve":
        serve(metadata, processor_factory, args)
    elif args.command == "build":
        build(metadata, args.output_directory)
