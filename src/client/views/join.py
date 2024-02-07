from .base_view import BaseView
import pygame
import pygame_gui

class JoinView(BaseView):

    def __init__(self, screen, manager, screen_size: tuple, dt, network_handler: object, player):
        super().__init__(screen, manager, screen_size, dt)
        self.network_handler = network_handler
        self.game_id = None
        self.player = player
        print("Waiting for game ID.")

    def createUI(self):
        self.join_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, 35), (150, 100)),
                                                      text="Join A Game!",
                                                      container=None,
                                                      manager=self.manager,
                                                      anchors={'centerx': 'centerx'})
        self.gameID_entry = pygame_gui.elements.UITextEntryBox(relative_rect=pygame.Rect((0, 50), (250, 50)),
                                                               initial_text="Enter game ID here...",
                                                               manager=self.manager,
                                                               container=None,
                                                               anchors={'centerx': 'centerx', 'top_target': self.join_label})
        self.submit_bt = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((20, 185), (150, 50)),
                                                      text='SUBMIT',
                                                      manager=self.manager,
                                                      container=None,
                                                      anchors={'left_target': self.gameID_entry})
    
    def killUI(self):
        self.join_label.kill()
        self.gameID_entry.kill()
        self.submit_bt.kill()

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("quitting")
                self.scene = "quit"
                return "quit"
            
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.submit_bt:
                    game_id = self.gameID_entry.get_text()
                    self.player.setGameID(game_id)
                    self.game_id = self.player.getGameID()
                    name = self.player.getName()
                    request = {'type': 'join_request', 'data': [{'game_id': self.game_id, 'name': name}]}
                    self.network_handler.sendRequest(request)
                    print("Submitted game_id")
                    
            self.manager.process_events(event)

        return True

    def handleResponse(self, response):
        if response['status'] == "Success":
            print("Joined game successfully, switching to lobby.")
            self.scene = "lobby"

    def update(self):
        # Will only execute after every 5 frames to limit text effect on game title. 
        if self.frame_counter % 5 == 0:
            self.manager.update(self.dt)
        
        self.frame_counter += 1

    def sceneLoop(self):
        self.network_handler.setCallbackResponse(self.handleResponse)
        self.frame_counter = 0
        self.running = True
        print("Creating UI: JOIN")
        self.createUI()

        while self.running:
            self.dt
            self.running = self.handleEvents()

            if self.scene == "quit":
                return "quit"
            
            if self.scene == "lobby":
                self.killUI()
                return "lobby"
            
            self.update()
            self.draw()
            pygame.display.update()