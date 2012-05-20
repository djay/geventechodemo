import urllib2
import httplib
from urllib import urlencode

class gevent_HTTPConnection(httplib.HTTPConnection):
    def connect(self):
        from gevent import socket as cosocket
        self.sock = cosocket.create_connection((self.host, self.port), self.timeout)
class gevent_HTTPHandler(urllib2.HTTPHandler):
   def http_open(self, request):
        return self.do_open(gevent_HTTPConnection, request)
def gevent_url_fetch(url):
    opener = urllib2.build_opener(gevent_HTTPHandler)
    resp = opener.open(url)
    return resp


from gevent.server import StreamServer

def echo(socket, addr):
    print '...connected from:', addr
    fileobj = socket.makefile()
    while True:
        line = fileobj.readline()
        if not line: break
        line = gevent_url_fetch("http://isithackday.com/arrpi.php?"+urlencode({'text':line})).read()
        fileobj.write("echo: %s\n"%line)
        fileobj.flush()

server = StreamServer(('localhost', 8080), echo)
print 'waiting for connection...'
server.serve_forever()


