import pygame
import socket
import threading

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

def listen(sock, data_list) :
    while True :
        data, addr = sock.recvfrom(1024)
        data_list[0] = int(data.decode())

def main() :

    data_list = [0]

    t1 = threading.Thread(target = listen, args = (sock, data_list))
    t1.start()

    gameover = False
    nomovement = True
    UP = False
    DOWN = False

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

            if event.type == pygame.KEYUP :
                nomovement = True
                UP = False
                DOWN = False

        if not nomovement :
            if UP :
                sock.sendto("UP".encode(), (server_IP, server_PORT))
            if DOWN :
                sock.sendto("DOWN".encode(), (server_IP, server_PORT))

        #data, addr = sock.recvfrom(10)
        #print(int(data.decode()))

        surface.fill((0, 0, 0))

        pygame.draw.rect(surface, (255, 255, 255), (data_list[0], 300, 10, 10))

        pygame.display.update()
        clck.tick(30)

    sock.close()

main()
