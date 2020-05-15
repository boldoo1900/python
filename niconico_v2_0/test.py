from threading import Thread

# python2
# from SocketServer import ThreadingMixIn
# from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
# python3
from socketserver import ThreadingMixIn
from http.server import HTTPServer, BaseHTTPRequestHandler

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        # self.wfile.write("Hello World!")
        self.wfile.write(bytes("Hello World!", "utf-8"))

class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True

def serve_on_port(port):
    server = ThreadingHTTPServer(("localhost",port), Handler)
    server.serve_forever()

Thread(target=serve_on_port, args=[1111]).start()
serve_on_port(2222)