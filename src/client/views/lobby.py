from .base_view import BaseView
import pygame
import pygame_gui

class LobbyView(BaseView):

    def __init__(self, screen, manager, screen_size: tuple, dt, network_handler: object, player):
        super().__init__(screen, manager, screen_size, dt)
        self.network_handler = network_handler
        self.player = player

    def createUI(self):
        self.lobby_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, 35), (150, 100)),
                                                      text="LOBBY",
                                                      container=None,
                                                      manager=self.manager,
                                                      anchors={'centerx': 'centerx'})
        self.info_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, 25), (600, 50)),
                                                               text="Waiting for host to start the game...",
                                                               manager=self.manager,
                                                               container=None,
                                                               anchors={'centerx': 'centerx', 'top_target': self.lobby_label})
        
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
        self.lobby_label.kill()
        self.info_label.kill()
        self.chat_textbox.kill()
        self.chat_textentry.kill()
        self.chat_panel.kill()
        self.chat_submit.kill()

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("quitting")
                self.scene = "quit"
                return "quit"
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.chat_submit:
                    message = self.chat_textentry.get_text()
                    self.game_id = self.player.getGameID()
                    request = {'type': 'chat', 'message': message, 'game_id': self.game_id}
                    self.network_handler.sendRequest(request)
            self.manager.process_events(event)

        return True

    def handleResponse(self, response):
        print(f"In LOBBY: {response}")
        if response['type'] == "start_response":
            print("Host has started the game.")
            self.scene = "quiz"
        elif response['type'] == "chat_response":
            name = response['data'][0]['name']
            message = response['data'][0]['message']
            history = self.chat_textbox.html_text
            new_chat = f"{history}<br>{name}: {message}"
            self.chat_textbox.set_text(new_chat)
            self.chat_textbox.rebuild()
            self.chat_textbox.starting_height = 1

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