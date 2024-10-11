import pygame

class TextArea:
    def __init__(self, text, WIDTH, HEIGHT, x=0, y=0, text_color=(255, 255, 255),
            bg_color=(0, 0, 0), title="", title_color=(255, 255, 255), title_font_size=30,font_size=24):
        """
        A scrollable text area that displays text with a title at the top.
        cant be used to input text - only to display it
        """
        self.font_size = font_size
        self.scroll_speed = 20
        self.scrollbar_w = 20

        # Create title and title font
        self.title = title
        self.title_font = pygame.font.Font(None, title_font_size)
        self.title_color = title_color

        self.font = pygame.font.Font(None, self.font_size)

        # Allow customization of background and text color
        self.text_color = text_color
        self.bg_color = bg_color

        # Add some padding for the title
        self.title_padding = title_font_size + 10  # Add some space for the title

        # Render the text and account for title padding
        self.text_lines = self.render_text(text=text, WIDTH=WIDTH)

        self.scroll_y = 0
        self.max_scroll = max(0, len(self.text_lines) * self.font_size - (HEIGHT - self.title_padding))
        self.scrollbar_h = max(30, int((HEIGHT - self.title_padding) * (HEIGHT - self.title_padding) / (len(self.text_lines) * self.font_size)))
        self.scrollbar_rect = pygame.Rect(x + WIDTH - self.scrollbar_w, y + self.title_padding, self.scrollbar_w, self.scrollbar_h)

        self.dragging = False

        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.x = x
        self.y = y

    def render_text(self, text, WIDTH):
        lines = []
        words = text.split(' ')
        current_line = ""

        for word in words:
            test_line = f"{current_line} {word}".strip()
            if self.font.size(test_line)[0] <= WIDTH - self.scrollbar_w:  # Adjust for scrollbar width
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word

        if current_line:
            lines.append(current_line)  # Add the last line
        return lines

    def event_handler(self, event):
        # Define the text area as a rectangle, exclude the title area
        text_area_rect = pygame.Rect(self.x, self.y + self.title_padding, self.WIDTH - self.scrollbar_w, self.HEIGHT - self.title_padding)

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the mouse is within the text area before handling scroll
            if text_area_rect.collidepoint(event.pos):
                if event.button == 4:  # Scroll up
                    self.scroll_y -= self.scroll_speed
                if event.button == 5:  # Scroll down
                    self.scroll_y += self.scroll_speed
            # Handle scrollbar dragging
            if event.button == 1 and self.scrollbar_rect.collidepoint(event.pos):  # Left mouse button
                self.dragging = True

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.dragging = False

        if event.type == pygame.MOUSEMOTION and self.dragging:
            mouse_y = event.pos[1]
            self.scrollbar_rect.y = mouse_y - self.scrollbar_h // 2  # Center the scrollbar on the mouse
            # Limit scrollbar movement
            self.scrollbar_rect.y = max(self.y + self.title_padding, min(self.scrollbar_rect.y, self.y + self.HEIGHT - self.scrollbar_h))
            # Update scroll_y based on scrollbar position
            self.scroll_y = ((self.scrollbar_rect.y - (self.y + self.title_padding)) / (self.HEIGHT - self.title_padding - self.scrollbar_h)) * self.max_scroll

    def display(self, screen):
        self.scroll_y = max(0, min(self.scroll_y, self.max_scroll))
        
        # Draw background
        pygame.draw.rect(screen, self.bg_color, (self.x, self.y, self.WIDTH, self.HEIGHT))

        # Draw title
        if self.title:
            title_surface = self.title_font.render(self.title, True, self.title_color)
            screen.blit(title_surface, (self.x + 10, self.y + 5))  # 5px padding from top and left

        # Draw text content
        for i, line in enumerate(self.text_lines):
            # Calculate position, adjust for title padding
            line_pos = i * self.font_size - self.scroll_y + self.title_padding
            if line_pos > self.HEIGHT:  # Stop rendering when the line is off-screen
                break
            if line_pos + self.font_size < self.title_padding:  # Skip rendering for lines above the visible area
                continue

            text_surface = self.font.render(line, True, self.text_color)
            screen.blit(text_surface, (self.x, self.y + line_pos))

        # Scrollbar
        pygame.draw.rect(screen, (100, 100, 100), self.scrollbar_rect)  # Scrollbar background
        pygame.draw.rect(screen, (255, 255, 255), self.scrollbar_rect.inflate(-5, -5))  # Scrollbar border
