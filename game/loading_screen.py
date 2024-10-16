import pygame
import sys
from widgets.image import Image
from widgets.textarea import TextArea
from widgets.input_text import InputText
from widgets.button import Button
import time
import threading
from comfy_prompt import run_comfy
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from world_generator.generate_world import GenerateWorld
import json


class LoadingScreen:
    def __init__(self,game,w,h):
        self.game = game
        self.bg = Image('./pics/loading_backgroud.webp',pos=(0,0),scale=(w,h-200))
        self.char = game.char
        self.terminal_box = TextArea(text='',WIDTH=w,HEIGHT=200,x=0,y=h-200,
            text_color=(255, 255, 255),bg_color=(69, 69, 69),title='Terminal',title_color='black')

        self.loading_complete= False
        self.gen_button = Button(pos=(w-325,h-400),text_input='Submit',
                image=None,base_color="black", hovering_color="Green",font=pygame.font.Font(None, 36))
        
        self.terminal_text = ''


    def start_generating(self):
        self.dungeon_generator()
        self.char_img_generator()
        self.loading_complete = True


    def char_img_generator(self):
        self.terminal_text = self.terminal_text+'generating character image'+'\n'
        self.terminal_box.new_text(text=self.terminal_text)
        run_comfy(self.char.description, self.char.name)
        
        self.char.image = f'./pics/{self.char.name}/profile_img.png'
        
        
    def dungeon_generator(self):
        self.terminal_text = self.terminal_text+'generating dungeon json'+'\n'
        self.terminal_box.new_text(text=self.terminal_text)
        world = GenerateWorld()
        world.run_dungeon()
        self.dungeon_room_splitter()
 
        with open('dungeon.json') as f:
            dungeon_data = json.load(f)
        self.terminal_text = self.terminal_text+'generating dungeon rooms images'+'\n'
        self.terminal_box.new_text(text=self.terminal_text)
        rooms =self.prepare_rooms(rooms_data=dungeon_data['rooms'])
        
        for room in rooms:
            description = room['description']
            room_id = room['id']
            run_comfy(description,self.char.name,image_type='room',room_id=room_id)

        self.char.image = f'./pics/{self.char.name}/profile_img.png'
        



    def dungeon_room_splitter(self):
        # Load dungeon JSON from a file
        with open('dungeon.json', 'r') as dungeon_file:
            dungeon = json.load(dungeon_file)
            
        # Directory where you want to save the item JSON files
        output_directory = "room_items"

        # Create directory for room items if it doesn't exist
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        # Loop through each room and create a JSON file for the items
        for room in dungeon['rooms']:
            # Extract room name or room_id to name the file
            room_id = room['room_id']
            
            # Define the file name and path
            item_file_name = f"room_{room_id}_items.json"
            item_file_path = os.path.join(output_directory, item_file_name)
            
            # Extract items
            room_items = room.get('items', [])
            
            # Save items as a JSON file
            with open(item_file_path, 'w') as item_file:
                json.dump(room_items, item_file, indent=4)
            
            # Update the original dungeon room to include the path to the items file
            room['items_file'] = item_file_path
            
            # Remove the inline items array from the room
            del room['items']

        # Save the modified dungeon JSON
        with open('dungeon.json', 'w') as dungeon_file:
            json.dump(dungeon, dungeon_file, indent=4)

        print("Room item files and updated dungeon JSON have been saved.")        
    
    def prepare_rooms(self,rooms_data):
        self.terminal_text = self.terminal_text+'preparing rooms data'+'\n'
        self.terminal_box.new_text(text=self.terminal_text)
        rooms = []
        extra_prompt= 'Make a topview dungeon map in style of famous dungeons and dragons style battlemap for a role playing game with this description: '
        for room in rooms_data:
            room_data = {}
            room_data['name'] = room['name']
            room_data['description'] = extra_prompt + room['description']
            room_data['id'] = str(room['room_id'])
            rooms.append(room_data)
        return rooms


    def handle_event(self,events,mouse_pos):
        self.gen_button.changeColor(position=mouse_pos)
        for event in events:
            # handles quits 
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.gen_button.checkForInput(mouse_pos):
                    threading.Thread(target=self.start_generating).start() 
                    

            self.terminal_box.handle_event(event=event)




    
    def run(self,screen,events,mouse_pos):
        self.handle_event(events=events,mouse_pos=mouse_pos)
        self.bg.draw(screen=screen)
        self.terminal_box.draw(screen=screen)
        self.gen_button.draw(screen)

        if self.loading_complete:
            self.game.game_mode ='dungeon'
        

