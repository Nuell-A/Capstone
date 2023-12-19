import pygame

pygame.init()
running = True
WIDTH, HEIGHT = 1280, 720
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
# Starts in the middle of the screen. 
player_pos = pygame.Vector2(1280/2, 720/2)
clock = pygame.time.Clock() # Controls FPS

dt = 0 # movement modifier

while running:
    # Checks for changes in events.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    SCREEN.fill("blue")

    pygame.draw.circle(SCREEN, "black", player_pos, 35)
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= 300 * dt
    if keys[pygame.K_s]:
        player_pos.y += 300 * dt
    if keys[pygame.K_a]:
        player_pos.x -= 300 * dt
    if keys[pygame.K_d]:
        player_pos.x += 300 * dt

    pygame.display.flip()

    dt = clock.tick(60) / 1000

pygame.quit()