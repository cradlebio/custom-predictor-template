from predictor import create_server


def serve():
    with create_server(8000) as server:
        server.serve_forever()


if __name__ == "__main__":
    serve()
