import pygame
import threading
from time import time,sleep
from random import randint
import queue

# Initialize Pygame
pygame.init()

# Set the screen size and caption
size = (800, 600)
scale = (8,8)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Nested Array Drawing Example")
clock = pygame.time.Clock()

# Create a queue to hold the pixel data
pixel_data_queue = queue.Queue()

# Create a Pygame surface to hold the pixel data
pixel_array = pygame.Surface((int(size[0]/scale[0]),int(size[1]/scale[1])), depth=24)

# Define a function to update the pixel values in the nested array
def update_pixel_values():
    global running,pixel_data_queue
    while running:
        # Update the pixel values in the nested array
        nested_array = [[(randint(0,255), randint(0,255), randint(0,255)) for _ in range(int(800/scale[0]))] for _ in range(int(600/scale[1]))]
        pixel_data_queue.put(nested_array)

# Create a separate thread to run the update_pixel_values function
update_thread = threading.Thread(target=update_pixel_values)

# Main game loop
update = time()
running = True
update_thread.start()
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            update_thread.join()

    # Get the pixel data from the queue
    try:
        nested_array = pixel_data_queue.get(block=False)
    except queue.Empty:
        pass
    else:
        fps = 0
        if time()- update !=0:
            fps = int(1/(time()-update))
        update=time()
        print(fps)
        # Update the pixel array surface with the new pixel data
        pixel_array.lock()
        for y, row in enumerate(nested_array):
            for x, value in enumerate(row):
                pixel_array.set_at((x, y), value)
        pixel_array.unlock()

    # Draw the pixel array surface on the screen
    scaled_pixel_array = pygame.transform.scale(pixel_array,(800,600))
    screen.blit(scaled_pixel_array, (0,0))

    # Update the screen
    pygame.display.flip()
    clock.tick(60)
    # print(clock.get_fps())

# Quit Pygame
pygame.quit()
