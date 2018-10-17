import socket
import threading
import pygame
from point import Point
import time

class Ball :
    def __init__(self) :
        self.ballposX = 400
        self.ballposY = 300
        self.speedX = 5
        self.speedY = 5
        self.nextdirection = -1

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

def send_pos(sock, paddle1, paddle2, addr, ball) :
    while True :
        sock.sendto((str(paddle1.pos_y)+","+str(paddle2.pos_y)+","+str(ball.ballposX)+","+str(ball.ballposY)).encode(), addr)

clnt_address = init(sock)
paddle1 = Point()
paddle2 = Point()
ball = Ball()
paddle1.pos_y = 275
paddle2.pos_y = 275
clck = pygame.time.Clock()
player1_score = 0
player2_score = 0

t1 = threading.Thread(target = keyboard_listen, args = (sock, clnt_address, paddle1, paddle2))
t2 = threading.Thread(target = send_pos, args = (sock, paddle1, paddle2, clnt_address[0], ball))
t3 = threading.Thread(target = send_pos, args = (sock, paddle1, paddle2, clnt_address[1], ball))

t1.start()
t2.start()
t3.start()

while True :
    ball.ballposX += ball.speedX
    ball.ballposY += ball.speedY

    if ball.ballposY <= 5 or ball.ballposY >= 595 :
        ball.speedY *= -1

    if ball.ballposX <= 0 :
        ball.ballposX = 400
        ball.ballposY = 300
        player2_score += 1
        sock.sendto((str(player1_score) + "," + str(player2_score)).encode(), clnt_address[0])
        sock.sendto((str(player1_score) + "," + str(player2_score)).encode(), clnt_address[1])

    if ball.ballposX >= 790 :
        ball.ballposX = 400
        ball.ballposY = 300
        player1_score += 1
        sock.sendto((str(player1_score) + "," + str(player2_score)).encode(), clnt_address[0])
        sock.sendto((str(player1_score) + "," + str(player2_score)).encode(), clnt_address[1])

    if (ball.ballposX >= 760 and ball.ballposY >= paddle2.pos_y - 10) and (ball.ballposX >= 770 and ball.ballposY <= paddle2.pos_y + 60) :
        ball.speedX *= -1

    if (ball.ballposX <= 30 and ball.ballposY >= paddle1.pos_y - 10) and (ball.ballposX <= 30 and ball.ballposY <= paddle1.pos_y + 60) :
        ball.speedX *= -1

    clck.tick(30)