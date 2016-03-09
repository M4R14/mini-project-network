import socket

def Main():
    host = '10.199.2.83'
    port = 5000

    s = socket.socket()
    s.connect((host, port))

    filename = raw_input("fliename? ->")
    if filename != 'q':
        s.send(filename)
        data = s.recv(1024)
        if data[:6] == 'EXISTS':
            filesize = long(data[6:])
            message = raw_input("File Exists, " + str(filesize) +\
             "Bytes, download? (Y/N)? ->")
            if message == 'Y':
                s.send('OK')
                f = open('new_' + filename, 'wb')
                data = s.recv(1024)
                totalRecv = len(data)
                f.write(data)
                while totalRecv < filesize:
                    data = s.recv(1024)
                    totalRecv += len(data)
                    f.write(data)
                    print "{0:.sf}".format((totalRecv/float(filesize))*100)+\
                            "% Done"
                print "Dowload Complete"
        else:
            print "File does not Exist!"
    s.close()

if __name__ == '__main__':
    Main()
