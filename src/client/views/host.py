import pygame
import pygame_gui
from .base_view import BaseView
import time


class HostView(BaseView):

    def __init__(self, screen, manager, screen_size, dt, network_handler: object, player):
        super().__init__(screen, manager, screen_size, dt)
        self.gameID = None # Default/testing value
        self.player = player
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
        panel_rect = ((0, 200), (500, 350))
        self.chat_panel = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect(panel_rect),
                                                      starting_height=1,
                                                      manager=self.manager,
                                                      container=None,
                                                      anchors={'centerx': 'centerx'})
        x_offset = -6
        y_offset = -5
        self.chat_textbox = pygame_gui.elements.UITextBox(relative_rect=pygame.Rect((x_offset, y_offset), (500, 300)),
                                                          html_text="Lobby Chat",
                                                          manager=self.manager,
                                                          container=self.chat_panel)
        self.chat_textentry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((x_offset, y_offset + 300), (440, 50)),
                                                                  manager=self.manager,
                                                                  container=self.chat_panel)
        self.chat_submit = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((x_offset + 440, y_offset + 300), (60, 50)),
                                                        text="Chat",
                                                        manager=self.manager,
                                                        container=self.chat_panel)

    def killUI(self):
        self.gameID_label.kill()
        self.start_game_bt.kill()
        self.chat_textbox.kill()
        self.chat_textentry.kill()
        self.chat_panel.kill()
        self.chat_submit.kill()

    def handleEvents(self):
        """Checks for specific events and acts accordingly."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("quitting")
                self.scene = "quit"
                return "quit"
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.start_game_bt:
                    request = {'type': 'start_request', 'game_id': self.gameID}
                    self.network_handler.sendRequest(request)
                elif event.ui_element == self.chat_submit:
                    message = self.chat_textentry.get_text()
                    request = {'type': 'chat', 'message': message, 'game_id': self.gameID}
                    self.network_handler.sendRequest(request)
            self.manager.process_events(event)
        return True
    
    def handleResponse(self, response):
        if response['type'] == "uniqueID_response":
            print(f"{response['data'][0]['uniqueID']} From callback.")
            game_id = response['data'][0]['uniqueID']
            self.player.setGameID(game_id)
            self.gameID = self.player.getGameID()
            print(f"Game ID set: {self.gameID}")
        elif response['type'] == "chat_response":
            name = response['data'][0]['name']
            message = response['data'][0]['message']
            history = self.chat_textbox.html_text
            new_chat = f"{history}<br>{name}: {message}"
            self.chat_textbox.set_text(new_chat)
            self.chat_textbox.rebuild()
            self.chat_textbox.starting_height = 1
        elif response['type'] == "start_response":
            self.scene = "quiz"

    def getUniqueID(self):
        "Requests uniqueID from server"
        name = self.player.getName()
        request = {'type': 'uniqueID', 'data': [{'name': name}]}
        print("Requesting unique ID: HOST")
        self.network_handler.sendRequest(request)
        time.sleep(.3)

    def update(self):
        # Will only execute after every 5 frames to limit text effect on game title. 
        if self.frame_counter % 5 == 0:
            self.manager.update(self.dt)
        
        self.frame_counter += 1
    
    def sceneLoop(self):
        self.frame_counter = 0
        self.network_handler.setCallbackResponse(self.handleResponse)
        self.getUniqueID()
        self.running = True
        print("creating UI")
        self.createUI()

        while self.running:
            self.dt
            self.running = self.handleEvents()

            if self.scene == "quit":
                return "quit"
            
            if self.scene == "quiz":
                self.killUI()
                return
            
            self.update()
            self.draw()
            pygame.display.update()