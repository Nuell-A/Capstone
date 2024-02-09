import pygame
import pygame_gui
from .base_view import BaseView
import time


class ResultsView(BaseView):
    """Handles all functions related to the Menu view."""

    def __init__(self, screen, manager, screen_size: tuple, dt, network_handler: object, player):
        super().__init__(screen, manager, screen_size, dt)
        self.network_handler = network_handler
        self.player = player
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
        
        self.results_panel = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((0, 120), (200, 500)),
                                                         manager=self.manager,
                                                         container=None,
                                                         starting_height=1,
                                                         anchors={'centerx': 'centerx'})
        x_offset = 10
        y_offset = 10
        spacing = 30

        for player in self.player_info_list:
            name = player['name']
            score = player['score']
            
            self.name_text = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((x_offset, y_offset), (100, 20)),
                                                    text=name,
                                                    manager=self.manager,
                                                    container=self.results_panel)
            self.score_text = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((x_offset + 100, y_offset), (100, 20)),
                                                     text=str(score),
                                                     manager=self.manager,
                                                     container=self.results_panel)
            y_offset += spacing # Spacing for next player
        
        
    def killUI(self):
        self.results_label.kill()
        self.results_panel.kill()

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

    def handleResponse(self, response):
        try:
            if response['type'] == 'get_scores_response':
                    self.player_info_list = response['data'] # 'data' = [{'name': name, 'score': score}]
                    print(self.player_info_list)
        except:
            print("There was an error handling the response. Most likely you already have the data.")


    def getScores(self):
        game_id = self.player.getGameID()
        request = {'type': 'get_scores', 'data': [{'game_id': game_id}]}
        self.network_handler.sendRequest(request)
        time.sleep(.2)

    def update(self):
        self.manager.update(self.dt)
        
    def sceneLoop(self):
        self.network_handler.setCallbackResponse(self.handleResponse)
        self.running = True
        self.getScores()
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