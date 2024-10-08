
# TO DO:

# 1 - make possible to do ollama calls in the game




#  - make floor change dynamic - for move thing - so it uses a JSON rather then a hardcoded map
#  add items to rooms

# add inventory/hp etc screen 
# import the loot actions from before
# add the img generation call from before

# test to add music generation and speech and see how slow it gets

###make combat loop###
# add monsters, call for initative, combat mode etc

import pygame
import pygame_menu
import sys

import time

import threading

sys.path.append('../function_calls/')  # Adjust the path
from ollama_tools_v2 import OllamaToolCall  # Import your LLaMA tool function


# Define a Room class to represent each room
class Room:
    def __init__(self, name, description, connections, special=None):
        
        
        self.name = name  # Room name
        self.description = description  # Room description
        self.connections = connections  # Dictionary mapping directions (e.g., 'north') to connected rooms
        self.special = special  # Special feature (e.g., 'exit', 'up-floor', 'down-floor')


class GameMap:
    def __init__(self, game,w,h):
        self.game = game
        # self.screen = pygame.display.set_mode((w, h))
        pygame.display.set_caption("Lair Machina: MAP MODE")

        
        # Basic setup
        self.WIDTH = 800
        self.HEIGHT = 600
        pygame.init()


        # test LLM calls
        # TESTING: Set up the input box for LLM calls
        self.input_box = pygame.Rect(100, 550, 600, 40)  # Position and size of the input box
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color(255, 0, 0)
        self.color = self.color_inactive
        self.active = False
        self.text = ''
        self.done = False
        self.output_text = ''
        
        
        # Initialize pygame mixer - for music
        # pygame.mixer.init()
        pygame.mixer.init(frequency=22050, size=-16, channels=2)
        

        # Load and play background music (loop indefinitely)
        pygame.mixer.music.load('sound/The_journey(2).mp3')
        pygame.mixer.music.play(-1)  # -1 means the music will loop indefinitely

        pygame.mixer.music.set_volume(0.3)  # Set background music volume (0.0 to 1.0)
        
        
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()  # Clock object to control the game's framerate
        self.FPS = 60

        pygame.display.update()
         # Initialize pygame's font module
        pygame.font.init()
        # Create a font object. 'None' uses the default font, and 36 is the size
        self.font = pygame.font.Font(None, 36)
        
        # Game state: track the current room and position in the grid
        self.current_room = None
        self.player_position = [2, 2]  # Starting position in the map (Room 1)
        self.special_action_available = None  # To track if a special action is available
        self.game_exit = False  # Flag to handle game exit

        # Create rooms and set up the initial floor
        self.create_rooms()






    def create_rooms(self):
        # This should be replaced with loading from a JSON file or similar  - here we need it use the generated JSONS

        # First floor rooms
        door_out = Room('Door out', 'This is the door out.', {}, special='exit')
        room1 = Room('Room 1', 'This is the first room north of Door in.', {})
        room2 = Room('Room 2', 'This room is north of Room 1.', {})
        room3 = Room('Room 3', 'This room is east of Room 2.', {}, special='up-floor')

        # Second floor rooms
        floor2_room1 = Room('Floor 2 Room 1', 'First room on floor 2 (stairs down here).', {}, special='down-floor')
        floor2_room2 = Room('Floor 2 Room 2', 'Second room on floor 2.', {})
        floor2_room3 = Room('Floor 2 Room 3', 'Third room on floor 2.', {})
        floor2_room4 = Room('Floor 2 Room 4', 'Fourth room on floor 2.', {})

        # Define floor layouts
        self.floor1_rooms = {
            'Door out': door_out,
            'Room 1': room1,
            'Room 2': room2,
            'Room 3': room3
        }

        self.floor2_rooms = {
            'Floor 2 Room 1': floor2_room1,
            'Floor 2 Room 2': floor2_room2,
            'Floor 2 Room 3': floor2_room3,
            'Floor 2 Room 4': floor2_room4
        }

        # TURN THIS INTO A  def Update_floor(self, floor_data): function
        # Set the starting floor and room
        self.current_floor_rooms = self.floor1_rooms
        self.current_room = door_out

        # Initial map grid for floor 1
        self.map_grid = [
            ['-', '-', 'O', 'U'],  # 'U' for up-floor
            ['-', '-', 'O', '-'],
            ['-', '-', 'E', '-']   # 'E' for exit
        ]

        # Position to room mapping for floor 1
        self.position_to_room = {
            (2, 2): 'Door out',  # Exit
            (2, 1): 'Room 1',
            (2, 0): 'Room 2',
            (3, 0): 'Room 3', # Stairs up
        }

    def trigger_up_floor(self):
        print("You have found the stairs up! Moving to the next level...")
        # Update map grid for floor 2 - should be dynamic like self.map_grid = self.current_floor_rooms['map_grid']
        self.map_grid = [
            ['-', '-','-', 'D'], # 'D' for down-floor
            ['-', '-','O', 'O'],
            ['-', '-','O', '-']   
        ]
        # Reset player position for the new floor
        self.player_position = [3, 0]
        # Set the current floor rooms and room
        self.current_floor_rooms = self.floor2_rooms
        self.current_room = self.current_floor_rooms['Floor 2 Room 1']
        # Update position to room mapping for floor 2
        self.position_to_room = {
            (3, 0): 'Floor 2 Room 1', #D Stairs down
            (3, 1): 'Floor 2 Room 2',
            (2, 1): 'Floor 2 Room 3',
            (2, 2): 'Floor 2 Room 4',
        }
        self.special_action_available = self.current_room.special

    def trigger_down_floor(self):
        print("You have found the stairs down! Moving to the previous level...")
        # Reset map grid to floor 1
        self.map_grid = [
            ['-', '-', 'O', 'U'],  # 'U' for up-floor
            ['-', '-', 'O', '-'],
            ['-', '-', 'E', '-']   # 'E' for exit
        ]
        # Reset player position for the first floor
        self.player_position = [3, 0]  # Position corresponding to Room 2
        # Set the current floor rooms and room
        self.current_floor_rooms = self.floor1_rooms
        self.current_room = self.current_floor_rooms['Room 3']
        # Reset position to room mapping for floor 1
        self.position_to_room = {
            (2, 2): 'Door out',  # Exit
            (2, 1): 'Room 1',
            (2, 0): 'Room 2',
            (3, 0): 'Room 3', # Stairs up
        }
        self.special_action_available = self.current_room.special
        # Reset special action

    def trigger_exit(self):
        print("You have found the exit! Congratulations!")
        # Set a flag to indicate the game should exit
        # self.game_active = False
        # self.game_exit = True  # Add a new attribute to handle game exit

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

        # Check bounds
        if 0 <= new_x < len(self.map_grid[0]) and 0 <= new_y < len(self.map_grid):
            # Check if cell is not a wall ('-')
            target_cell = self.map_grid[new_y][new_x]
            if target_cell != '-':
                # Update player position
                self.player_position = [new_x, new_y]
                # Optionally, print the new player position for debugging
                print(f"Player moved to position: {self.player_position}")

                # Update current room based on position
                room_name = self.position_to_room.get(tuple(self.player_position))
                if room_name:
                    self.current_room = self.current_floor_rooms[room_name]
                    print(f"Moved to {self.current_room.name}")
                    self.special_action_available = self.current_room.special
                else:
                    self.current_room = Room('Unknown', 'An empty space.', {})
                    self.special_action_available = None
            else:
                print("Cannot move to a wall!")
        else:
            print("Cannot move out of bounds!")

    def display_current_room(self):
        # Display the current room's name and description
        self.screen.fill((0, 0, 0))  # Clear screen with black
        font = pygame.font.Font(None, 36)
        text_surface = font.render(f"You are in {self.current_room.name}", True, (255, 255, 255))
        self.screen.blit(text_surface, (50, 50))

        description_surface = font.render(self.current_room.description, True, (255, 255, 255))
        self.screen.blit(description_surface, (50, 100))

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
            self.screen.blit(action_surface, (50, 150))

    def display_map(self):
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
            text_surface = font.render(row_text, True, (255, 255, 255))
            self.screen.blit(text_surface, (grid_offset_x, grid_offset_y + row_idx * cell_size))



    def handle_event(self, event):
        # keys for player navigation
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.move_to_room('north')
            elif event.key == pygame.K_DOWN:
                self.move_to_room('south')
            elif event.key == pygame.K_LEFT:
                self.move_to_room('west')
            elif event.key == pygame.K_RIGHT:
                self.move_to_room('east')
            elif event.key == pygame.K_u:  # 'U' key pressed
                if self.special_action_available == 'exit':
                    print("You found the exit!")
                    self.trigger_exit()
                elif self.special_action_available == 'up-floor':
                    print("You found stairs up! Moving up...")
                    self.trigger_up_floor()
                elif self.special_action_available == 'down-floor':
                    print("You found stairs down! Moving down...")
                    self.trigger_down_floor()
                else:
                    print("There's nothing special here.")
        # testing for LLaMA calls
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(f"{self.input_box.collidepoint(event.pos)}")
            # If the user clicked on the input_box rect.
            if self.input_box.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = self.color_active if self.active else self.color_inactive
            print(self.color)
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    
                    ollama_instance = OllamaToolCall(messages=self.text, room_file='castle_map.json') #room_file='room_json.json'
                    ollama_text_output = ollama_instance.activate_functions()
                    self.output_text = ollama_text_output
                    # self.output_text = self.text  # Here you can call your LLaMA function
                    self.text = ''  # Clear input text
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode


    def run(self,screen,events):
        screen.fill((0, 0, 0))  # Clear the screen with a black background, or choose another color

        # Render the text "Map Mode Active" in white
        text_surface = self.font.render('Map Mode Active', True, (255, 255, 255))
        # Blit the text surface onto the main screen surface at the calculated position
        screen.blit(text_surface, (0, 0))
        self.display_current_room()
        self.display_map()
        
        


        font = pygame.font.Font(None, 32)  # Default font of size 32
        # screen.fill((30, 30, 30))
        # Render the current text.
        txt_surface = font.render(self.text, True, self.color)
        # Resize the box if the text is too long.
        width = max(200, txt_surface.get_width()+10)
        self.input_box.w = width
        # Blit the text.
        screen.blit(txt_surface, (self.input_box.x+5, self.input_box.y+5))

        # Display the output text
        output_surface = font.render(self.output_text, True, pygame.Color('white'))
        screen.blit(output_surface, (100, 500))  # Position the output text above the input box
        # Blit the input_box rect.
        pygame.draw.rect(screen, self.color, self.input_box, 2)

        pygame.display.flip()



        
        for event in events:
            self.handle_event(event=event)
        
        
        
        
        # self.bg.update(screen=screen)

        # self.character_image.update(screen=screen)


