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
        path = f'./pics/{self.char.name}/dungeon_rooms/'


        self.dungeon_room_img = Image(image=path+'1.png',pos=(0,0),scale=(0.4*w,0.5*h))


        self.character_image = Image(image=self.char.image,pos=(0.75*w,0.75*h),scale=(0.25*w,0.25*h))

        #Text boxes
        self.prompt_box = InputText(x=0,y=0.75*h,width=0.75*w,height=0.25*h,
                        title='',bg_color=(69, 69, 69), text_color=(255, 255, 255),font_size=24)


        self.prompt_button = Button(pos=(0.07*w,0.78*h),text_input='Submit',
                            base_color="black", hovering_color="Green") 
        
        self.DM_box = TextArea(text='',WIDTH=0.6*w,HEIGHT=0.5*h,x=0.4*w,y=0,
            text_color=(255, 255, 255),bg_color=(69, 69, 69),title='Dungeon Master',title_color='black')



        self.inventory_box = TextArea(text='',WIDTH=0.2*w,HEIGHT=0.25*h,x=0,y=0.5*h,
                    text_color=(255, 255, 255),bg_color=(69, 69, 69),title='Player Inventory',title_color='black')

        self.current_room_options_box = TextArea(text='',WIDTH=0.2*w,HEIGHT=0.25*h,x=0.2*w,y=0.5*h,
                            text_color=(255, 255, 255),bg_color=(69, 69, 69),title='Move info:',title_color='black')
        
        
        #set starting- current room
        self.current_room_id = 0

        # set inventory to items
        with open('inventory_json.json') as f:
            self.inventory = json.load(f)
        
        # Extract only the names of the items in the inventory
        item_names = [item['name'] for item in self.inventory['inventory']]
            
        self.inventory = f'{item_names}'

        with open('dungeon.json') as f:
            self.dungeon = json.load(f)
        
        self.current_room_data = self.dungeon['rooms'][self.current_room_id]
        self.current_room_name = self.dungeon['rooms'][self.current_room_id]['name']
        self.current_room_description = self.dungeon['rooms'][self.current_room_id]['description']
        self.current_x = self.dungeon['rooms'][self.current_room_id]['coordinates'][0]
        self.current_y = self.dungeon['rooms'][self.current_room_id]['coordinates'][1]
        
        # the room json path from updated dungeon . json
        self.current_room_items_path = self.dungeon['rooms'][self.current_room_id]['items_file']
        
        with open(self.current_room_items_path) as f:
            self.current_room_items = json.load(f)
        
        # Extract only the names of the items in the inventory
        # room_item_names = [item['name'] for item in self.current_room_items]
        # Check if item is a dictionary before trying to access 'name'
        room_item_names = [item['name'] for item in self.current_room_items if isinstance(item, dict) and 'name' in item]

        # 
        self.current_room_items = f'{room_item_names}'

        # print(self.current_room_items)
        self.current_room_items_box = TextArea(text=self.current_room_items,font_size=20,WIDTH=0.2*w,HEIGHT=0.25*h,x=0.4*w,y=0.5*h,
                                        text_color=(255, 255, 255),bg_color=(69, 69, 69),title='Room items:',title_color='black')


        
        # Game state: track the current room and position in the grid
        self.player_move_options = self.dungeon['rooms'][self.current_room_id]['connections']  # move options from current in the map
        self.player_position = [self.dungeon['rooms'][self.current_room_id]['coordinates'][0], self.dungeon['rooms'][self.current_room_id]['coordinates'][1]] # player position in the map
        print(self.player_position)


        # room info boxes 
        self.current_room_box = TextArea(text='',font_size=18,WIDTH=340,HEIGHT=250,x=5,y=5,text_color=(255, 255, 255),bg_color=(69, 69, 69),title=self.current_room_name,title_color='black')

        self.special_action_available = None  # To track if a special action is available
        self.game_exit = False  # Flag to handle game exit
        
        
        print(self.player_move_options)
        print(self.player_position)
        
        # threading attributes
        self.response = None  
        self.is_fetching = False  


    def update_current_room_box(self):
        self.current_room_box.new_text(text=self.current_room_description)


        self.current_room_options_box = TextArea(text=f"move options:{self.player_move_options}, current location:{self.player_position}",
                                                 WIDTH=0.2*self.WIDTH,HEIGHT=0.25*self.HEIGHT,x=0.2*self.WIDTH,y=0.5*self.HEIGHT,
                                                 text_color=(255, 255, 255),bg_color=(69, 69, 69),title='Move info:',title_color='black')
        
        
        with open(self.current_room_items_path) as f:
            self.current_room_items = json.load(f)
        
        # Extract only the names of the items in the inventory
        # room_item_names = [item['name'] for item in self.current_room_items]
        # Check if item is a dictionary before trying to access 'name'
        room_item_names = [item['name'] for item in self.current_room_items if isinstance(item, dict) and 'name' in item]

            
        self.current_room_items = f'{room_item_names}'
        
        # list of items in a room
        self.current_room_items_box.new_text(text=self.current_room_items)

        # # Display instructions if a special action is available
        # if self.special_action_available:
        #     action_text = "Press 'U' to "
        #     if self.special_action_available == 'exit':
        #         action_text += "exit"
        #     elif self.special_action_available == 'up-floor':
        #         action_text += "go up"
        #     elif self.special_action_available == 'down-floor':
        #         action_text += "go down"
        #     action_surface = font.render(action_text, True, (255, 255, 0))  # Yellow text
        #     self.game.screen.blit(action_surface, (50, 150))

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
            new_y -= 1
        elif direction == 'south':
            new_y += 1
        elif direction == 'east':
            new_x += 1
        elif direction == 'west':
            new_x -= 1
        
        if [new_x, new_y] in self.player_move_options:
            print('valid move')
            self.player_position = [new_x, new_y]
            print(self.current_room_id)
            self.current_room_id = self.get_room_by_coordinates(rooms=self.dungeon['rooms'],new_coordinates=self.player_position)
            self.current_room_id = self.current_room_id - 1
            print(self.current_room_id)
            self.current_room_data = self.dungeon['rooms'][self.current_room_id]
            self.current_room_name = self.dungeon['rooms'][self.current_room_id]['name']
            self.current_room_description = self.dungeon['rooms'][self.current_room_id]['description']
            self.current_x = self.dungeon['rooms'][self.current_room_id]['coordinates'][0]
            self.current_y = self.dungeon['rooms'][self.current_room_id]['coordinates'][1]
            self.player_move_options = self.dungeon['rooms'][self.current_room_id]['connections']
            self.update_current_room_box()
            # update so looking at the right room JSON
            self.current_room_items_path = self.dungeon['rooms'][self.current_room_id]['items_file']
            self.room_file= self.dungeon['rooms'][self.current_room_id]['items_file']
            
            with open(self.current_room_items_path) as f:
                self.current_room_items = json.load(f)        
            
            self.update_current_room_box()
            
        else:
            print('invalid move')
            
    def display_map(self):
        # displays the map in the top right corner - from the JSON file
        with open('./dungeon_map.json') as f:
            self.map_grid = json.load(f)

        # Display the map in the top-right corner
        font = pygame.font.Font(None, 24)
        cell_size = 20  # Cell size for better fit
        grid_offset_x = 0.7*self.WIDTH # X offset for where the grid will be displayed
        grid_offset_y = 0.6*self.HEIGHT  # Y offset for where the grid will be displayed

        for row_idx, row in enumerate(self.map_grid):
            row_text = ''
            for col_idx, cell in enumerate(row):
                print(col_idx, row_idx)
                # Check if this is the player's position and mark it with 'X'
                if [col_idx+1, row_idx+1] == self.player_position:
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

        # NOW IT WORKS ATLEAST - but needs to run the "room_fixer" after generation, so that each room is a separate jsonfile, it cant handle all rooms data at the same time
        
        
        # give it the current room in the JSON 
        self.room_file= self.dungeon['rooms'][self.current_room_id]['items_file']
        print(self.inventory)
        # print(self.current_room_items)
        
        ollama_instance = OllamaToolCall(messages=f'Player request:{prompt}. Items in the room the player is in: {self.current_room_items}, The room description: {self.current_room_description} The players current inventory: {self.inventory} The room_file: ./{self.room_file}', room_file=self.room_file)
        self.response = ollama_instance.activate_functions()
        # self.is_fetching = False  # Mark that fetching is done
        
        self.DM_box.new_text(text=self.response)
        self.response = None  # Clear the response after updating the box


        # This runs in a separate thread, so it won't block the main loop
        # self.is_fetching = True  # Mark that we are fetching
        # resp = ollama.generate(
        #     model='llama3.1',
        #     prompt=prompt
        # )
        # self.response = resp['response']
        # self.is_fetching = False  # Mark that fetching is done
        
    def update_inventory_box(self):
        with open('./inventory_json.json') as f:
            self.inventory = json.load(f)
            
        
        # Extract only the names of the items in the inventory
        item_names = [item['name'] for item in self.inventory['inventory']]
            
        self.inventory = f'{item_names}'

        self.inventory_box.new_text(text=self.inventory)
         
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
                pygame.quit()
                sys.exit()
            
            # keys for player navigation
            if event.type == pygame.KEYDOWN:
                print(self.current_room_items_path)
                if event.key == pygame.K_UP:
                    self.move_to_room('north')
                elif event.key == pygame.K_DOWN:
                    self.move_to_room('south')
                elif event.key == pygame.K_LEFT:
                    self.move_to_room('west')
                elif event.key == pygame.K_RIGHT:
                    self.move_to_room('east')
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.prompt_button.checkForInput(mouse_pos) and not self.is_fetching:
                    prompt = self.prompt_box.send_text()
                    # Start a new thread for the LLM request
                    threading.Thread(target=self.ask_ollama_tools, args=(prompt,)).start()

            self.DM_box.handle_event(event=event)

    def run(self,screen,events,mouse_pos):
        self.handle_event(events=events,mouse_pos=mouse_pos)
        self.update_response()
        self.dungeon_room_img.draw(screen=screen)
        
        self.character_image.draw(screen=screen)
        self.prompt_box.draw(screen=screen,events=events)
        self.DM_box.draw(screen=screen)

        self.prompt_button.draw(screen=screen)
        

        # these are deprecated
        # self.current_room_box.new_text(text=self.current_room_description)
        # self.current_room_box.draw(screen=screen)
        
        self.update_current_room_box()
        self.current_room_options_box.draw(screen=screen)
        
        self.update_inventory_box()
        self.inventory_box.draw(screen=screen)
             
        self.current_room_items_box.draw(screen=screen)
        self.display_map()

        

       
        
        



