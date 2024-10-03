import pygame
import pygame_menu
import sys
from debug import debug
import os
from textarea import TextArea
from button import Button
from image import Image
from character_creation import CreactionScreen
from menu_screen import MenuScreen

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from world_generator.generate_world import GenerateWorld
from world_generator.define_world import save_to_json, room



class Game:
    def __init__(self):
        # setup
        self.FPS = 60
        self.WIDTH = 800
        self.HEIGHT = 600
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()

        pygame.display.set_caption("Lair Machina")

        self.game_mode = 'menu'

        self.creation_screen = CreactionScreen(game=self,w=self.WIDTH,h=self.HEIGHT)
        self.menu_screen = MenuScreen(game=self,w=self.WIDTH,h=self.HEIGHT)

    def run(self):
        while True:  
            events = pygame.event.get()
            self.screen.fill('white')  

            
            if self.game_mode == 'menu':
                self.menu_screen.run(screen=self.screen,events=events)

            elif self.game_mode == 'creation':
                self.creation_screen.run(screen=self.screen,events=events)

                                      
            pygame.display.flip()           
            self.clock.tick(self.FPS)

   
if __name__ == '__main__':
    game = Game()
    game.run()