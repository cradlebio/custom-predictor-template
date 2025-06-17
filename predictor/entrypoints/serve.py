from predictor import create_server, Processor
from predictor.metadata import CustomPredictorMetadata


def serve():
    metadata = CustomPredictorMetadata()
    processor = Processor({})  # TODO(armin): provide parameters
    with create_server(8000, metadata.batch_size, processor) as server:
        server.serve_forever()


if __name__ == "__main__":
    serve()
