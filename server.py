import socket
import threading
import pygame

server_IP = "192.168.0.11"
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
            print("2 client connected")
            return players_List

def sendstring(sock, addr) :
    clck = pygame.time.Clock()
    num = 0
    while True :
        sock.sendto(str(num).encode(), addr)
        num += 5
        clck.tick(30)

clnt_address = init(sock)

t1 = threading.Thread(target = keyboard_listen, args = (sock,))
t2 = threading.Thread(target = sendstring, args = (sock, clnt_address[0]))
t3 = threading.Thread(target = sendstring, args = (sock, clnt_address[1]))

t1.start()
t2.start()
t3.start()




