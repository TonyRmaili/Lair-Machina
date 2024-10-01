import pygame
import sys
from textarea import TextArea


# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Large Text Scroll Test")

with open('../world_generator/texts/lore.txt', 'r') as file:
    large_text= file.read()


text_area = TextArea(text=large_text,WIDTH=WIDTH,HEIGHT=HEIGHT)



while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        # Handle mouse wheel scrolling
        text_area.event_handler(event=event)

    screen.fill((0, 0, 0))


    text_area.display(screen=screen)

    # Update display
    pygame.display.flip()
