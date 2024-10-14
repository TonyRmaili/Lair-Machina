import pygame
import sys
from widgets.image import Image
from widgets.textarea import TextArea
from widgets.input_text import InputText
from widgets.button import Button
import ollama
import threading

class DungeonSceen:
    """
    needs to be updated to merge with the game_map.py
    """
    def __init__(self,game,w,h):
        self.game = game
        self.char = game.char
        path = './pics/'
        self.bg = Image(image=path+'floor.jpg',pos=(250,0),scale=(w-250,h-250))
        namepath = self.game.char.name
        path = './pics/'+ namepath + '/'

        # THIS NEEDS TO HAVE errorhandling/async - if the img or folder is not created yet
        self.character_image = Image(image=path+'profile_img.png',pos=(w-250,h-250),scale=(250,250))

        self.prompt_box = InputText(x=0,y=h-250,width=w-250,height=h-250,
                        title='prompt box',bg_color=(69, 69, 69), text_color=(255, 255, 255))
        
        self.response_box = TextArea(text='',WIDTH=250,HEIGHT=h-300,x=0,y=0,
                        text_color=(255, 255, 255),bg_color=(69, 69, 69),title='response box',title_color='black')

        self.prompt_button = Button(pos=(w-325,h-275),text_input='Submit',
                image=None,base_color="black", hovering_color="Green",font=pygame.font.Font(None, 36))
        
        # threading attributes
        self.response = None  
        self.is_fetching = False  

    def ask_ollama(self, prompt):
        # This runs in a separate thread, so it won't block the main loop
        self.is_fetching = True  # Mark that we are fetching
        resp = ollama.generate(
            model='llama3.1',
            prompt=prompt
        )
        self.response = resp['response']
        self.is_fetching = False  # Mark that fetching is done


    def update_response(self):
        # Check if there's a new response and update the response box
        if self.response:
            self.response_box.new_text(text=self.response)
            self.response = None  # Clear the response after updating the box

    def handle_event(self,events,mouse_pos):
        self.prompt_button.changeColor(position=mouse_pos)
        for event in events:
            # handles quits 
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:                
                if event.key == pygame.K_q:
                    self.game.game_mode = 'menu'
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.prompt_button.checkForInput(mouse_pos) and not self.is_fetching:
                    prompt = self.prompt_box.send_text()
                    # Start a new thread for the LLM request
                    threading.Thread(target=self.ask_ollama, args=(prompt,)).start()

            self.response_box.handle_event(event=event)

    def run(self,screen,events,mouse_pos):
        self.handle_event(events=events,mouse_pos=mouse_pos)
        self.update_response()
        self.bg.draw(screen=screen)

        self.character_image.draw(screen=screen)
        self.prompt_box.draw(screen=screen,events=events)
        self.response_box.draw(screen=screen)
        self.prompt_button.draw(screen=screen)




        

       
        
        



