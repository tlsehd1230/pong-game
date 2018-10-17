import pygame
import socket
import threading
from point import Point

server_IP = input("ip주소를 입력하세요: ")
server_PORT = int(input("포트주소를 입력하세요: "))

clck = pygame.time.Clock()

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#sock.sendto("client-connected".encode(), (server_IP, server_PORT))

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
            score_list[0] = result_list2[0]
            score_list[1] = result_list2[1]

def main() :

    gameover = False
    nomovement = True
    UP = False
    DOWN = False
    STARTED = False
    thread_running = False
    WIN1 = False
    WIN2 = False
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

    while not gameover :
        if STARTED and not thread_running:
            t1.start()
            thread_running = True

        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                gameover = True

            if event.type == pygame.MOUSEBUTTONDOWN :
                sock.sendto("START".encode(), (server_IP, server_PORT))
                STARTED = True

            if event.type == pygame.KEYDOWN :
                nomovement = False
                if event.key == pygame.K_UP :
                    UP = True
                    DOWN = False
                if event.key == pygame.K_DOWN:
                    UP = False
                    DOWN = True

            if event.type == pygame.KEYUP :
                nomovement = True
                UP = False
                DOWN = False

        if not nomovement :
            if UP :
                sock.sendto("UP".encode(), (server_IP, server_PORT))
            if DOWN :
                sock.sendto("DOWN".encode(), (server_IP, server_PORT))

        surface.fill((0, 0, 0))

        pygame.draw.rect(surface, (255, 255, 255), (player1.pos_x, player1.pos_y , 10, 50))
        pygame.draw.rect(surface, (255, 255, 255), (player2.pos_x, player2.pos_y, 10, 50))

        pygame.draw.rect(surface, (255, 255, 255), (ball.pos_x-5, ball.pos_y-5, 10, 10))

        score_label = font_40.render(str(score_list[0]), True, (255, 255, 255))
        surface.blit(score_label, (200, 50))
        score_label2 = font_40.render(str(score_list[1]), True, (255, 255, 255))
        surface.blit(score_label2, (600, 50))

        if score_list[0] == 11 :
            WIN1 = True

        if score_list[1] == 11 :
            WIN2 = True

        if WIN1 :
            surface.fill((0, 0, 0))
            winner_label = font_40.render("PLAYER 1 WIN", True, (255, 255, 255))
            surface.blit(winner_label, (400, 300))

        if WIN2 :
            surface.fill((0, 0, 0))
            winner_label2 = font_40.render("PLAYER 2 WIN", True, (255, 255, 255))
            surface.blit(winner_label2, (400, 300))

        pygame.display.update()
        clck.tick(30)

    sock.close()

main()