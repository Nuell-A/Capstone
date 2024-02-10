import pygame

class BaseView:

    def __init__(self, screen, manager, screen_size: tuple, dt):
        self.scene = None
        self.running = True
        self.dt = dt
        self.screen = screen
        self.manager = manager
        self.screen_size = screen_size

    def update(self):
        self.manager.update(self.dt)

    def draw(self):
        background = pygame.Surface(self.screen_size)
        background.fill(pygame.Color(255, 175, 204))

        # Blit to add background (Surface) to screen
        self.screen.blit(background, (0, 0))
        self.manager.draw_ui(self.screen) # Adds UI elements to screen