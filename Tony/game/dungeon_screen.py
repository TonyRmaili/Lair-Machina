import pygame
import sys
from image import Image




class DungeonSceen:
    def __init__(self,game,w,h):
        path = './pics/'
        pygame.display.set_caption("Lair Machina: Dungeon")

        self.bg = Image(image=path+'floor.jpg',pos=(0,0),scale=(w,h))
        self.character_image = Image(image=path+'garry.jpg',pos=(400,400),scale=(150,150))

        self.game = game


    def handle_event(self,events):
        for event in events:
            # handles quits 
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:                
                if event.key == pygame.K_q:
                    self.game.game_mode = 'menu'

    def run(self,screen,events):
        self.handle_event(events=events)
        
        self.bg.update(screen=screen)

        self.character_image.update(screen=screen)

        

       
        
        



