import pygame
import pygame_gui
import time


class MenuView:
    """Handles all functions related to the Menu view."""

    def __init__(self, screen, manager, screen_size: tuple, dt):
        self.scene = None
        self.dt = dt
        self.running = True
        self.screen = screen
        self.manager = manager
        self.screen_size = screen_size
        print("running sceneloop")

    def createUI(self):
        """Creating and position UI elements. Rects are used for positioning relative to
        other elements. """
        # Buttons
        host_rect = pygame.Rect((0, 200), (100, 50))
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
        # TextBox
        self.title_label = pygame_gui.elements.UITextBox(relative_rect=pygame.Rect((0, 50), (150, 100)),
                                                         html_text='<effect id=title>GAME TITLE</effect>',
                                                         manager=self.manager,
                                                         container=None,
                                                         anchors={'centerx': 'centerx'})
        self.title_label.set_active_effect(pygame_gui.TEXT_EFFECT_BOUNCE, effect_tag='title')
        # TextBoxEntry
        self.username_text = pygame_gui.elements.UITextEntryBox(relative_rect=pygame.Rect((0, 80), (250, 50)),
                                                                initial_text="Type user name here.....",
                                                                manager=self.manager,
                                                                container=None,
                                                                anchors={'centerx': 'centerx',
                                                                         'top_target': self.join_bt})
        
    def killUI(self):
        self.host_bt.kill()
        self.join_bt.kill()
        self.title_label.kill()
        self.username_text.kill()

    def handleEvents(self):
        """Checks for specific events and acts accordingly."""
        for event in pygame.event.get():
            print(self.running)
            if event.type == pygame.QUIT:
                print("quitting")
                self.running = "quit"
                return self.running
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.host_bt:
                    print("Hosting session...")
                    self.scene = "quiz"
                    return "quiz"

                elif event.ui_element == self.join_bt:
                    print("Joining session...")

            self.manager.process_events(event)

        return "menu"

    def update(self):
        self.manager.update(self.dt)

    def draw(self):
        background = pygame.Surface(self.screen_size)
        background.fill(pygame.Color('#a575c6'))

        # blit is used to add a surface to the screen.
        self.screen.blit(background, (0, 0))
        self.manager.draw_ui(self.screen)

    def sceneLoop(self):
        self.running = True
        print("creating UI")
        self.createUI()

        while self.running:
            self.dt
            self.running = self.handleEvents()
            print(self.running)
            if self.running == "quit":
                return "quit"
            
            if self.running == "quiz":
                self.killUI()
                print("killed UI")
                return
            
            print(1)
            self.update()
            self.draw()
            print(2)
            pygame.display.update()