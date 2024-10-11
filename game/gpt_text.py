import pygame

# Initialize pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600



import pygame

class TextInputer:
    def __init__(self, x, y, width, height, font_size=32, line_limit=20):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (200, 200, 200)  # Default box color (inactive)
        self.text = ""
        self.font = pygame.font.Font(None, font_size)
        self.active = False  # Is the input box active (focused)?
        self.line_limit = line_limit  # Maximum number of characters per line
        self.lines = [""]  # To store the text in multiple lines

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input box
            if self.rect.collidepoint(event.pos):
                self.active = True  # Toggle active state
                self.color = (255, 255, 255)  # Active color
            else:
                self.active = False
                self.color = (200, 200, 200)  # Inactive color

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.lines)  # For example, print the text when Enter is pressed
                    self.text = ""  # Clear the text box after submission
                    self.lines = [""]
                elif event.key == pygame.K_BACKSPACE:
                    if self.lines[-1] == "" and len(self.lines) > 1:
                        self.lines.pop()  # Remove the last line if empty
                    else:
                        self.lines[-1] = self.lines[-1][:-1]  # Remove last character
                else:
                    self.add_character(event.unicode)

    def add_character(self, char):
        if len(self.lines[-1]) < self.line_limit:
            self.lines[-1] += char
        else:
            self.lines.append(char)  # Start a new line if the limit is exceeded

    def update(self):
        pass

    def draw(self, screen):
        # Draw each line of text in the text box
        for i, line in enumerate(self.lines):
            txt_surface = self.font.render(line, True, (0, 0, 0))
            screen.blit(txt_surface, (self.rect.x + 5, self.rect.y + 5 + i * self.font.get_height()))

        # Draw the input box rectangle
        pygame.draw.rect(screen, self.color, self.rect, 2)


class GameLogic:
    def __init__(self):
        # Set up the screen
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Text Input Example")

        # Create a TextInputer instance
        self.text_inputer = TextInputer(100, 100, 300, 150, font_size=32, line_limit=20)

        # Control the game loop
        self.running = True

    def run(self):
        clock = pygame.time.Clock()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                # Pass events to the text input handler
                self.text_inputer.handle_event(event)

            # Update game logic
            self.text_inputer.update()

            # Draw everything
            self.screen.fill(WHITE)  # Clear the screen
            self.text_inputer.draw(self.screen)  # Draw the text input box

            pygame.display.flip()  # Update the display
            clock.tick(30)  # Limit the frame rate to 30 FPS

        pygame.quit()


if __name__ == "__main__":
    # Create the game logic and start the game loop
    game = GameLogic()
    game.run()
