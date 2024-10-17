import pygame
import pygame_menu
import sys
from widgets.image import Image
from widgets.textarea import TextArea
from widgets.input_text import InputText
from character import Character
from settings import custom_theme


class CreactionScreen:
    """
    This class is responsible for the character creation screen - it allows the player to create a character and saves the data
    """
    def __init__(self,game,w,h):
        path = './pics/'
        self.bg = Image(image=path+'char_creation_bg.jpg',pos=(0,0),scale=(w,h))
        self.game = game

        self.char_menu,self.menu_rect = self.create_char_menu(w,h)
         
        self.char = self.game.char

        self.char.name = 'Traveler'
        self.char.klass = 'Fighter'
        self.char.race = 'Human'

        self.description_box = InputText(550, 50, 300, 200, title="Description", font_size=24, 
                bg_color=(69, 69, 69), text_color=(255, 255, 255), title_color=(255, 255, 255))

       
    
    def create_char_menu(self,w,h):
        theme = custom_theme(theme_name='THEME_BLUE')

        menu = pygame_menu.Menu('Create Character', w//2, h//2,
                        theme=theme,position=(0,0))
        
        rect = pygame.Rect(0, 0, w//2, h//2)
        
        menu.add.text_input('Name :', default='Traveler',maxchar=20, 
                                              onchange=self.set_name)
        
        menu.add.selector('Class :', [('Fighter', 1), ('Wizard', 2)], onchange=self.set_class)
        menu.add.selector('Race :', [('Human', 1), ('Elf', 2),('Dwarf',3)], onchange=self.set_race)

        menu.add.button('Play', self.start_game)
        return menu,rect

    def start_game(self):
        print(self.char.name)
        print(self.char.klass)
        print(self.char.race)

        self.char.description = self.description_box.format_lines()
        print(self.char.description)
        
        self.game.game_mode ='loading'
        # self.game.loading_screen.img_generator()
        # self.game.game_mode = 'map'



    def set_name(self,name):
        self.char.name = name
       
    def set_class(self, selected_value, index):
        selected_class, class_id = selected_value
        self.char.klass = selected_class[0]
        
    def set_race(self, selected_value, index):
        selected_race, race_id = selected_value
        self.char.race = selected_race[0]
           
    def handle_event(self,events):
        for event in events:
            # handles quits 
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
                             
    def run(self,screen,events,mouse_pos):
        self.handle_event(events)
        self.bg.draw(screen=screen)

        # Only update and draw the menu if the mouse is over it
        if self.menu_rect.collidepoint(mouse_pos):
            self.char_menu.update(events=events)

        
        self.char_menu.draw(screen)
        self.description_box.draw(screen=screen,events=events)
       
        