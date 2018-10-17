import pygame
import socket
import threading
from point import Point

server_IP = "127.0.0.1"
server_PORT = 20000

clck = pygame.time.Clock()

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto("client-connected".encode(), (server_IP, server_PORT))

pygame.init()

display_width = 800
display_height = 600
surface = pygame.display.set_mode((display_width, display_height))

pygame.display.set_caption("pong-game")

def listen(sock, player1, player2, ball, score_list) :
    while True :
        data, addr = sock.recvfrom(1024)
        if len(data.decode()) > 10 :
            result_list = data.decode().split(",")
            result_list = list(map(int, result_list))
            player1.pos_y = result_list[0]
            player2.pos_y = result_list[1]
            ball.pos_x = result_list[2]
            ball.pos_y = result_list[3]

        else :
            result_list2 = data.decode().split(",")
            result_list2 = list(map(int, result_list2))
            print(data.decode())
            score_list[0] = result_list2[0]
            score_list[1] = result_list2[1]

def main() :

    gameover = False
    nomovement = True
    UP = False
    DOWN = False
    UP2 = False
    DOWN2 = False
    player1 = Point()
    player2 = Point()
    ball = Point()
    player1.pos_x = 20
    player2.pos_x = 770
    player1.pos_y = 275
    player2.pos_y = 275
    ball.pos_x = 400
    ball.pos_y = 300
    score_list = [0, 0]
    font_40 = pygame.font.SysFont("D2Coding", 40)

    t1 = threading.Thread(target=listen, args=(sock, player1, player2, ball, score_list))
    t1.start()

    while not gameover :
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                gameover = True

            if event.type == pygame.KEYDOWN :
                nomovement = False
                if event.key == pygame.K_UP :
                    UP = True
                    DOWN = False
                if event.key == pygame.K_DOWN:
                    UP = False
                    DOWN = True
                if event.key == pygame.K_q :
                    UP2 = True
                    DOWN2 = False
                if event.key == pygame.K_a :
                    UP2 = False
                    DOWN2 = True

            if event.type == pygame.KEYUP :
                nomovement = True
                UP = False
                DOWN = False
                UP2 = False
                DOWN2 =False

            #if event.type == pygame.MOUSEBUTTONUP :
            #    sock.sendto("START".encode(), (server_IP, server_PORT))

        if not nomovement :
            if UP :
                sock.sendto("UP".encode(), (server_IP, server_PORT))
            if DOWN :
                sock.sendto("DOWN".encode(), (server_IP, server_PORT))
            if UP2 :
                sock.sendto("UP2".encode(), (server_IP, server_PORT))
            if DOWN2 :
                sock.sendto("DOWN2".encode(), (server_IP, server_PORT))

        surface.fill((0, 0, 0))

        pygame.draw.rect(surface, (255, 255, 255), (player1.pos_x, player1.pos_y , 10, 50))
        pygame.draw.rect(surface, (255, 255, 255), (player2.pos_x, player2.pos_y, 10, 50))

        pygame.draw.rect(surface, (255, 255, 255), (ball.pos_x-5, ball.pos_y-5, 10, 10))



        pygame.display.update()
        clck.tick(30)

    sock.close()

main()