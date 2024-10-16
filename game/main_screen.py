import pygame
import sys
from debug import debug
import os
from creation_screen import CreactionScreen
from menu_screen import MenuScreen
from dungeon_screen import DungeonScreen
from loading_screen import LoadingScreen
from load_profile_screen import LoadProfile
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from character import Character
# from game_map import GameMap

class Game:
    def __init__(self):
        """
        this is the main game class
        will have all game modes/ screens etc in it, import it (game) in every screen to get the size etc
        """
        # setup
        self.FPS = 60
        self.WIDTH = 945
        self.HEIGHT = 650
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()
        
        self.char = Character()
        
        pygame.display.set_caption("Lair Machina")

        self.game_mode = 'menu'

        # screens
        self.creation_screen = CreactionScreen(game=self,w=self.WIDTH,h=self.HEIGHT)
        self.menu_screen = MenuScreen(game=self,w=self.WIDTH,h=self.HEIGHT)
        self.dungeon_screen = None
        self.loading_screen = LoadingScreen(game=self,w=self.WIDTH,h=self.HEIGHT)
        self.load_profile_screen = LoadProfile(game=self,w=self.WIDTH,h=self.HEIGHT)
        
    
    def run(self):
        while True:  
            events = pygame.event.get()
            mouse_pos = pygame.mouse.get_pos()
            self.screen.fill('white')  

            
            if self.game_mode == 'menu':
                self.menu_screen.run(screen=self.screen,events=events)

            elif self.game_mode == 'creation':
                self.creation_screen.run(screen=self.screen,events=events,mouse_pos=mouse_pos)

            elif self.game_mode == 'dungeon':
                if self.dungeon_screen is None:
                    self.dungeon_screen = DungeonScreen(game=self, w=self.WIDTH, h=self.HEIGHT)
                self.dungeon_screen.run(screen=self.screen,events=events,mouse_pos=mouse_pos)
                
            elif self.game_mode == 'load_profile':
                self.load_profile_screen.run(screen=self.screen,events=events,mouse_pos=mouse_pos)
                
            elif self.game_mode == 'loading':
                self.loading_screen.run(screen=self.screen,events=events,mouse_pos=mouse_pos)

            
            pygame.display.flip()           
            self.clock.tick(self.FPS)

   
if __name__ == '__main__':
    game = Game()
    game.run()