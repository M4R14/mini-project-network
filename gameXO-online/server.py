import socket, pickle

def Main():
    # host = "10.199.2.16"
    host = ""
    port = 5000

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host,port))

    print "Server Started."
    while True:
        data, addr = s.recvfrom(1024)
        print str(addr) +": "+ str(data)

        # data = str(data).upper()
        data = [1,2,3]

        print "sending: " + str(data)
        data = pickle.dumps(data)
        s.sendto(data, addr)
    s.close()

if __name__ == '__maint__':
    Main()
