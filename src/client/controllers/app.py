import pygame
import pygame_gui
import logging
from network_client import NetworkClient

import sys
sys.path.insert(1, "/Users/emanuelalcala/Desktop/Projects/Project/Capstone/src") # Mac
sys.path.insert(2, "C:\\Users\\alcal\\Documents\\Projects\\Capstone\\Capstone\\src") # Windows
from client.views.menu import MenuView
from client.views.quiz import QuizView
from client.views.host import HostView


def gameLoop():
    # State control variable
    active_scene = "menu" # default
    # Pygame attributes
    screen_size = (1280, 720)
    clock = pygame.time.Clock() # Controls FPS & tracks time.
    dt = clock.tick(60) / 1000
    pygame.init()
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Menu")
    manager = pygame_gui.UIManager(screen_size)

    network_handler = None
    try:
        network_handler = NetworkClient()
        # Network handling
    except:
        print("There was an error connecting to the server. Check logs.")
        logging.error(f"There was an error connecting to the server. Make sure that" +
                      " server.py is running and verify host/port is configured in config.py", exc_info=True)
    # Views
    menu_view = MenuView(screen, manager, screen_size, dt, network_handler)
    quiz_view = QuizView(screen, manager, screen_size, dt, network_handler)
    host_view = HostView(screen, manager, screen_size, dt, network_handler)


    while True:
        
        if active_scene == "menu":
            menu_view.sceneLoop()
            print("finished menu")
            active_scene = menu_view.scene

        if active_scene == "quiz":
            quiz_view.sceneLoop()
            active_scene = quiz_view.scene

        if active_scene == "host":
            host_view.sceneLoop()
            active_scene = host_view.scene

        if active_scene == "quit":
            network_handler.s.close()
            break

    pygame.quit
    sys.exit()

if __name__=="__main__":
    logging.basicConfig(filename="app.log", level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
    gameLoop()

'''Issue deciding where to place createUI(). If it's placed in if statment, then the program starts choking
and doesn't register inputs. If it's placed in the constructor, then all views are generated and displayed
over each other. Going to look for alternate solutions.'''