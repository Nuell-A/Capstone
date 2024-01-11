import socket
import pygame
import pygame_gui

import sys
sys.path.insert(1, "/Users/emanuelalcala/Desktop/Projects/Project/Capstone/src") # Mac
sys.path.insert(2, "C:\\Users\\alcal\\Documents\\Projects\\Capstone\\Capstone\\src") # Windows
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

screen_size = (1280, 720)
running = True
clock = pygame.time.Clock() # Controls FPS & tracks time.

pygame.init()
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Menu")
manager = pygame_gui.UIManager(screen_size)

menu_view = MenuView(screen, manager, screen_size)
quiz_view = QuizView(screen, manager, screen_size)

current_state = "menu" # Default view is the menu

while running:
    dt = clock.tick(30) / 1000 # Liimits to 30 fps


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if current_state == "menu":
            menu_view.handleEvents(event)

        elif current_state == "hosting":
            print("host state")
        elif current_state == "joining":
            print("joing state")
        elif current_state == "quiz":
            print("quiz state")
            quiz_view.createUI()
            quiz_view.handleEvents(event)

    if current_state == "menu":
        menu_view.update(dt)
        menu_view.draw()
    elif current_state == "hosting":
        pass
    elif current_state == "joining":
        pass
    elif current_state == "quiz":
        pass

    pygame.display.update() # Updates whole screen (if no argument is passed).

pygame.quit

'''Issue deciding where to place createUI(). If it's placed in if statment, then the program starts choking
and doesn't register inputs. If it's placed in the constructor, then all views are generated and displayed
over each other. Going to look for alternate solutions.'''