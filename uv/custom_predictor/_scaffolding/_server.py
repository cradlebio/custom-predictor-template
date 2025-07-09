from http.server import BaseHTTPRequestHandler, HTTPServer
import dataclasses
import json
from abc import ABC, abstractmethod
import functools
from socket import socket


MAX_SEQUENCE_LENGTH = 4096


@dataclasses.dataclass
class Request:
    random_seed: int
    sequences: list[str]


@dataclasses.dataclass
class Response:
    scores: list[list[float]]


@dataclasses.dataclass
class ErrorResponse:
    detail: str


class BadRequestError(ValueError):
    pass


class AbstractProcessor(ABC):
    @abstractmethod
    def __call__(self, sequences: list[str], random_seed: int) -> list[list[float]]:
        pass


class _Handler(BaseHTTPRequestHandler):
    def __init__(
        self,
        request: socket | tuple[bytes, socket],
        client_address: tuple[str, int],
        server: HTTPServer,
        batch_size: int,
        processor: AbstractProcessor,
    ):
        self._batch_size = batch_size
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
            error_response = ErrorResponse(detail=str(ex))
            self._send_response(400, "application/problem+json", json.dumps(error_response, default=dataclasses.asdict))
        except Exception as ex:
            error_response = ErrorResponse(detail=str(ex))
            self._send_response(500, "application/problem+json", json.dumps(error_response, default=dataclasses.asdict))
        else:
            self._send_response(200, "application/json", json.dumps(response, default=dataclasses.asdict))

    def _send_response(self, status_code: int, content_type: str, content: str):
        response_bytes = content.encode("utf-8")

        self.send_response(status_code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", f"{len(response_bytes)}")
        self.end_headers()

        self.wfile.write(response_bytes)

    def _process(self, payload: bytes) -> Response:
        try:
            decoded = json.loads(payload)
        except json.JSONDecodeError as ex:
            raise BadRequestError(f"Failed to decode JSON: {ex}") from ex

        field_values = {}
        fields = dataclasses.fields(Request)
        for field in fields:
            field_name = field.name.replace("_", "-")
            val = decoded.get(field_name)
            if field.default == dataclasses.MISSING and val is None:
                raise BadRequestError(f"Field `{field_name}` is missing")
            field_values[field.name] = val

        try:
            request = Request(**field_values)
        except TypeError as ex:
            raise BadRequestError(f"Failed to construct request: {ex}") from ex

        if len(request.sequences) > self._batch_size:
            raise BadRequestError(f"Provided more sequences than max batch size ({self._batch_size})")
        if any(len(seq) > MAX_SEQUENCE_LENGTH for seq in request.sequences):
            raise BadRequestError(f"Maximum sequence length exceeded ({MAX_SEQUENCE_LENGTH})")

        return Response(scores=self._processor(request.sequences, request.random_seed))


def create_server(endpoint: tuple[str, int], batch_size: int, processor: AbstractProcessor) -> HTTPServer:
    return HTTPServer(endpoint, functools.partial(_Handler, batch_size=batch_size, processor=processor))
