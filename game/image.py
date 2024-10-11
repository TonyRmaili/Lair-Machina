import pygame

class Image():
    def __init__(self, image, pos,anchor='topleft', scale=None):
        """
        used to display images on the screen
        similar to the button class - so that we can have a uniform way of displaying images
        """
        
        self.image = pygame.image.load(image)
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        if scale is not None:
            self.image = pygame.transform.scale(self.image, scale)
        
        self.rect = self.image.get_rect()
        setattr(self.rect, anchor, pos)


    def update(self, screen):
        screen.blit(self.image, self.rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    # def changeImage(self, new_image, scale=None):
    #     """Change the image being displayed."""
    #     self.image = new_image
    #     if scale is not None:
    #         self.image = pygame.transform.scale(self.image, scale)
    #     self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
