import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FONT_SIZE = 24
SCROLL_SPEED = 20  # Scroll speed for mouse wheel
SCROLLBAR_WIDTH = 20  # Width of the scrollbar

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Large Text Scroll Test")

# Set up font
font = pygame.font.Font(None, FONT_SIZE)

# Create a large amount of text
large_text = "\n".join([f"This is line {i + 1}. This is a lot of text to demonstrate scrolling in Pygame. " * 3 for i in range(100)])  # 100 lines of text

# Function to render text and wrap it
def render_text(text):
    lines = []
    words = text.split(' ')
    current_line = ""

    for word in words:
        test_line = f"{current_line} {word}".strip()
        if font.size(test_line)[0] <= WIDTH - SCROLLBAR_WIDTH:  # Adjust for scrollbar width
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)  # Add the last line
    return lines

# Rendered text lines
text_lines = render_text(large_text)

# Scroll variables
scroll_y = 0
max_scroll = max(0, len(text_lines) * FONT_SIZE - HEIGHT)

# Scrollbar variables
scrollbar_height = max(30, int(HEIGHT * (HEIGHT / (len(text_lines) * FONT_SIZE))))  # Minimum scrollbar height
scrollbar_rect = pygame.Rect(WIDTH - SCROLLBAR_WIDTH, 0, SCROLLBAR_WIDTH, scrollbar_height)

# Initialize dragging variable
dragging = False

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        # Handle mouse wheel scrolling
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Scroll up
                scroll_y -= SCROLL_SPEED
            if event.button == 5:  # Scroll down
                scroll_y += SCROLL_SPEED
            # Handle scrollbar dragging
            if event.button == 1 and scrollbar_rect.collidepoint(event.pos):  # Left mouse button
                dragging = True
                mouse_y = event.pos[1]

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                dragging = False

        if event.type == pygame.MOUSEMOTION and dragging:
            mouse_y = event.pos[1]
            scrollbar_rect.y = mouse_y - scrollbar_height // 2  # Center the scrollbar on the mouse
            # Limit scrollbar movement
            scrollbar_rect.y = max(0, min(scrollbar_rect.y, HEIGHT - scrollbar_height))
            # Update scroll_y based on scrollbar position
            scroll_y = (scrollbar_rect.y / (HEIGHT - scrollbar_height)) * max_scroll

    # Limit scrolling
    scroll_y = max(0, min(scroll_y, max_scroll))

    # Clear screen
    screen.fill((0, 0, 0))

    # Display text with scrolling
    for i, line in enumerate(text_lines):
        # Calculate position
        line_pos = i * FONT_SIZE - scroll_y
        if line_pos > HEIGHT:  # Stop rendering when the line is off-screen
            break
        if line_pos + FONT_SIZE < 0:  # Skip rendering for lines above the screen
            continue
        
        text_surface = font.render(line, True, (255, 255, 255))
        screen.blit(text_surface, (0, line_pos))

    # Draw scrollbar
    pygame.draw.rect(screen, (100, 100, 100), scrollbar_rect)  # Scrollbar background
    pygame.draw.rect(screen, (255, 255, 255), scrollbar_rect.inflate(-5, -5))  # Scrollbar border

    # Update display
    pygame.display.flip()
