import socket
import time
import pickle

def getIP():
    return socket.gethostbyname(socket.gethostname())

def sendMsg(s, msg, addr):
    s.sendto(msg, addr)
    # print("send to ", addr, ":",msg)

host = '10.199.2.83'
port = 5000

clients = []
player = []

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
s.setblocking(0)

quitting = False
print("Server Started!! at ", getIP())

while not quitting:
    try:
        data, addr = s.recvfrom(1024)
        dataArr = pickle.loads(data)
        print(time.ctime(time.time()) + str(addr) + ": :" + repr(pickle.loads(data)))

        if "ONLINE" in dataArr['data']:
            msg = ''
            index = 0
            if not player:
                msg = "True"
            else:
                for pl in player:
                    if dataArr['from'] == pl['name']:
                        msg = "False"
                        break
                    else:
                        msg = "True"
                    index = index+1

            if msg == "True":
                player.append({
                    'name'  :dataArr['from'],
                    'score' :'0',
                    'addr'  :addr
                })
                sendMsg(s, msg.encode('utf-8'), addr)
            else:
                msg = "True"
                player[index]['addr'] = addr
                sendMsg(s, msg.encode('utf-8'), addr)

        elif "Quit" in str(data):
            quitting = True

        elif "list-player" in dataArr['data']:
            s.sendto(pickle.dumps(player), addr)
            # print("send to ", addr, ":", repr(pickle.dumps(player)))

        elif 'game' in dataArr['title']:
            addrPlayer = ''
            for li in player:
                if dataArr['send'] == li['name']:
                    addrPlayer = li['addr']
            s.sendto(data, addrPlayer)
            print('Send!!'+str(addrPlayer))

        elif 'changpoint' in dataArr['title']:
            index = 0
            for li in player:
                if dataArr['from'] == li['name']:
                    score = int(li['score']) + int(dataArr['data'])
                    player[index]['score'] = str(score)
                    break
                index = index + 1

        elif addr not in clients:
            clients.append(addr)#ลงทะเบียน IP
    except:
        pass
s.close()
