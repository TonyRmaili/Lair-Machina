import pygame

class InputText:
    def __init__(self, x, y, width, height, title, font_size=32, line_limit=20, 
                 bg_color='black', text_color=(0, 0, 0), title_color='black'):
        """
        this is a class that creates a text box for the user to input text
        has formatting options for the text and the box, and can be used in any pygame project
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.title = title
        self.font = pygame.font.Font(None, font_size)
        self.title_font = pygame.font.Font(None, font_size + 8)  # Slightly bigger font for title
        self.bg_color = bg_color
        self.text_color = text_color
        self.title_color = title_color
        self.active = False  # Input box focus state
        self.line_limit = line_limit  # Maximum number of characters per line
        self.lines = [""]  # Store text in multiple lines
        self.scroll_offset = 0  # Scroll offset for text

        # Calculate the visible area for the text (leave room for the title)
        self.text_area_rect = pygame.Rect(x, y + 40, width, height - 40)

    def handle_event(self, events):
        """
        handle the events for the text box - mouse down = active = TRUE, = can type in the box
        """
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Toggle active state when the user clicks inside the text area
                if self.rect.collidepoint(event.pos):
                    self.active = True
                else:
                    self.active = False

            if event.type == pygame.KEYDOWN:
                if self.active:
                    if event.key == pygame.K_RETURN:
                        self.lines.append("")  # Add a new line on Enter
                    elif event.key == pygame.K_BACKSPACE:
                        # Remove character or line if the current line is empty
                        if len(self.lines[-1]) == 0 and len(self.lines) > 1:
                            self.lines.pop()
                        else:
                            self.lines[-1] = self.lines[-1][:-1]  # Remove last character
                    else:
                        self.add_character(event.unicode)

    
    def add_character(self, char):
    # Render the current line to measure its width
        current_line_text = self.lines[-1] + char
        text_surface = self.font.render(current_line_text, True, self.text_color)

        # Allow more space before wrapping to a new line
        margin = 10  # You can adjust this margin to make line breaks happen later
        
        # Check if the current line's width exceeds the text area's width minus the margin
        if text_surface.get_width() > self.text_area_rect.width - margin:
            words = self.lines[-1].split(' ')
            if len(words) > 1:
                # If there are multiple words, move the last word to a new line
                last_word = words.pop()
                self.lines[-1] = ' '.join(words)
                self.lines.append(last_word + char)  # Start a new line with the last word plus the new character
            else:
                # If it's a long single word, just move the entire word to the next line
                self.lines.append(char)
        else:
            # Add the character to the current line if it doesn't exceed the width
            self.lines[-1] += char


    def scroll(self, direction):
        # Scroll up or down by adjusting the scroll offset
        if direction == "up" and self.scroll_offset > 0:
            self.scroll_offset -= 1
        elif direction == "down" and self.scroll_offset < len(self.lines) - 1:
            self.scroll_offset += 1


    def draw(self, screen, events):
        self.handle_event(events)

        # Draw the text area background
        pygame.draw.rect(screen, self.bg_color, self.rect)

        # Draw the title at the top
        title_surface = self.title_font.render(self.title, True, self.title_color)
        screen.blit(title_surface, (self.rect.x, self.rect.y - 35))

        # Draw the text inside the text area with scrolling, and add a small bottom margin
        bottom_margin = 10  # Set the bottom margin to prevent clipping
        visible_lines = (self.text_area_rect.height - bottom_margin) // self.font.get_height()

        for i, line in enumerate(self.lines[self.scroll_offset:self.scroll_offset + visible_lines]):
            text_surface = self.font.render(line, True, self.text_color)
            screen.blit(text_surface, (self.text_area_rect.x + 5, self.text_area_rect.y + 5 + i * self.font.get_height()))

        # Draw the border around the text area
        pygame.draw.rect(screen, self.text_color, self.rect, 2)

        # Scroll the text if necessary
        for event in events:
            if event.type == pygame.MOUSEWHEEL:
                if event.y > 0:
                    self.scroll("up")
                elif event.y < 0:
                    self.scroll("down")


    def format_lines(self):
        return '\n'.join(self.lines)



