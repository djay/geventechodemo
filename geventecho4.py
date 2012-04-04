from gevent.monkey import patch_all; patch_all()
from socket import *
import threading
import urllib2

def echo(socket, addr):
    print '...connected from:', addr
    fileobj = socket.makefile()
    while True:
        line = fileobj.readline()
        if not line: break
        line = urllib2.urlopen("http://isithackday.com/arrpi.php?text="+line).read()
        fileobj.write("echo: %s\n"%line)
        fileobj.flush()

serversock = socket(AF_INET, SOCK_STREAM)
serversock.bind( ('localhost',8080) )
serversock.listen(2)

while 1:
     print 'waiting for connection...'
     clientsock, addr = serversock.accept()
     threading.Thread(target=echo, args=(clientsock,addr)).start()
