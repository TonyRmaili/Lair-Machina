import pygame
import sys
from widgets.image import Image
import os
import json


class LoadProfile:
    def __init__(self,game,w,h):
        self.game = game
        # self.bg = Image('./pics/loading_backgroud.webp',pos=(0,0),scale=(w,h))
        self.bg = Image('./pics/load_profile.webp',pos=(0,0),scale=(w,h))

        self.char = game.char
        
        self.profiles_path = './profiles/'

        self.scan_folder()

    def scan_folder(self):
        self.images = []
        try:
            # List the contents of the specified folder
            names = os.listdir(self.profiles_path)
            counter = 0
            for name in names:
                image_path = self.profiles_path+name+'/profile_img.png'

                image = Image(image=image_path,pos=(300+counter,100),scale=(100,120),title=name,font_color='black')
                counter +=200

                self.images.append(image)

        except FileNotFoundError:
            return f"Folder '{self.profiles_path}' not found."
        except Exception as e:
            return f"An error occurred: {str(e)}"


    def select_profile(self,name):
        with open(self.profiles_path+'/'+name+'/save_file.json', 'r') as json_file:
            data = json.load(json_file)
        
        self.char.__dict__.update(data)
        self.game.game_mode = 'dungeon'

    def handle_event(self,events,mouse_pos):
        for event in events:
            # handles quits 
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            for image in self.images:
                if image.check_for_click(event):
                    self.select_profile(name=image.title)
        
    def run(self,screen,events,mouse_pos):
        self.handle_event(events=events,mouse_pos=mouse_pos)
        self.bg.draw(screen=screen)

        for image in self.images:
            image.draw(screen)
