import pygame
import sys
from widgets.image import Image
from widgets.textarea import TextArea
from widgets.input_text import InputText
from widgets.button import Button
import ollama
import threading
import json
from function_calls.ollama_tools_v2 import OllamaToolCall  # Import your LLaMA tool function
from function_calls.ollama_tools_states import OllamaToolCallState  # Import your LLaMA tool function
from function_calls.ollama_context import OllamaWithContext
from debug import debug
import os


from function_calls.ollama_dmg import OllamaDmg

class DungeonScreen:
    """
    this is the game mode 
    - works to move
    -still working on loot etc
    """
    def __init__(self,game,w,h):
        # setup
        self.game = game
        self.WIDTH = w
        self.HEIGHT = h
        self.char = game.char
        self.dungeon_img_path = self.char.dungeon_path+'images/'
        dungeon_path = self.char.dungeon_path

        #set starting- current room
        self.current_room_id = 0

        # Images - dungeon room and character
        self.dungeon_room_img = Image(image=self.dungeon_img_path+'1.png',pos=(595,0),scale=(0.35*w,0.45*h))

        self.character_image = Image(image=self.char.profile_path+'profile_img.png',
                pos=(0.75*w,0.75*h),scale=(0.25*w,0.25*h))
        
        
        #Text boxes
        # prompt box + button
        self.prompt_box = InputText(x=0,y=0.75*h,width=0.75*w,height=0.25*h,
                        title='',bg_color=(69, 69, 69), text_color=(255, 255, 255),font_size=24)
        self.prompt_button = Button(pos=(0.07*w,0.78*h),text_input='Submit',
                            base_color="black", hovering_color="Green") 
        
        # prompt response box
        self.DM_box = TextArea(text='',WIDTH=0.6*w,HEIGHT=0.49*h,x=0*w,y=0,
            text_color=(255, 255, 255),bg_color=(69, 69, 69),title='Dungeon Master',title_color='black')
        #showing rolls and dmg 
        self.roll_box = TextArea(text='',WIDTH=0.5*w,HEIGHT=0.11*h,x=0.22*h,y=0-1,
            text_color=(0, 0, 0),bg_color=(69, 69, 69),title='Roll:', font_size=20, title_color='black')

        # player inventory box
        self.inventory_box = TextArea(text='',WIDTH=0.2*w,HEIGHT=0.25*h,x=0,y=0.5*h, font_size=20,
                    text_color=(255, 255, 255),bg_color=(69, 69, 69),title='Player Inventory',title_color='black')
        # current room move options box
        self.current_room_options_box = TextArea(text='',WIDTH=0.2*w,HEIGHT=0.25*h,x=0.2*w,y=0.5*h, font_size=20,
                            text_color=(255, 255, 255),bg_color=(69, 69, 69),title='You are in:',title_color='black')
        
        
    
        self.inventory_path = './inventory.json'

        # Check if the file exists, and if not, create it
        if not os.path.exists(self.inventory_path):
            # Create the directories if they don't exist
            os.makedirs(os.path.dirname(self.inventory_path), exist_ok=True)
            
            # Create an empty JSON file or initialize it with default data
            with open(self.inventory_path, 'w') as f:
                json.dump([], f)  # Empty dictionary as default content

        
        with open(self.inventory_path,'w') as f:
            json.dump(self.char.inventory,f,indent=4)

        self.inventory = self.char.inventory

        # Extract only the names of the items in the inventory
        self.item_names = ', '.join([item['name'] for item in self.inventory])

        # self.inventory.append(f'{item_names}')
        
        
        # open the dungeon json file and set the current room data to use in the boxes
        with open(dungeon_path+'dungeon.json') as f:
            self.dungeon = json.load(f)
        
        self.current_room_data = self.dungeon['rooms'][self.current_room_id]
        self.current_room_name = self.dungeon['rooms'][self.current_room_id]['name']
        self.current_room_description = self.dungeon['rooms'][self.current_room_id]['description']

        
        # the room json path from updated dungeon . json
        self.current_room_items_path = self.dungeon['rooms'][self.current_room_id]['items_file']
        
        
        
        # THIS VAriable dosnt work? needs fixing? why??
        # self.current_room_items_path

        
        with open(self.current_room_items_path) as f:
            self.current_room_items = json.load(f)
        
        # Extract only the names of the items in the inventory
        # Check if item is a dictionary before trying to access 'name'
        room_item_names = [item['name'] for item in self.current_room_items if isinstance(item, dict) and 'name' in item]

        # makes a string of the items in the room
        self.current_room_items = f'{room_item_names}'

        self.current_room_items_box = TextArea(text=self.current_room_items,font_size=20,WIDTH=0.2*w,HEIGHT=0.25*h,x=0.4*w,y=0.5*h,
                                        text_color=(255, 255, 255),bg_color=(69, 69, 69),title='Room items:',title_color='black')


        
        # Game state: track the current room and position in the grid
        self.player_move_options = self.dungeon['rooms'][self.current_room_id]['connections']  # move options from current in the map
        self.player_position = [self.dungeon['rooms'][self.current_room_id]['coordinates'][0], self.dungeon['rooms'][self.current_room_id]['coordinates'][1]] # player position in the map


        # room desciption box 
        self.current_room_box = TextArea(text='',font_size=18,WIDTH=370,HEIGHT=185,x=0.605*w,y=0.46*h,text_color=(255, 255, 255),bg_color=(69, 69, 69),title='Room Description',title_color='black')


        # not used right now, but is ment to be used for going up and down floors
        # self.special_action_available = None  # To track if a special action is available
        self.game_exit = False  # Flag to handle game exit
        
    
        
        # threading attributes 
        self.response = None  
        self.is_fetching = False  


    def update_current_room_options_box(self):
        self.current_room_options_box.new_text(text=f"{self.current_room_name}, current position: {self.player_position}, move options:{self.player_move_options}") 
    
    def update_current_room_items_box(self):
        # open the json file with the items in the room
        with open(self.current_room_items_path) as f:
            self.current_room_items = json.load(f)
        
        # Extract only the names of the items in the inventory
        # Check if item is a dictionary before trying to access 'name' - because had issues with the JSON file before -dont think it is needed anymore, but more "safe"/error handling
        room_item_names = [item['name'] for item in self.current_room_items if isinstance(item, dict) and 'name' in item]

        # makes a string of the items in the room
        self.current_room_items = f'{room_item_names}'
        
        # set box info to list of items in a room
        self.current_room_items_box.new_text(text=self.current_room_items)

    def get_room_by_coordinates(self, rooms, new_coordinates):
        """Get the room ID based on the coordinates - would be better if id/coordinates were in the top level of the json so we could just use the coordinates as a key, but this works for now, and I guess it would be messy to change the generator function prompts etc"""
        for room in rooms:
            if room['coordinates'] == new_coordinates:
                return room['room_id']  # Or return room itself if you need more info

    def move_to_room(self, direction):
        # Calculate new position
        new_x = self.player_position[0]
        new_y = self.player_position[1]
        if direction == 'north':
            new_x -= 1
        elif direction == 'south':
            new_x += 1
        elif direction == 'east':
            new_y += 1
        elif direction == 'west':
            new_y -= 1
        
        if [new_x, new_y] in self.player_move_options:
            print('valid move')
            
            # set new player position
            self.player_position = [new_x, new_y]
            
            # find the new room id
            self.current_room_id = self.get_room_by_coordinates(rooms=self.dungeon['rooms'],new_coordinates=self.player_position)
            # set the new room data (id -1 because the room id is 1-indexed (starts at 1 and array index starts at 0))
            self.current_room_id = self.current_room_id - 1
            
            # update the room data
            self.current_room_data = self.dungeon['rooms'][self.current_room_id]
            self.current_room_name = self.dungeon['rooms'][self.current_room_id]['name']
            self.current_room_description = self.dungeon['rooms'][self.current_room_id]['description']
            self.player_move_options = self.dungeon['rooms'][self.current_room_id]['connections']
            
            # update so looking at the right room JSON
            self.current_room_items_path = self.dungeon['rooms'][self.current_room_id]['items_file']
            self.room_file= self.dungeon['rooms'][self.current_room_id]['items_file']
            
        else:
            print('invalid move')
            
    def display_map(self):
        # displays the map in the top right corner - from the JSON file
        with open(self.char.dungeon_path+'dungeon_map.json') as f:
            self.map_grid = json.load(f)

        # Display the map in the top-right corner
        font = pygame.font.Font(None, 24)
        cell_size = 20  # Cell size for better fit
        grid_offset_x = 0.25*self.WIDTH # X offset for where the grid will be displayed
        grid_offset_y = 0.65*self.HEIGHT  # Y offset for where the grid will be displayed


        for row_idx, row in enumerate(self.map_grid):
            row_text = ''
            for col_idx, cell in enumerate(row):
                # Check if this is the player's position and mark it with 'X'
                if [row_idx+1, col_idx+1] == self.player_position:
                    cell_text = 'X'
                else:
                    cell_text = cell
                row_text += cell_text + ' '
            # Render the row text
            text_surface = font.render(row_text, True, (0, 0, 0))
            self.game.screen.blit(text_surface, (grid_offset_x, grid_offset_y + row_idx * cell_size))

    def ask_ollama_tools(self, prompt):
        # not sure if works with threading 
        # self.is_fetching = True  # Mark that we are fetching
        
        # give it the current room in the JSON  - used in prompt
        self.room_file= self.dungeon['rooms'][self.current_room_id]['items_file']
        # print(f'from ollama_screen {self.char.inventory}')
        # print(self.current_room_items)
        


        # room_file outside the prompt does nothing here? - remove?
        # calling the first tools - DROPITEM, TAKEITEM, LOOKATROOM, ROLLACTION
        ollama_instance = OllamaToolCall(messages=f'Player request:{prompt}. Items in the room the player is in: {self.current_room_items}, The room description: {self.current_room_description} The players current inventory: {self.char.inventory} The room_file: ./{self.room_file}',
                    room_file=self.room_file)
        prompt,system,tool_used = ollama_instance.activate_functions()

        # if did roll/action
        if tool_used == 'resolve_hard_action':
            
            roll_info = prompt
            # add it to the info box
            self.roll_box = TextArea(text='',WIDTH=0.4*self.WIDTH,HEIGHT=0.05*self.HEIGHT,x=0.22*self.HEIGHT,y=0-0.9,
            text_color=(0, 0, 0),bg_color=(69, 69, 69),title=f'{roll_info}', font_size=14, title_color='black')


            
            #run ollama falvor text with context for the roll/outcome 
            ollama_with_context = OllamaWithContext(path=self.char.profile_path)
            # DONT USE self.response here- has to be flavor_text or messes with order - gotcha thing
            flavor_text = ollama_with_context.generate_context(prompt=prompt,system=system)


            
            # Check if the player took damage using the 
            ollama_dmg = OllamaDmg()            
            dmg = ollama_dmg.damage_check_and_resolve(prompt=flavor_text)
            if dmg > 0:
                self.response = f'{flavor_text}. (You take {dmg} damage!)'
                # need to implement HP for the player and change it here
            elif dmg == 0:
                self.response = f'{flavor_text}. (You take no damage)'

        
        # if used leave/drop item
        elif tool_used == 'leave_drop_throw_item':
            
            # if item found make flavor text with context    
            if system:
                ollama_with_context = OllamaWithContext(path=self.char.profile_path)
                self.response = ollama_with_context.generate_context(prompt=prompt,system=system)
            else:
                # if item not found when try to leave/loot - response = item not found
                self.response = prompt
        
        #if used loot item from room 
        elif tool_used == 'loot_item_from_room':
            # if item found make flavor text with context        
            if system:
                ollama_with_context = OllamaWithContext(path=self.char.profile_path)
                self.response = ollama_with_context.generate_context(prompt=prompt,system=system)
            else:
                # if item not found when try to leave/loot - response = item not found
                self.response = prompt
        
        # if used look at room
        elif tool_used == 'look_at_room':
            # generate room description with context
            ollama_with_context = OllamaWithContext(path=self.char.profile_path)
            self.response = ollama_with_context.generate_context(prompt=prompt,system=system)
            
            
        # set the response in the DM box
        self.DM_box.new_text(text=self.response)
        
        # STILL NEED TO UPDATE THE DESCRIPTION OF THE ROOM AND THE ITEMS IN THE ROOM
        # NEED TO ADD HP FOR THE PLAYER AND UPDATE IT AFTER THE ROLL
        # NICE IF ALSO PRINTED THE ROLL IN THE DM BOX - AND MADE A FUNCTION TO PRESS FOR THE ROLL
        
        # ALSO MERGE ITEMS ? - LIKE ADD POISON TO PIE?
        
        # HAS NO WAY TO ADD NEW ITEMS TO THE ROOM OR REMOVE THEM - AI TOO STUPID, THINK ABOUT HOW TO DO THIS
        
        
        # ollama_instance_state = OllamaToolCallState(message=self.response, inventory_file='inventory_json.json', room_file=self.room_file)
        # self.response = ollama_instance_state.activate_functions()

        # self.DM_box.new_text(text=self.response)
        self.response = None  # Clear the response after updating the box
      
    def update_inventory_box(self):
        with open('./inventory.json') as f:
            self.inventory = json.load(f)
        
        # function_calls and inventory needs rework before char.inventory replaces it
        # self.char.inventory = self.inventory['inventory']
        
        # Extract only the names of the items in the inventory
        self.item_names = ', '.join([item['name'] for item in self.inventory])
            
        # self.inventory.append(f'{item_names}')

        
        self.inventory_box.new_text(text=self.item_names)
        
           

    def update_response(self):
        # Check if there's a new response and update the response box
        if self.response:
            self.DM_box.new_text(text=self.response)
            self.response = None  # Clear the response after updating the box

    def handle_event(self,events,mouse_pos):
        self.prompt_button.changeColor(position=mouse_pos)
        for event in events:
            # handles quits 
            if event.type == pygame.QUIT:
                # handle character save
                self.char.inventory = self.inventory
                self.char.save_profile()
                pygame.quit()
                sys.exit()
                

            # keys for player navigation
            if event.type == pygame.KEYDOWN:
                # print(self.current_room_items_path)
                if event.key == pygame.K_UP:
                    self.move_to_room('north')
                elif event.key == pygame.K_DOWN:
                    self.move_to_room('south')
                elif event.key == pygame.K_LEFT:
                    self.move_to_room('west')
                elif event.key == pygame.K_RIGHT:
                    self.move_to_room('east')
                
                # change room image - needs to change later when dungeon gets larger
                room_id_changed = str(self.current_room_id+1) + '.png'
                self.dungeon_room_img.change_image(new_image=self.dungeon_img_path+room_id_changed)
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.prompt_button.checkForInput(mouse_pos) and not self.is_fetching:
                    prompt = self.prompt_box.send_text()
                    # Start a new thread for the LLM request
                    threading.Thread(target=self.ask_ollama_tools, args=(prompt,)).start()

            self.DM_box.handle_event(event=event)
            self.inventory_box.handle_event(event=event)
            self.current_room_box.handle_event(event=event)

    def run(self,screen,events,mouse_pos):
        self.handle_event(events=events,mouse_pos=mouse_pos)
        self.update_response()
        self.dungeon_room_img.draw(screen=screen)
        
        self.character_image.draw(screen=screen)
        self.prompt_box.draw(screen=screen,events=events)
        self.DM_box.draw(screen=screen)

        self.prompt_button.draw(screen=screen)
        

        # description of the room
        self.current_room_box.new_text(text=self.current_room_description)
        self.current_room_box.draw(screen=screen)
        
        #move options (coordinates and room name)
        self.update_current_room_options_box()
        self.current_room_options_box.draw(screen=screen)

        #player inventory 
        self.update_inventory_box()
        self.inventory_box.draw(screen=screen)
            
        # items in the room
        self.update_current_room_items_box()
        self.current_room_items_box.draw(screen=screen)
        
        #box for rolls
        self.roll_box.draw(screen=screen)
        
        self.display_map()

        

       
        
        



