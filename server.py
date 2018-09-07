import socket
import threading

server_IP = "127.0.0.1"
server_PORT = 20000
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((server_IP, server_PORT))

def keyboard_listen(sock) :
    while True :
        data, addr = sock.recvfrom(1024)
        print(data.decode())

def init(sock) :
    players_List = []
    while True :
        data, addr = sock.recvfrom(1024)
        if addr not in players_List :
            players_List.append(addr)
        if len(players_List) == 2 :
            return players_List

clnt_address = init(sock)
print(clnt_address)

t = threading.Thread(target = keyboard_listen, args = (sock,))
t.start()

