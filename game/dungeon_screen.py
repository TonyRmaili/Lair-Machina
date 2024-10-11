import pygame
import sys
from image import Image


class DungeonSceen:
    """
    needs to be updated to merge with the game_map.py
    """
    def __init__(self,game,w,h):
        self.game = game
        
        pygame.display.set_caption("Lair Machina: Dungeon")
        
        path = './game/pics/'
        self.bg = Image(image=path+'floor.jpg',pos=(0,0),scale=(w,h))
        namepath = self.game.char.name
        path = './game/pics/'+ namepath + '/'
        # THIS NEEDS TO HAVE errorhandling/async - if the img or folder is not created yet
        self.character_image = Image(image=path+'ComfyUI_00019_.png',pos=(400,400),scale=(150,150))


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

        

       
        
        



