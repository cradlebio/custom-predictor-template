from http.server import BaseHTTPRequestHandler, HTTPServer
from dataclasses import dataclass, asdict
import json


@dataclass
class Request:
    sequences: list[str]


@dataclass
class Response:
    scores: list[list[float]]


class _Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        self.protocol_version = "HTTP/1.1"
        if self.path != "/predict":
            self.send_response(404)
            self.send_header("Content-Length", "0")
            return

        content_length = int(self.headers["Content-Length"])
        payload = self.rfile.read(content_length)

        try:
            _request = Request(**json.loads(payload))
        except TypeError:
            self.send_response(400)
            self.send_header("Content-Length", "0")
            return

        # TODO(armin): check number of sequences against batch size

        response = Response(scores=[[0, 0], [0, 0], [0, 0]])
        response_text = json.dumps(response, default=asdict).encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", "{}".format(len(response_text)))
        self.end_headers()

        self.wfile.write(response_text)


def create_server(port: int) -> HTTPServer:
    return HTTPServer(("", 8000), _Handler)
