import socket
import threading
import pygame
from point import Point

server_IP = "127.0.0.1"
server_PORT = 20000
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((server_IP, server_PORT))

def keyboard_listen(sock, clnt_address, paddle1, paddle2) :
    while True :
        data, addr = sock.recvfrom(1024)
        if addr == clnt_address[0] :
            if data.decode() == "UP" :
                paddle1.pos_y -= 5
            if data.decode() == "DOWN" :
                paddle1.pos_y += 5
        elif addr == clnt_address[1] :
            if data.decode() == "UP":
                paddle2.pos_y -= 5
            if data.decode() == "DOWN":
                paddle2.pos_y += 5

def init(sock) :
    players_List = []
    while True :
        data, addr = sock.recvfrom(1024)
        if addr not in players_List :
            players_List.append(addr)
        if len(players_List) == 2 :
            print("2 client connected")
            return players_List

def send_pos(sock, paddle1, paddle2, addr) :
    while True :
        sock.sendto((str(paddle1.pos_y)+","+str(paddle2.pos_y)).encode(), addr)

clnt_address = init(sock)
paddle1 = Point()
paddle2 = Point()

t1 = threading.Thread(target = keyboard_listen, args = (sock, clnt_address, paddle1, paddle2))
t2 = threading.Thread(target = send_pos, args = (sock, paddle1, paddle2, clnt_address[0]))
t3 = threading.Thread(target = send_pos, args = (sock, paddle1, paddle2, clnt_address[1]))

t1.start()
t2.start()
t3.start()