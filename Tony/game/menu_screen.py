import pygame
import pygame_menu
from settings import custom_theme


class MenuScreen:
    def __init__(self,game,w,h) -> None:
        self.game = game

        dark_theme = custom_theme()

        self.menu = pygame_menu.Menu('Welcome Adventurer', w, h,
                                     theme=dark_theme)
        
        self.menu.add.button('New Game', self.new_game)
        self.menu.add.button('Continue', self.continue_game)
        self.menu.add.button('Load Game', self.load_game)
        self.menu.add.button('Quit', pygame_menu.events.EXIT)


    
    def new_game(self):
        self.game.game_mode = 'creation'
        

    def continue_game(self):
        print('continue game')


    def load_game(self):
        print('load game')


    def run(self,screen,events):
        screen.fill('black')
        self.menu.update(events)
        self.menu.draw(screen)