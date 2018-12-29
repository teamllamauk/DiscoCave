GNU nano 2.7.4                File: webserver.py                           
import string,cgi,time
from os import curdir, sep
#from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            try:
                url_addr, query_string = self.path.split("?")
            except:
                url_addr = self.path
                query_string = ""
            if url_addr == "/":
                url_addr = "index.html"
            try:
                query = urlparse(self.path).query
                query_components = dict(qc.split("=") for qc in query.split($split("&"))            
                qGpio = query_components["gpio"]
            except:
               print ("no qGpio")
            f = open(curdir + sep + url_addr)
            self.send_response(200)
            self.send_header('Content-type',    'text/html')
            self.end_headers()
            self.wfile.write(bytes(f.read(), "utf-8"))
            f.close()
            return
        except IOError:
            self.send_error(404,'File Not Found: %s' % url_addr)

def main():
    try:
        server = HTTPServer(('', 80), MyHandler)
        print ('started httpserver...')
        server.serve_forever()
    except KeyboardInterrupt:
        print ('^C received, shutting down server')
        server.socket.close()

if __name__ == '__main__':
    main()
