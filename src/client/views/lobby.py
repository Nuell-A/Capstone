from .base_view import BaseView
import pygame
import pygame_gui

class LobbyView(BaseView):

    def __init__(self, screen, manager, screen_size: tuple, dt, network_handler: object):
        super().__init__(screen, manager, screen_size, dt)
        self.network_handler = network_handler
        print("Waiting for host to start.")

    def createUI(self):
        self.lobby_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, 35), (150, 100)),
                                                      text="LOBBY",
                                                      container=None,
                                                      manager=self.manager,
                                                      anchors={'centerx': 'centerx'})
        self.info_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, 50), (600, 50)),
                                                               text="Waiting for host to start the game...",
                                                               manager=self.manager,
                                                               container=None,
                                                               anchors={'centerx': 'centerx', 'top_target': self.lobby_label})
    
    def killUI(self):
        self.lobby_label.kill()
        self.info_label.kill()

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("quitting")
                self.scene = "quit"
                return "quit"
                    
            self.manager.process_events(event)

        return True

    def handleResponse(self, response):
        print(f"In LOBBY: {response}")
        if response['type'] == "start_response":
            print("Host has started the game.")
            self.scene = "quiz"

    def update(self):
        # Will only execute after every 5 frames to limit text effect on game title. 
        if self.frame_counter % 5 == 0:
            self.manager.update(self.dt)
        
        self.frame_counter += 1

    def sceneLoop(self):
        self.network_handler.setCallbackResponse(self.handleResponse)
        self.frame_counter = 0
        self.running = True
        print("Creating UI: LOBBY")
        self.createUI()

        while self.running:
            self.dt
            self.running = self.handleEvents()

            if self.scene == "quit":
                return "quit"
            
            if self.scene == "quiz":
                self.killUI()
                return "quiz"
            
            self.update()
            self.draw()
            pygame.display.update()