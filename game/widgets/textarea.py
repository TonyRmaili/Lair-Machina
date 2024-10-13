import pygame

class TextArea:
    def __init__(self, text, WIDTH, HEIGHT, x=0, y=0, text_color=(255, 255, 255),
                 bg_color=(0, 0, 0), title="", title_color=(255, 255, 255), title_font_size=30, font_size=24):
        """
        A scrollable text area that displays text with a title at the top.
        Cannot be used to input text - only to display it.
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

        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.x = x
        self.y = y

        # Render the initial text
        self.new_text(text)
        self.dragging = False

    def render_text(self, text, WIDTH):
        lines = []
        words = text.split(' ')
        current_line = ""

        for word in words:
            test_line = f"{current_line} {word}".strip()
            if self.font.size(test_line)[0] <= WIDTH - self.scrollbar_w:  # Adjust for scrollbar width
                current_line = test_line
            else:
                # Handle long words that don't fit in a single line
                while self.font.size(word)[0] > WIDTH - self.scrollbar_w:
                    # Break long words
                    part = word[:len(word) // 2]
                    lines.append(part)
                    word = word[len(part):]
                lines.append(current_line)
                current_line = word

        if current_line:
            lines.append(current_line)  # Add the last line
        return lines

    def new_text(self, text):
        """
        Updates the text in the text area and recalculates the scrolling and rendering logic.
        """
        self.text_lines = self.render_text(text=text, WIDTH=self.WIDTH)
        self.scroll_y = 0  # Reset scroll to the top

        # Prevent ZeroDivisionError by ensuring len(self.text_lines) is never zero
        if len(self.text_lines) == 0:
            self.max_scroll = 0
            self.scrollbar_h = self.HEIGHT - self.title_padding  # Scrollbar takes up full height when no scrolling is needed
        else:
            total_text_height = len(self.text_lines) * self.font_size
            visible_height = self.HEIGHT - self.title_padding

            # Ensure we calculate max_scroll correctly, adjusting by font size to ensure the last line shows
            self.max_scroll = max(0, total_text_height - visible_height + self.font_size)

            # Calculate scrollbar height based on content size relative to the visible area
            self.scrollbar_h = max(30, int(visible_height * visible_height / total_text_height))

        # Set scrollbar position and rectangle
        self.scrollbar_rect = pygame.Rect(self.x + self.WIDTH - self.scrollbar_w, self.y + self.title_padding, self.scrollbar_w, self.scrollbar_h)

    def handle_event(self, event):
        text_area_rect = pygame.Rect(self.x, self.y + self.title_padding, self.WIDTH - self.scrollbar_w, self.HEIGHT - self.title_padding)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if text_area_rect.collidepoint(event.pos):
                if event.button == 4:  # Scroll up
                    self.scroll_y -= self.scroll_speed
                if event.button == 5:  # Scroll down
                    self.scroll_y += self.scroll_speed
            if event.button == 1 and self.scrollbar_rect.collidepoint(event.pos):  # Left mouse button
                self.dragging = True

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.dragging = False

        if event.type == pygame.MOUSEMOTION and self.dragging and self.max_scroll > 0:  # Only allow dragging if there is text to scroll
            mouse_y = event.pos[1]
            try:
                self.scrollbar_rect.y = mouse_y - self.scrollbar_h // 2  # Center the scrollbar on the mouse
                self.scrollbar_rect.y = max(self.y + self.title_padding, min(self.scrollbar_rect.y, self.y + self.HEIGHT - self.scrollbar_h))
                self.scroll_y = ((self.scrollbar_rect.y - (self.y + self.title_padding)) / (self.HEIGHT - self.title_padding - self.scrollbar_h)) * self.max_scroll
            except ZeroDivisionError:
                pass

    def draw(self, screen):
        # Draw the title (not clipped)
        pygame.draw.rect(screen, self.bg_color, (self.x, self.y, self.WIDTH, self.HEIGHT))
        if self.title:
            title_surface = self.title_font.render(self.title, True, self.title_color)
            screen.blit(title_surface, (self.x + 10, self.y + 5))

        # Clip the text area (excluding the title) to prevent text from drawing outside the defined area
        clip_rect = pygame.Rect(self.x, self.y + self.title_padding, self.WIDTH - self.scrollbar_w, self.HEIGHT - self.title_padding)
        screen.set_clip(clip_rect)

        self.scroll_y = max(0, min(self.scroll_y, self.max_scroll))

        # Render only lines that are within the visible text area
        for i, line in enumerate(self.text_lines):
            line_pos = i * self.font_size - self.scroll_y + self.title_padding
            if line_pos > self.HEIGHT - self.title_padding:  # Stop rendering if text goes out of the lower bound
                break
            if line_pos + self.font_size < self.title_padding:  # Skip rendering if text is above the top bound
                continue

            text_surface = self.font.render(line, True, self.text_color)
            screen.blit(text_surface, (self.x, self.y + line_pos))

        # Reset the clipping after drawing
        screen.set_clip(None)

        # Draw the scrollbar only if there's content to scroll
        if self.max_scroll > 0:
            pygame.draw.rect(screen, (100, 100, 100), self.scrollbar_rect)
            pygame.draw.rect(screen, (255, 255, 255), self.scrollbar_rect.inflate(-5, -5))
