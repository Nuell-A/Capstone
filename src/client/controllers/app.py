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

def gameLoop():
    active_scene = "menu" # default
    screen_size = (1280, 720)
    clock = pygame.time.Clock() # Controls FPS & tracks time.
    dt = clock.tick(60) / 1000
    pygame.init()
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Menu")
    manager = pygame_gui.UIManager(screen_size)

    menu_view = MenuView(screen, manager, screen_size, dt)
    quiz_view = QuizView(screen, manager, screen_size, dt)


    while True:
        
        if active_scene == "menu":
            menu_view.sceneLoop()
            print("finished menu")
            active_scene = menu_view.scene

        if active_scene == "quiz":
            quiz_view.sceneLoop()

        if menu_view.scene or quiz_view.scene == "quit":
            break

    pygame.quit
    sys.exit()

gameLoop()

'''Issue deciding where to place createUI(). If it's placed in if statment, then the program starts choking
and doesn't register inputs. If it's placed in the constructor, then all views are generated and displayed
over each other. Going to look for alternate solutions.'''