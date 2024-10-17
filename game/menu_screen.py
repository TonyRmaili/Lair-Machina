import pygame_menu
from settings import custom_theme
import json
class MenuScreen:
    def __init__(self,game,w,h):
        self.game = game
        self.char = game.char
        dark_theme = custom_theme()

        self.menu = pygame_menu.Menu('Welcome Adventurer', w, h,
                                     theme=dark_theme)
        
        self.menu.add.button('New Game', self.new_game)
        self.menu.add.button('Continue', self.continue_game)
        self.menu.add.button('Load Game', self.load_game)
        self.menu.add.button('Quit', pygame_menu.events.EXIT)


    def load_profile(self,filename="character_profile.json"):
        # with open(filename, 'r') as json_file:
        #     data = json.load(json_file)
        
        # self.char.__dict__.update(data)
        self.game.game_mode = 'load_profile'
        
    
    def new_game(self):
        self.game.game_mode = 'creation'
        
    def continue_game(self):
        self.load_profile()
        self.game.game_mode = 'dungeon'

    def load_game(self):
        self.game.game_mode = 'load_profile'

    def run(self,screen,events):
        screen.fill('black')
        self.menu.update(events)
        self.menu.draw(screen)
        