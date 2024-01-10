import socket
import pygame
import pygame_gui

import sys
sys.path.insert(1, "/Users/emanuelalcala/Desktop/Projects/Project/Capstone/src")
import config
from client.views.menu import MenuView
from client.views.quiz import QuizView
'''
# Using with statment means that we do not have to close the socket,
# . it closes on its own.
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Initiate connection with server host/port combo.
    s.connect((config.socket_host, config.socket_port))

    while True:
        message = input("Type a message:")
        if not message:
            break
        s.sendall(message.encode("utf-8"))
        receive = s.recv(1024)
        print(receive)
'''

WIDTH, HEIGHT = 1280, 720
running = True
clock = pygame.time.Clock() # Controls FPS & tracks time.

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu")
manager = pygame_gui.UIManager((WIDTH, HEIGHT))

menu_view = MenuView(screen, manager, WIDTH, HEIGHT)

while running:
    dt = clock.tick(30) / 1000 # Liimits to 30 fps

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        menu_view.handleEvents(event)

        menu_view.update(dt)
        menu_view.draw()
        pygame.display.update() # Updates whole screen (if no argument is passed).

pygame.quit