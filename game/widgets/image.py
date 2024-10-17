import pygame

class Image():
    def __init__(self, image, pos, anchor='topleft', scale=None, title=None, font_size=24, font_color=(255, 255, 255)):
        """
        Used to display images on the screen with an optional title over the image.
        """
        self.image = pygame.image.load(image)
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.title = title
        self.font_size = font_size
        self.font_color = font_color
        
        # Load and scale the image if needed
        if scale is not None:
            self.image = pygame.transform.scale(self.image, scale)
        
        self.rect = self.image.get_rect()
        setattr(self.rect, anchor, pos)
        
        # Initialize font for the title
        if title:
            pygame.font.init()
            self.font = pygame.font.Font(None, self.font_size)

    def draw(self, screen):
        # Draw the image
        screen.blit(self.image, self.rect)
        
        # Draw the title if it exists
        if self.title:
            title_surface = self.font.render(self.title, True, self.font_color)
            title_rect = title_surface.get_rect(midtop=self.rect.midtop)  # Center the title at the top of the image
            screen.blit(title_surface, title_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False
    
    def check_for_click(self, event):
        """
        Check if the image is clicked by the mouse.
        """
        # Check if the event is a mouse button click
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()  # Get the current mouse position
            # Check if the mouse click is within the image's rectangle
            if self.rect.collidepoint(mouse_pos):
                return True
        return False

    def changeImage(self, new_image, scale=None):
        """Change the image being displayed."""
        self.image = pygame.image.load(new_image)
        if scale is not None:
            self.image = pygame.transform.scale(self.image, scale)
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
