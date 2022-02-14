# pyhon -m http.server 8000
from http.server import HTTPServer, SimpleHTTPRequestHandler
from datetime import datetime


class MyServer(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("content-type", "text/html")
        self.end_headers()
        print(self.path)
        # Dyanamic Routing
        if self.path == "/hello":
            content = f"<h1>Hello :) {datetime.now()}</h1>"
        else:
            content = "<h1>ERROR</h1>"
        self.wfile.write(content.encode())
        # encode -  string to byte


address = "127.0.0.1"
port = 8000
server_address = (address, port)
httpd = HTTPServer(server_address, MyServer)
httpd.serve_forever()
