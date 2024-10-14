import pygame
import sys
from widgets.image import Image
from widgets.textarea import TextArea
from widgets.input_text import InputText
from widgets.button import Button
import time
import threading
from comfy_prompt import run_in_thread, image_generation_event
import os


class LoadingScreen:
    def __init__(self,game,w,h):
        self.game = game
        self.bg = Image('./pics/loading_backgroud.webp',pos=(0,0),scale=(w,h-200))
        self.char = game.char
        self.terminal_box = TextArea(text='',WIDTH=w,HEIGHT=200,x=0,y=h-200,
            text_color=(255, 255, 255),bg_color=(69, 69, 69),title='Terminal',title_color='black')

        self.loading_complete = False

    def img_generator(self):
        run_in_thread(self.char.description, self.char.name)
        image_path = f'./pics/{self.char.name}/profile_img.png'

        # Continuously check if the image has been generated
        while not os.path.exists(image_path):
            print("Waiting for image generation...")
            time.sleep(1)  # Sleep for a short duration before checking again
            # Wait for the image generation to complete
        
        
        print("Image has been generated!")
        self.char.image = f'./pics/{self.char.name}/profile_img.png'
        self.loading_complete = True
            

    # def start_image_generation(self):
    #     threading.Thread(target=self.img_generator).start() 


    def handle_event(self,events,mouse_pos):
        for event in events:
            # handles quits 
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            self.terminal_box.handle_event(event=event)

    
    def run(self,screen,events,mouse_pos):
        self.handle_event(events=events,mouse_pos=mouse_pos)
        self.bg.draw(screen=screen)
        self.terminal_box.draw(screen=screen)

        if self.loading_complete:
            self.game.game_mode ='dungeon'
        

