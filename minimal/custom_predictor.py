from concurrent.futures import ThreadPoolExecutor
import http.server
import json
from socketserver import ThreadingMixIn


class ThreadingHTTPServer(ThreadingMixIn, http.server.HTTPServer):
    """Allow concurrent requests to the HTTP server

    This makes sure that health probes can be processed immediately and don't
    need to wait on a previous request handler to finish.
    """

    def __init__(self, endpoint: tuple[str, int], handler: type[http.server.BaseHTTPRequestHandler]):
        self._pool = ThreadPoolExecutor(max_workers=1)
        super().__init__(endpoint, handler)


class _AlanineCounter(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/predict":
            self.send_response(404)
            self.end_headers()
            return

        self.server._pool.submit(self._process).result()  # pyright: ignore[reportAttributeAccessIssue]

    def _process(self):
        content_length = int(self.headers["content-length"])
        payload = json.loads(self.rfile.read(content_length))
        sequences: list[str] = payload["sequences"]
        outputs = []
        for sequence in sequences:
            outputs.append([sequence.count("A")])
        output = json.dumps({"scores": outputs}).encode()
        self.send_response(200)
        self.end_headers()
        self.wfile.write(output)


def run():
    ThreadingHTTPServer(("", 8080), _AlanineCounter).serve_forever()
