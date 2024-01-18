import pygame
import pygame_gui
from .base_view import BaseView


class HostView(BaseView):

    def __init__(self, screen, manager, screen_size, dt, network_handler: object):
        super().__init__(screen, manager, screen_size, dt)
        self.gameID = 100010 # Default/testing value
        self.network_handler = network_handler

    def createUI(self):
        self.gameID_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, 35), (150, 50)),
                                                        text=str(self.gameID),
                                                        manager = self.manager,
                                                        container=None,
                                                        anchors={'centerx': 'centerx'})

        self.start_game_bt = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 35), (150, 50)),
                                                          text="Start Game",
                                                          manager=self.manager,
                                                          container=None,
                                                          anchors={'centerx': 'centerx', 'top_target': self.gameID_label})
    
    def killUI(self):
        self.gameID_label.kill()
        self.start_game_bt.kill()

    def handleEvents(self):
        """Checks for specific events and acts accordingly."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("quitting")
                self.scene = "quit"
                return "quit"
            
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.start_game_bt:
                    print("Starting game!")
                    self.scene =  "quiz"
                    return "quiz"

            self.manager.process_events(event)

        return True
    
    def getUniqueID(self):
        "Requests uniqueID from server"
        request = {'type': 'uniqueID'}
        print("requesting unique ID")

        self.network_handler.sendRequest(request)
    
    def sceneLoop(self):
        self.gameID = self.getUniqueID()
        self.running = True
        print("creating UI")
        self.createUI()

        while self.running:
            self.dt
            self.running = self.handleEvents()

            if self.running == "quit":
                return "quit"
            
            if self.running == "quiz":
                self.killUI()
                return
            
            self.update()
            self.draw()
            pygame.display.update()