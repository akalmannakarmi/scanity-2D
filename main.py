import pygame
from random import randint
from time import sleep,time
from threading import Thread

def update():
    global size,pixel_array,running
    while True:
        # Updating the pixel array surface with the new values
        pixel_array.lock()
        for y in range(size[1]):
            for x in range(size[0]):
                pixel_array.set_at((x, y), (randint(0,255), randint(0,255), randint(0,255)))
        pixel_array.unlock()
        sleep(0.1)

# Initialize Pygame
pygame.init()

# Set the screen size and caption
size = (800, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Nested Array Drawing Example")
clock = pygame.time.Clock()
updateThread = Thread(target=update)

# Create a Pygame surface to hold the pixel data
pixel_array = pygame.Surface((800, 600), depth=24)


# Main game loop
running = True
updateThread.run()
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw the pixel array surface on the screen
    screen.blit(pixel_array, (0, 0))

    # Update the screen
    pygame.display.flip()
    clock.tick(60)
    print(clock.get_fps())

# Quit Pygame
pygame.quit()
