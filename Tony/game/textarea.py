import pygame


class TextArea:
    def __init__(self,text,WIDTH,HEIGHT):
        self.font_size = 24
        self.scroll_speed = 20
        self.scrollbar_w = 20

        self.font = pygame.font.Font(None,self.font_size)

    
        self.text_lines = self.render_text(text=text,WIDTH=WIDTH)

        self.scroll_y = 0
        self.max_scroll = max(0, len(self.text_lines) * self.font_size - HEIGHT)
        self.scrollbar_h = max(30, int(HEIGHT * (HEIGHT / (len(self.text_lines) * self.font_size))))
        self.scrollbar_rect = pygame.Rect(WIDTH - self.scrollbar_w, 0, self.scrollbar_w, self.scrollbar_h)

        self.dragging = False
        
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT


    def render_text(self,text,WIDTH):
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
    
    def event_handler(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Scroll up
                self.scroll_y -= self.scroll_speed
            if event.button == 5:  # Scroll down
                self.scroll_y += self.scroll_speed
            # Handle scrollbar dragging
            if event.button == 1 and self.scrollbar_rect.collidepoint(event.pos):  # Left mouse button
                self.dragging = True
                mouse_y = event.pos[1]

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.dragging = False

        if event.type == pygame.MOUSEMOTION and self.dragging:
            mouse_y = event.pos[1]
            self.scrollbar_rect.y = mouse_y - self.scrollbar_h // 2  # Center the scrollbar on the mouse
            # Limit scrollbar movement
            self.scrollbar_rect.y = max(0, min(self.scrollbar_rect.y, self.HEIGHT - self.scrollbar_h))
            # Update scroll_y based on scrollbar position
            self.scroll_y = (self.scrollbar_rect.y / (self.HEIGHT - self.scrollbar_h)) * self.max_scroll


    def display(self,screen):
        self.scroll_y = max(0, min(self.scroll_y, self.max_scroll))
        for i, line in enumerate(self.text_lines):
        # Calculate position
            line_pos = i * self.font_size - self.scroll_y
            if line_pos > self.HEIGHT:  # Stop rendering when the line is off-screen
                break
            if line_pos + self.font_size < 0:  # Skip rendering for lines above the screen
                continue
            
            text_surface = self.font.render(line, True, (255, 255, 255))
            screen.blit(text_surface, (0, line_pos))
        
        pygame.draw.rect(screen, (100, 100, 100), self.scrollbar_rect)  # Scrollbar background
        pygame.draw.rect(screen, (255, 255, 255), self.scrollbar_rect.inflate(-5, -5))  # Scrollbar border