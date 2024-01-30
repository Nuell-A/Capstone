import pygame
import pygame_gui
from .base_view import BaseView


class ResultsView(BaseView):
    """Handles all functions related to the Menu view."""

    def __init__(self, screen, manager, screen_size: tuple, dt, network_handler: object):
        super().__init__(screen, manager, screen_size, dt)
        self.network_handler = network_handler
        print("Running sceneloop: RESULTS")

    def createUI(self):
        """Creating and positioning UI elements. Rects are used for positioning relative to
        other elements. """
        # TextBox
        self.results_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, 50), (150, 100)),
                                                         text="RESULTS",
                                                         manager=self.manager,
                                                         container=None,
                                                         anchors={'centerx': 'centerx'})
        
        
    def killUI(self):
        self.results_label.kill()

    def handleEvents(self):
        """Checks for specific events and acts accordingly."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("quitting")
                self.scene = "quit"
                return "quit"
            
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == "<button here>":
                    pass
                elif event.ui_element == "<button here2>":
                    pass

            self.manager.process_events(event)

        return True

    def update(self):
        self.manager.update(self.dt)
        
    def sceneLoop(self):
        self.running = True
        print("Creating UI: RESULTS")
        self.createUI()

        while self.running:
            self.dt
            self.running = self.handleEvents()

            if self.running == "quit":
                return "quit"
            
            self.update()
            self.draw()
            pygame.display.update()