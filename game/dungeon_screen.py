import pygame
import sys
from widgets.image import Image
from widgets.textarea import TextArea
from widgets.input_text import InputText
from widgets.button import Button
import ollama
import threading

import json


sys.path.append('../function_calls/')  # Adjust the path
from ollama_tools_v2 import OllamaToolCall  # Import your LLaMA tool function

# # Define a Room class to represent each room
# class Room:
#     def __init__(self, name, description, connections, special=None):
        
        
#         self.name = name  # Room name
#         self.description = description  # Room description
#         self.connections = connections  # Dictionary mapping directions (e.g., 'north') to connected rooms
#         self.special = special  # Special feature (e.g., 'exit', 'up-floor', 'down-floor')
#         # self.output_text ='DEBUGG'


class DungeonSceen:
    """
    needs to be updated to merge with the game_map.py
    """
    def __init__(self,game,w,h):
        self.game = game
        self.WIDTH = w
        path = './pics/'
        self.bg = Image(image=path+'floor.jpg',pos=(250,0),scale=(w-250,h-250))
        namepath = self.game.char.name
        path = './pics/'+ namepath + '/'
        # THIS NEEDS TO HAVE errorhandling/async - if the img or folder is not created yet
        self.character_image = Image(image=path+'ComfyUI_00019_.png',pos=(w-250,h-250),scale=(250,250))

        self.prompt_box = InputText(x=0,y=h-250,width=w-250,height=h-250,title='prompt box',bg_color=(69, 69, 69), text_color=(255, 255, 255))
        self.response_box = TextArea(text='',WIDTH=250,HEIGHT=h-300,x=0,y=0,text_color=(255, 255, 255),bg_color=(69, 69, 69),title='response box',title_color='black')
        

        self.prompt_button = Button(pos=(w-325,h-275),text_input='Submit',image=None,base_color="black", hovering_color="Green",font=pygame.font.Font(None, 36)) 
        
        

        #set starting- current room
        self.current_room_id = 0

        with open('../world_generator/dungeon.json') as f:
            self.dungeon = json.load(f)
        
        self.current_room_data = self.dungeon['rooms'][self.current_room_id]
        self.current_room_name = self.dungeon['rooms'][self.current_room_id]['name']
        self.current_room_description = self.dungeon['rooms'][self.current_room_id]['description']

        # Game state: track the current room and position in the grid
        self.player_move_options = self.dungeon['rooms'][self.current_room_id]['connections']  # move options from current in the map
        self.player_position = self.dungeon['rooms'][self.current_room_id]['coordinates']  # Starting position in the map (Room 1)
        self.special_action_available = None  # To track if a special action is available
        self.game_exit = False  # Flag to handle game exit


        self.current_room_box = TextArea(text='',WIDTH=250,HEIGHT=250,x=0,y=0,text_color=(255, 255, 255),bg_color=(69, 69, 69),title=self.current_room_name,title_color='black')


        # print(self.dungeon['rooms'][self.current_room_id]['name'])
        # print(self.dungeon['rooms'][self.current_room_id]['description'])
        
        # self.current_room = self.dungeon[self.current_room_id]
        
        # print(self.current_room)
        
        
        # threading attributes
        self.response = None  
        self.is_fetching = False  


    def display_current_room(self):
        
        # # Display the current room's name and description
        # self.game.screen.fill((0, 0, 0))  # Clear screen with black
        # font = pygame.font.Font(None, 36)
        # text_surface = font.render(f"You are in {self.current_room_name}", True, (255, 255, 255))
        # self.game.screen.blit(text_surface, (50, 50))

        # description_surface = font.render(self.current_room_description, True, (255, 255, 255))
        # self.game.screen.blit(description_surface, (50, 100))

        # Display instructions if a special action is available
        if self.special_action_available:
            action_text = "Press 'U' to "
            if self.special_action_available == 'exit':
                action_text += "exit"
            elif self.special_action_available == 'up-floor':
                action_text += "go up"
            elif self.special_action_available == 'down-floor':
                action_text += "go down"
            action_surface = font.render(action_text, True, (255, 255, 0))  # Yellow text
            self.game.screen.blit(action_surface, (50, 150))





    def display_map(self):
        # displays the map in the top right corner - from the JSON file
        with open('../world_generator/dungeon_map.json') as f:
            self.map_grid = json.load(f)

        # Display the map in the top-right corner
        font = pygame.font.Font(None, 24)
        cell_size = 20  # Cell size for better fit
        grid_offset_x = self.WIDTH - 150  # X offset for where the grid will be displayed
        grid_offset_y = 50  # Y offset for where the grid will be displayed

        for row_idx, row in enumerate(self.map_grid):
            row_text = ''
            for col_idx, cell in enumerate(row):
                # Check if this is the player's position and mark it with 'X'
                if [col_idx, row_idx] == self.player_position:
                    cell_text = 'X'
                else:
                    cell_text = cell
                row_text += cell_text + ' '
            # Render the row text
            text_surface = font.render(row_text, True, (0, 0, 0))
            self.game.screen.blit(text_surface, (grid_offset_x, grid_offset_y + row_idx * cell_size))


    def update_map(self):
        # Update the map grid based on the current room and position
        # self.map_grid.new_text(text=)
        pass


    def ask_ollama_tools(self, prompt):
        # # we need to have it so each room has its own json file - 
        # '../world_generator/dungeon.json'
        # using wrong room file now


        # not sure if works with threading 
        # self.is_fetching = True  # Mark that we are fetching

        # NOW IT WORKS ATLEAST - but needs to take the current room? otherwise too much bullshit?
        
        ollama_instance = OllamaToolCall(messages=prompt, room_file='castle_map.json')
        self.response = ollama_instance.activate_functions()
        # self.is_fetching = False  # Mark that fetching is done
        
        self.response_box.new_text(text=self.response)
        self.response = None  # Clear the response after updating the box


        # This runs in a separate thread, so it won't block the main loop
        # self.is_fetching = True  # Mark that we are fetching
        # resp = ollama.generate(
        #     model='llama3.1',
        #     prompt=prompt
        # )
        # self.response = resp['response']
        # self.is_fetching = False  # Mark that fetching is done
        

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
                    
                    threading.Thread(target=self.ask_ollama_tools, args=(prompt,)).start()
                    # threading.Thread(target=self.ask_ollama, args=(prompt,)).start()

            self.response_box.handle_event(event=event)

    def run(self,screen,events,mouse_pos):
        self.handle_event(events=events,mouse_pos=mouse_pos)
        self.update_response()
        self.bg.draw(screen=screen)

        # self.character_image.draw(screen=screen)
        # self.prompt_box.draw(screen=screen,events=events)
        # self.response_box.draw(screen=screen)
        # self.prompt_button.draw(screen=screen)
        self.display_map()
        self.current_room_box.new_text(text=self.current_room_description)
        self.current_room_box.draw(screen=screen)

        # self.map_grid.draw(screen=screen)
        

       
        
        



