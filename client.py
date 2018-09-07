import pygame
import socket

server_IP = "127.0.0.1"
server_PORT = 20000
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto("client-connected".encode(), (server_IP, server_PORT))

pygame.init()

display_width = 800
display_height = 600
surface = pygame.display.set_mode((display_width, display_height))

pygame.display.set_caption("pong-game")

def main() :
    gameover = False

    while not gameover :
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                gameover = True

            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_UP :
                    sock.sendto("UP".encode(), (server_IP, server_PORT))
                if event.key == pygame.K_DOWN :
                    sock.sendto("DOWN".encode(), (server_IP, server_PORT))

        pygame.display.update()

    sock.close()

main()