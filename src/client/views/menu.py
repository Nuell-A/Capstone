import pygame
import pygame_gui

WIDTH, HEIGHT = 1280, 720
class MenuView:
    '''Handles all functions related to the Menu view.'''
    def __init__(self, screen, manager):
        
        self.screen = screen
        self.manager = manager
        self.createUI(WIDTH, HEIGHT)

    def createUI(self, WIDTH, HEIGHT):
        '''Creating and positiong UI elements. Rects are used for positioning relative to
        other elements. '''
        # Buttons
        host_rect = pygame.Rect((0,200), (100, 50))
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
                                                html_text='<h1><effect id=title>GAME TITLE</effect></h1>',
                                                manager=self.manager,
                                                container=None,
                                                anchors={'centerx': 'centerx'})
        self.title_label.set_active_effect(pygame_gui.TEXT_EFFECT_BOUNCE, effect_tag='title')
        # TextBoxEntry
        self.usrname_text = pygame_gui.elements.UITextEntryBox(relative_rect=pygame.Rect((0,80), (250, 50)),
                                                        initial_text="Type user name here.....",
                                                        manager=self.manager,
                                                        container=None,
                                                        anchors={'centerx': 'centerx', 
                                                                'top_target': self.join_bt})

    def handleEvents(self, event):
        '''Checks for specific events and acts accordingly.'''
        for event in pygame.event.get():
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.host_bt:
                    print("Hosting session...")
            
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.join_bt:
                    print("Joining session...")

        self.manager.process_events(event)

    def update(self, dt):
        self.manager.update(dt)

    def draw(self, WIDTH, HEIGHT):
        background = pygame.Surface((WIDTH, HEIGHT))
        background.fill(pygame.Color('#a575c6'))

        # blit is used to add a surface to the screen.
        self.screen.blit(background, (0, 0))
        self.manager.draw_ui(self.screen)

def main():      
    running = True
    clock = pygame.time.Clock() # Controls FPS and tracks time.
    # dt = delta
    dt = 0 

    pygame.init()
    pygame.display.set_caption("Menu")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    manager = pygame_gui.UIManager((WIDTH, HEIGHT))

    menu_view = MenuView(screen, manager)
    
    while running:
        dt = clock.tick(30) / 1000 # Limited to 30 FPS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    running = False

            menu_view.handleEvents(event)
        
        menu_view.update(dt)
        menu_view.draw(WIDTH, HEIGHT)
        pygame.display.update() # Updates the whole screen (if no argument is passed).

    pygame.quit()

if __name__ == "__main__":
    main()