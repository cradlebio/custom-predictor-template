from http.server import BaseHTTPRequestHandler, HTTPServer
import dataclasses
import json
from typing import Callable
import functools


@dataclasses.dataclass
class Request:
    sequences: list[str]


@dataclasses.dataclass
class Response:
    scores: list[list[float]]


class BadRequestError(ValueError):
    pass


class _Handler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server, processor: Callable[[Request], Response]):
        self._processor = processor
        super().__init__(request, client_address, server)

    def do_POST(self):
        self.protocol_version = "HTTP/1.1"
        if self.path != "/predict":
            self.send_response(404)
            self.send_header("Content-Length", "0")
            return

        content_length = int(self.headers["Content-Length"])
        payload = self.rfile.read(content_length)

        try:
            response = self._process(payload)
        except BadRequestError as ex:
            text = str(ex).encode("utf-8")
            self.send_response(400)
            self.send_header("Content-Type", "text/plain")
            self.send_header("Content-Length", f"{len(text)}")
            self.end_headers()
            self.wfile.write(text)
        else:
            response_text = json.dumps(response, default=dataclasses.asdict).encode("utf-8")

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", f"{len(response_text)}")
            self.end_headers()

            self.wfile.write(response_text)

    def _process(self, payload: bytes) -> Response:
        try:
            decoded = json.loads(payload)
        except json.JSONDecodeError as ex:
            raise BadRequestError(f"Failed to decode JSON: {ex}") from ex

        field_values = {}
        fields = dataclasses.fields(Request)
        for field in fields:
            val = decoded.get(field.name)
            if field.default != dataclasses.MISSING and val is None:
                raise BadRequestError(f"Field `{field.name}` is missing")
            field_values[field.name] = val

        try:
            request = Request(**field_values)
        except TypeError as ex:
            raise BadRequestError(f"Failed to construct request: {ex}") from ex

        # TODO(armin): check number of sequences against batch size

        return self._processor(request)


def create_server(port: int, processor: Callable[[Request], Response]) -> HTTPServer:
    return HTTPServer(("", 8000), functools.partial(_Handler, processor=processor))
