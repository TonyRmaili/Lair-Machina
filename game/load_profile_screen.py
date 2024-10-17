import pygame
import sys
from widgets.image import Image
from widgets.textarea import TextArea
import os
import json


class LoadProfile:
    def __init__(self,game,w,h):
        self.game = game
        self.bg = Image('./pics/loading_backgroud.webp',pos=(0,0),scale=(w,h))
        # self.bg = Image('./pics/load_profile.webp',pos=(0,0),scale=(w,h))

        self.char = game.char
        
        self.profiles_path = './profiles'

    def scan_folder(self):
        try:
            # List the contents of the specified folder
            contents = os.listdir(self.profiles_path)
            return contents
        except FileNotFoundError:
            return f"Folder '{self.profiles_path}' not found."
        except Exception as e:
            return f"An error occurred: {str(e)}"

    def handle_event(self,events,mouse_pos):
        for event in events:
            # handles quits 
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        
    def run(self,screen,events,mouse_pos):
        self.handle_event(events=events,mouse_pos=mouse_pos)
        self.bg.draw(screen=screen)


def scan_folder():
    path = './profiles'
    profile_names = []
    try:
        names = os.listdir(path)
        for name in names:
            image_path = path+
        
        return profile_names


    except FileNotFoundError:
        return f"Folder '{path}' not found."
    except Exception as e:
        return f"An error occurred: {str(e)}"



if __name__=='__main__':
    content = scan_folder()
    print(content)
        

