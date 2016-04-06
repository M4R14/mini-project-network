import socket, pickle

def Main():
    host = '127.0.0.1'
    port = 5001

    server = ('127.0.0.1',5000)

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, port))

    msg = raw_input("->")
    while msg != 'q':
        s.sendto(msg, server)
        data, addr = s.recvfrom(1024)
        data = pickle.loads(data)
        print "Recieced from server: " + str(data)
        msg = raw_input("->")
    s.close()

if __name__ == '__main__':
    Main()
