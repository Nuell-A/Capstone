import pygame
import pygame_gui
from pygame_gui.core import ObjectID
import os
from .base_view import BaseView


class MenuView(BaseView):
    """Handles all functions related to the Menu view."""

    def __init__(self, screen, manager, screen_size: tuple, dt, network_handler: object, player):
        super().__init__(screen, manager, screen_size, dt)
        self.player = player
        self.network_handler = network_handler
        print("Running sceneloop: MENU")

    def createUI(self):
        """Creating and position UI elements. Rects are used for positioning relative to
        other elements. """
        # Buttons
        host_rect = pygame.Rect((0, 150), (100, 50))
        join_rect = pygame.Rect((0, 20), (100, 50))
        '''Anchor targets are of the element being placed not the element you're placing next to.
        e.g. in join_bt the top_target is the the top of join_bt to host_bt'''
        self.host_bt = pygame_gui.elements.UIButton(relative_rect=host_rect,
                                                    text='Host',
                                                    manager=self.manager,
                                                    container=None,
                                                    anchors={'centerx': 'centerx'})
        self.join_bt = pygame_gui.elements.UIButton(relative_rect=join_rect,
                                                    text='Join',
                                                    manager=self.manager,
                                                    container=None,
                                                    anchors={'centerx': 'centerx',
                                                             'top_target': self.host_bt})
        # Get the current directory
        current_dir = os.path.dirname(__file__)
        assets_dir = os.path.abspath(os.path.join(current_dir, '..', 'assets'))
        image_path = os.path.join(assets_dir, 'title.png')
        image_surface = pygame.image.load(image_path)
        self.title_img = pygame_gui.elements.UIImage(relative_rect=pygame.Rect((0, 50), (300, 100)),
                                                     image_surface=image_surface,
                                                     manager=self.manager,
                                                     anchors={'centerx': 'centerx'})
        # TextBoxEntry
        self.username_text = pygame_gui.elements.UITextEntryBox(relative_rect=pygame.Rect((0, 80), (250, 50)),
                                                                initial_text="",
                                                                manager=self.manager,
                                                                container=None,
                                                                anchors={'centerx': 'centerx',
                                                                         'top_target': self.join_bt})
        self.username_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, 300), (150, 50)),
                                                          text="Please input name:",
                                                          manager=self.manager,
                                                          container=None,
                                                          anchors={'centerx': 'centerx',})
        
    def killUI(self):
        self.host_bt.kill()
        self.join_bt.kill()
        self.title_img.kill()
        self.username_text.kill()
        self.username_label.kill()

    def handleEvents(self):
        """Checks for specific events and acts accordingly."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("quitting")
                self.scene = "quit"
                return "quit"
            
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.host_bt:
                    print("Hosting session...")
                    name = self.username_text.get_text()
                    if name:
                        self.player.setName(name)
                        print(self.player)
                        self.scene = "host"
                        return "host"
                    else:
                        print("Please enter a name")
                        return True

                elif event.ui_element == self.join_bt:
                    print("Joining session...")
                    name = self.username_text.get_text()
                    if name:
                        self.player.setName(name)
                        print(self.player)
                        self.scene = "join"
                        return "join"
                    else:
                        print("Please enter a name")
                        return True

            self.manager.process_events(event)

        return True

    def update(self):
        # Will only execute after every 5 frames to limit text effect on game title. 
        if self.frame_counter % 5 == 0:
            self.manager.update(self.dt)
        
        self.frame_counter += 1

    def sceneLoop(self):
        self.frame_counter = 0 # Initialized to keep track of frames
        self.running = True
        print("creating UI")
        self.createUI()

        while self.running:
            self.dt
            self.running = self.handleEvents()

            if self.scene == "quit":
                return
            
            if self.scene == "host":
                self.killUI()
                return
            
            if self.scene == "join":
                self.killUI()
                return
            
            self.update()
            self.draw()
            pygame.display.update()