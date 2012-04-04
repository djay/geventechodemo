from gevent.server import StreamServer

def echo(socket, addr):
    print '...connected from:', addr
    fileobj = socket.makefile()
    while True:
        line = fileobj.readline()
        if not line: break
        fileobj.write("echo: "+line)
        fileobj.flush()

server = StreamServer(('localhost', 8080), echo)
print 'waiting for connection...'
server.serve_forever()
