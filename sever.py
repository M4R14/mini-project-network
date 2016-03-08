from socket import *

def Main():
    host = '127.0.0.1'
    port = 5000

    s = socket()
    s.bind((host,port))

    s.listen(1)
    c, addr = s.accept()
    print "Connection From: " + str(addr)
    while True:
        data = c.recv(1024)
        if not data:
            break
        print "From connection user: " + str(data)
        data = str(data).upper()
        print "sending: " + str(data)
        c.send(data)
    c.close()

if __name__ == '__main__':
    Main()
