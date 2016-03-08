import socket
import sys

def Main(ip):
    host = ip
    port = 5000

    s = socket.socket()
    s.connect((host,port))

    msg = raw_input("->")
    while msg != 'q':
        s.send(msg)
        data = s.recv(1024)
        print "Recieved from server: " + str(data)
        msg = raw_input("->")
    s.close()

if __name__ == '__main__':
    Main(sys.argv[1])
