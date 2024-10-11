import pygame
import pygame_menu
import sys

import pygame_menu.widgets
import pygame_menu.widgets.widget
import pygame_menu.widgets.widget.scrollbar
from debug import debug
import os
from textarea import TextArea
from button import Button
from image import Image
from game.character_screen import CharCreactionScreen


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from world_generator.generate_world import GenerateWorld
from world_generator.define_world import save_to_json, room


###OLD! DONT LOOK HERE - WILL BE DELETED AFTER - threading logic has been looted

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

        
        
        # starter menu init
        self.menu = pygame_menu.Menu('Welcome Adventurer', self.WIDTH, self.HEIGHT,
                                     theme=pygame_menu.themes.THEME_DARK)
        
        self.menu.add.text_input('Name :', default='Traveler', onchange=self.set_name)
        self.menu.add.selector('Class :', [('Fighter', 1), ('Wizard', 2)], onchange=self.set_class)
        self.menu.add.selector('Race :', [('Human', 1), ('Elf', 2),('Dwarf',3)], onchange=self.set_race)
        self.menu.add.text_input('Character description :' ,default='', onchange=self.set_description,maxwidth=10)

        self.menu.add.button('Play', self.start_the_game)
        self.menu.add.button('Quit', pygame_menu.events.EXIT)

        self.bg = CharCreactionScreen(pos=(0,0),scale=(self.WIDTH,self.HEIGHT))
    
        self.game_active = False

        # character data
        self.char_name = None
        self.char_class = None
        self.class_id = None
        self.char_description = None
        self.char_race = None
        self.race_id = None

        # text generation
        save_to_json(data=room, file_name='room_blueprint.json')
        self.gen_world = GenerateWorld()
        self.texts_ready = False
        

        with open('../world_generator/texts/lore.txt', 'r') as file:
            self.lore_text = file.read()
            
        with open('../world_generator/texts/factions.txt', 'r') as file:
            self.factions_text = file.read()


        self.lore_area = TextArea(text=self.lore_text,
                                  WIDTH=self.WIDTH//2,
                                  HEIGHT=self.HEIGHT//2,
                                  x=self.WIDTH//2, title='Lore')
        
        self.faction_area = TextArea(text=self.factions_text,
                                  WIDTH=self.WIDTH//2 -30,
                                  HEIGHT=self.HEIGHT//2,
                                  x=0, title='Factions',title_color='red'
                                  )
        
        self.test_button = Button(image=None, pos=(400,400),
            text_input='test',font=pygame.font.Font(None, 30),
            base_color='blue',hovering_color='green')
        


        self.image = Image(
            image='./pics/garry.jpg',
            pos=(500,500),
            scale=(50,50)

        )

    def start_text_generation(self):
        # Start text generation in a separate thread
        self.gen_world.run_in_thread()

    def world_lore(self):
        self.lore_area.display(screen=self.screen)
        self.faction_area.display(screen=self.screen)
        

    def set_description(self, text):
        self.char_description = text
        print(f"Character description: {self.char_description}")


    def set_name(self, name):
        self.char_name = name  # Assign the name to a self variable
        print(f"Name set to: {self.char_name}")

    def set_class(self, selected_value, index):
        selected_class, class_id = selected_value
        self.char_class = selected_class[0]
        self.class_id = class_id
        print(f"Selected Class: {self.char_class} (ID: {self.class_id})")

    
    def set_race(self, selected_value, index):
        selected_race, race_id = selected_value
        self.char_race = selected_race[0]
        self.race_id = race_id
        print(f"Selected Race: {self.char_race} (ID: {self.race_id})")



    def start_the_game(self):
        self.game_active = True
        # self.start_text_generation()

    def run(self):
        while True:
            events = pygame.event.get()
            mouse_pos = pygame.mouse.get_pos()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # change screen on 'q' press
                if self.game_active:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                        self.game_active = False


                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.test_button.checkForInput(mouse_pos):
                            print('test button')
                        if self.image.checkForInput(mouse_pos):
                            print('garryu')
                            
                    self.lore_area.event_handler(event=event)
                    self.faction_area.event_handler(event=event)
                    

            if self.game_active:
                self.screen.fill('grey')
                if self.texts_ready:
                    # Lore is ready, show it
                    self.bg.run(screen=self.screen)
                    self.world_lore()
                    self.test_button.changeColor(mouse_pos)
                    self.test_button.update(screen=self.screen)
                    self.image.update(screen=self.screen)
                else:
                    # Show some loading message or animation while generating
                    loading_menu = pygame_menu.Menu('Loading World...', self.WIDTH, self.HEIGHT,
                                                    theme=pygame_menu.themes.THEME_GREEN)
                    loading_menu.add.label('Generating world, please wait...', font_size=25)
                    loading_menu.update(events)
                    loading_menu.draw(self.screen)

                
                pygame.display.update()
                # Add your game logic here

            else:
                # Instead of menu.mainloop(), update and draw the menu manually
                self.screen.fill('black')
                self.menu.update(events)
                self.menu.draw(self.screen)



            # debug(f'Game State: {self.game_active}', (10, 10))
            # debug(f'Name: {self.char_name}', (10, 30))
            # debug(f'Class: {self.char_class}', (10, 50))
            # debug(f'Race: {self.char_race}', (10, 70))
            # debug(f'text rdy: {self.texts_ready}', (10, 90))
            # debug(f'is generating: {self.gen_world.is_generating}', (10, 110))


            pygame.display.flip()
            self.clock.tick(self.FPS)

            if not self.gen_world.is_generating:
                self.texts_ready = True
            # else:
            #     self.texts_ready = False


if __name__ == '__main__':
    game = Game()
    game.run()


 