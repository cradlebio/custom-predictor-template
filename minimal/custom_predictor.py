import http.server
import json


class _AlanineCounter(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/predict":
            self.send_response(404)
            self.end_headers()
            return

        content_length = int(self.headers["content-length"])
        payload = json.loads(self.rfile.read(content_length))
        sequences: list[str] = payload["sequences"]
        outputs = []
        for sequence in sequences:
            outputs.append([sequence.count("A")])
        output = json.dumps(outputs).encode()
        self.send_response(200)
        self.end_headers()
        self.wfile.write(output)


def run():
    http.server.HTTPServer(("", 8080), _AlanineCounter).serve_forever()
