import sys
import pygame_gui
import pygame
import time

from scene1 import MenuView
from scene2 import QuizView

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

        time.sleep(2)
        if menu_view.scene == "quiz":
            quiz_view.sceneLoop()

        if active_scene == active_scene:
            break

    pygame.quit
    sys.exit()

gameLoop()