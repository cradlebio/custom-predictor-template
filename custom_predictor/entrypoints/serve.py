from custom_predictor import create_server, Processor, CustomPredictorMetadata
import argparse


def bool_parser(v):
    if v.lower() == "true":
        return True
    elif v.lower() == "false":
        return False
    else:
        raise argparse.ArgumentTypeError("Boolean value (true or false) expected.")


def serve():
    metadata = CustomPredictorMetadata()
    parser = argparse.ArgumentParser()
    for inp in metadata.inputs:
        TYPEMAP = {int: int, str: str, float: float, bool: bool_parser}
        if inp.default is not None:
            parser.add_argument(f"--{inp.name}", type=TYPEMAP[inp.type], default=inp.default)
        else:
            parser.add_argument(f"--{inp.name}", type=TYPEMAP[inp.type], required=True)
    args = parser.parse_args()

    processor = Processor(vars(args))
    with create_server(("", 8080), metadata.batch_size, processor) as server:
        server.serve_forever()


if __name__ == "__main__":
    serve()
