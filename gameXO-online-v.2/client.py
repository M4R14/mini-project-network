import socket
import pickle
import time

# gemeOX
board = [0,1,2,
         3,4,5,
         6,7,8]

def show():
    print (board[0],'|',board[1],'|',board[2])
    print ('---------')
    print (board[3],'|',board[4],'|',board[5])
    print ('---------')
    print (board[6],'|',board[7],'|',board[8])

def checkLine(char, spot1, spot2, spot3):
    if board[spot1] == char and board[spot2] == char and board[spot3] == char:
        # print board[spot1],':',board[spot2],':',board[spot3]
        return True

def checkWin(char):
    if checkLine(char,0,1,2):
        return True
    if checkLine(char,3,4,5):
        return True
    if checkLine(char,6,7,8):
        return True

    if checkLine(char,0,3,6):
        return True
    if checkLine(char,1,4,7):
        return True
    if checkLine(char,2,5,8):
        return True

    if checkLine(char,0,4,8):
        return True
    if checkLine(char,2,4,6):
        return True

def spot(char, key):
    if board[key] != 'X' and board[key] != 'O':
        board[key] = char
        return True
    else:
        return False

def GameForSelect(sock, name, player, server):
    Exit = False
    show()
    while not Exit:
        #ตาเดินของ X
        while True:
            key = input("Select a spot (X): ")

            data = {
                "from"  : name,
                "send"  : player['name'],
                "title" : 'game',
                "data"  : key
            }
            sock.sendto(pickle.dumps(data), server)

            key = int(key)

            if spot('X', key) == True:
                show()
                if checkWin('X') == True:
                    print("~~~~ X WIN ~~~~")
                    print(name + " get point +1")
                    Exit = True
                    return 1
                break
            else:
                print ('This spot is taken!')

        # ตรวจสอบจบเกมส์
        if Exit == True:
            break

        #ตาเดินของ O
        while True:
            # key = input("Select a spot (O): ")
            print(str(player['name'])+" Think...")
            data, addr = sock.recvfrom(1024)
            data = pickle.loads(data)
            key = int(data['data'])
            print(str(data['from'])+" select "+str(data['data']))

            if spot('O', key) == True:
                show()
                if checkWin('O') == True:
                    print("~~~~ O WIN ~~~~")
                    print(name + " lose point -1")
                    Exit = True
                    return -1
                break
            else:
                print ('This spot is taken!')

def GameForWait(sock, name, player ,server):
    Exit = False
    show()
    while not Exit:
        #ตาเดินของ X
        while True:
            print(str(player)+" Think...")
            data, addr = sock.recvfrom(1024)
            data = pickle.loads(data)
            key = int(data['data'])
            print(str(player)+" select "+str(data['data']))

            if spot('X', key) == True:
                show()
                if checkWin('X') == True:
                    print("~~~~ X WIN ~~~~")
                    print(name + " lose point -1")
                    Exit = True
                    return -1
                break
            else:
                print ('This spot is taken!')

        # ตรวจสอบจบเกมส์
        if Exit == True:
            break

        #ตาเดินของ O
        while True:
            # key = input("Select a spot (O): ")
            key = input("Select a spot (O): ")

            data = {
                "from"  : name,
                "send"  : player,
                'title' : 'game',
                "data"  : key
            }
            sock.sendto(pickle.dumps(data), server)

            key = int(key)

            if spot('O', key) == True:
                show()
                if checkWin('O') == True:
                    print("~~~~ O WIN ~~~~")
                    print(name + " get point +1")
                    Exit = True
                    return 1
                break
            else:
                print ('This spot is taken!')
# -------------------------

def listPlayer(sock, name, server):
    data = {
        "from"  : name,
        "send"  : "server",
        "data"  : "list-player"
    }
    sock.sendto(pickle.dumps(data), server)
    data, addr = sock.recvfrom(1024)
    data = pickle.loads(data)
    for li in data:
        if name in li['name']:
            data.remove(li)
    return data

def changpoint(point,sock, name, server):
    data = {
        "from"  : name,
        "send"  : "server",
        'title' : "changpoint",
        "data"  : str(point)
    }
    sock.sendto(pickle.dumps(data), server)

def Main():
    host = ''
    port = 0

    IP = input("IP Server: ")
    server = (IP,5000)

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, port))

    while True:
        name = input("Who are you? ")
        if name:
            data = {
                "from"  : name,
                "send"  : "server",
                "data"  : "ONLINE"
            }
            s.sendto(pickle.dumps(data), server)
            data, addr = s.recvfrom(1024)
            data = data.decode('utf-8')
            # print(data)
            if "True" == data:
                print(name," ONLINE!!")
                break

    while True:
        cmd = input("-> ")
        cmd_arr = cmd.split(' ')

        if 'list' == cmd:
            data = listPlayer(s,name,server)

            i=1
            print('No.','|','NAME')
            print('--------------')
            for li in data:
                print(i, '  |', li['name'], "(", li['score'],")")
                i=i+1

        if 'select' == cmd_arr[0]:
            data = listPlayer(s,name,server)
            index = int(cmd_arr[1])-1
            player = data[index]

            data = {
                "from"  : name,
                "send"  : player['name'],
                'title' : 'game',
                "data"  : "join"
            }
            s.sendto(pickle.dumps(data), server)
            print('...')
            data, addr = s.recvfrom(1024)
            data = pickle.loads(data)
            if 'yes' == data['data']:
                print('--------- Game start!! ------------')
                point = GameForSelect(s, name, player, server)
                changpoint(point,s, name, server)
            else:
                print('sorry')

        if 'wait' == cmd_arr[0]:
            data, addr = s.recvfrom(1024)
            data = pickle.loads(data)
            if 'join' == data['data']:
                while True:
                    join = input("Are you join the gmae with " + str(data['from']) +"? (yes/no): ")
                    if 'yes' == join:
                        say = "yes"
                        break
                    elif 'no' == join:
                        say = "no"
                        break
                    else:
                        print('yes/no')
            msg = {
                "from"  : name,
                "send"  : data['from'],
                'title' : 'game',
                "data"  : say
            }
            s.sendto(pickle.dumps(msg), server)
            if say == "yes":
                print('--------- Game start!! ------------')
                point = GameForWait(s, name, data['from'], server)
                changpoint(point,s, name, server)
            else:
                print("...")

        if 'score' ==  cmd_arr[0]:
            data = {
                "from"  : name,
                "send"  : "server",
                "data"  : "list-player"
            }
            s.sendto(pickle.dumps(data), server)
            data, addr = s.recvfrom(1024)
            data = pickle.loads(data)
            i=1
            print('No.','|','NAME')
            print('--------------')
            for li in data:
                print(i, '  |', li['name'], "(", li['score'],")")
                i=i+1

    # Game start

    s.close()

if __name__ == '__main__':
    Main()
