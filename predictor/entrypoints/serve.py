from predictor import create_server, Response


def bla(Request) -> Response:
    return Response(scores=[])


def serve():
    with create_server(8000, bla) as server:
        server.serve_forever()


if __name__ == "__main__":
    serve()
