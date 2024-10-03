

# # to do:
# # 1 copy tonys base file for pygame -see below
# # 2 - add a navigation system to the game - so you can move between rooms - and state for the player (hp, location, etc)






# # Import necessary libraries for game development
# import pygame  # Pygame is used to create the game window and handle events
# import pygame_menu  # Pygame Menu is used for creating menus in the game
# import sys  # Used for system-specific functions like exiting the program

# # Import additional pygame_menu widget components
# import pygame_menu.widgets
# import pygame_menu.widgets.widget
# import pygame_menu.widgets.widget.scrollbar

# # Custom modules for debugging, text area, and button
# from debug import debug  # Custom debug function to display text on the screen
# import os  # For interacting with the operating system (file paths)
# from textarea import TextArea  # Custom TextArea class to display text blocks
# from button import Button  # Custom Button class for creating buttons

# # Setting up paths and importing custom world generation code
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# from world_generator.generate_world import GenerateWorld  # Generates the game world
# from world_generator.define_world import save_to_json, room  # Functions for saving game data

# # Define the main Game class
# class Game:
#     def __init__(self):
#         # Setup basic game configuration (Frame per second, screen size)
#         self.FPS = 60  # Frames per second
#         self.WIDTH = 800  # Width of the game window
#         self.HEIGHT = 600  # Height of the game window
        
#         # Initialize the Pygame library and set up the game window
#         pygame.init()
#         self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
#         self.clock = pygame.time.Clock()  # Clock object to control the game's framerate
        
#         # Set the title of the game window
#         pygame.display.set_caption("Lair Machina")
        
#         # Create the initial menu using pygame_menu, setting the theme and layout
#         self.menu = pygame_menu.Menu('Welcome Adventurer', self.WIDTH, self.HEIGHT,
#                                      theme=pygame_menu.themes.THEME_DARK)
        
#         # Add widgets to the menu (text inputs, selectors, buttons)
#         self.menu.add.text_input('Name :', default='Traveler', onchange=self.set_name)
#         self.menu.add.selector('Class :', [('Fighter', 1), ('Wizard', 2)], onchange=self.set_class)
#         self.menu.add.selector('Race :', [('Human', 1), ('Elf', 2), ('Dwarf', 3)], onchange=self.set_race)
#         self.menu.add.text_input('Character description :', default='', onchange=self.set_description, maxwidth=10)

#         # Add Play and Quit buttons to the menu
#         self.menu.add.button('Play', self.start_the_game)
#         self.menu.add.button('Quit', pygame_menu.events.EXIT)
        
#         # Initialize variables to manage game state and character data
#         self.game_active = False  # Whether the game is running or still in the menu

#         # Character customization information
#         self.char_name = None  # Character's name
#         self.char_class = None  # Character's class
#         self.class_id = None  # Class ID
#         self.char_description = None  # Character's description
#         self.char_race = None  # Character's race
#         self.race_id = None  # Race ID

#         # Save room data to a JSON file for use in world generation
#         save_to_json(data=room, file_name='room_blueprint.json')
#         self.gen_world = GenerateWorld()  # Initialize world generation
#         self.texts_ready = False  # Whether text content is ready for display
        
#         # Load lore and factions text files for in-game content
#         with open('../world_generator/texts/lore.txt', 'r') as file:
#             self.lore_text = file.read()  # Read lore text
        
#         with open('../world_generator/texts/factions.txt', 'r') as file:
#             self.factions_text = file.read()  # Read factions text

#         # Create TextArea objects to display lore and factions information in the game
#         self.lore_area = TextArea(text=self.lore_text,
#                                   WIDTH=self.WIDTH // 2,
#                                   HEIGHT=self.HEIGHT // 2,
#                                   x=self.WIDTH // 2, title='Lore')
        
#         self.faction_area = TextArea(text=self.factions_text,
#                                      WIDTH=self.WIDTH // 2 - 30,
#                                      HEIGHT=self.HEIGHT // 2,
#                                      x=0, title='Factions', title_color='red')
        
#         # Initialize a button for testing purposes
#         self.test_button = Button(image=None, pos=(400, 400),
#                                   text_input='test', font=pygame.font.Font(None, 30),
#                                   base_color='blue', hovering_color='green')

#     # Start the world generation process in a separate thread
#     def start_text_generation(self):
#         self.gen_world.run_in_thread()

#     # Display lore and faction information in the game
#     def world_lore(self):
#         self.lore_area.display(screen=self.screen)  # Display lore text
#         self.faction_area.display(screen=self.screen)  # Display factions text

#     # Callback functions to set character customization data
#     def set_description(self, text):
#         self.char_description = text
#         print(f"Character description: {self.char_description}")

#     def set_name(self, name):
#         self.char_name = name  # Store the character's name
#         print(f"Name set to: {self.char_name}")

#     def set_class(self, selected_value, index):
#         selected_class, class_id = selected_value
#         self.char_class = selected_class[0]
#         self.class_id = class_id
#         print(f"Selected Class: {self.char_class} (ID: {self.class_id})")

#     def set_race(self, selected_value, index):
#         selected_race, race_id = selected_value
#         self.char_race = selected_race[0]
#         self.race_id = race_id
#         print(f"Selected Race: {self.char_race} (ID: {self.race_id})")

#     # Activate the game and switch from the menu to the game
#     def start_the_game(self):
#         self.game_active = True

#     # Main game loop
#     def run(self):
#         while True:
#             events = pygame.event.get()  # Get all events
#             mouse_pos = pygame.mouse.get_pos()  # Get current mouse position

#             for event in events:
#                 if event.type == pygame.QUIT:  # Exit game if the user clicks the close button
#                     pygame.quit()
#                     sys.exit()

#                 if self.game_active:  # If the game is active
#                     if event.type == pygame.KEYDOWN and event.key == pygame.K_q:  # Exit game on 'q' key press
#                         self.game_active = False

#                     if event.type == pygame.MOUSEBUTTONDOWN:  # If mouse is clicked
#                         if self.test_button.checkForInput(mouse_pos):  # Check if the test button was clicked
#                             print('test button')

#                     # Handle events for the text areas (lore and faction)
#                     self.lore_area.event_handler(event=event)
#                     self.faction_area.event_handler(event=event)

#             if self.game_active:  # If the game is active
#                 self.screen.fill('grey')  # Fill the screen with grey

#                 if self.texts_ready:  # If the texts are ready, display them
#                     self.world_lore()
#                     self.test_button.changeColor(mouse_pos)  # Change button color based on mouse hover
#                     self.test_button.update(screen=self.screen)  # Update button display
#                 else:
#                     # Display loading screen while generating the world
#                     loading_menu = pygame_menu.Menu('Loading World...', self.WIDTH, self.HEIGHT,
#                                                     theme=pygame_menu.themes.THEME_GREEN)
#                     loading_menu.add.label('Generating world, please wait...', font_size=25)
#                     loading_menu.update(events)
#                     loading_menu.draw(self.screen)

#                 pygame.display.update()  # Update the display with new content

#             else:
#                 # When the game is not active, display the menu
#                 self.screen.fill('black')  # Fill the screen with black
#                 self.menu.update(events)  # Update the menu state
#                 self.menu.draw(self.screen)  # Draw the menu on the screen

#             pygame.display.flip()  # Update the entire screen
#             self.clock.tick(self.FPS)  # Control the framerate

#             # Check if the world generation process is done
#             if not self.gen_world.is_generating:
#                 self.texts_ready = True  # Set texts ready flag to True if generation is done

# # Run the game if this file is executed
# if __name__ == '__main__':
#     game = Game()  # Create a Game object
#     game.run()  # Start the game loop
    
 
 
 
# import pygame
# import sys
# import pygame_menu

# # Define a Room class to represent each room
# class Room:
#     def __init__(self, name, description, connections):
#         self.name = name  # Room name
#         self.description = description  # Description of the room
#         self.connections = connections  # Dictionary mapping directions (e.g., 'north') to connected rooms

# # Define the main Game class
# class Game:
#     def __init__(self):
#         # Basic setup
#         self.FPS = 60
#         self.WIDTH = 800
#         self.HEIGHT = 600
#         pygame.init()
#         self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
#         self.clock = pygame.time.Clock()

#         # Set game title -the text above the game window
#         pygame.display.set_caption("Room Navigation Game")
        
#         # Game state: track the current room and position in the grid
#         self.current_room = None
#         self.create_rooms()  # Initialize the rooms and set starting room
#         self.player_position = [0, 0]  # Starting position in the map (room1)



#         # Set up a simple menu with a Play button
#         self.menu = pygame_menu.Menu('Welcome Adventurer', self.WIDTH, self.HEIGHT,
#                                      theme=pygame_menu.themes.THEME_DARK)
#         self.menu.add.button('Play', self.start_the_game)
#         self.menu.add.button('Quit', pygame_menu.events.EXIT)

#         self.game_active = False  # The game is inactive until the player presses "Play"

#         # 2D grid map representation (3x3 grid)
#         self.map_grid = [
#             ['O', 'O', 'O'],
#             ['O', '-', 'O'],
#             ['O', 'O', 'O']
#         ]

#     def create_rooms(self):
#         # Create rooms with connections to each other
#         room1 = Room('Room 1', 'This is the starting room.', {'north': 'Room 2'})
#         room2 = Room('Room 2', 'This room is north of Room 1.', {'south': 'Room 1', 'east': 'Room 3'})
#         room3 = Room('Room 3', 'This room is east of Room 2.', {'west': 'Room 2'})
        
#         # Store rooms in a dictionary for easy lookup
#         self.rooms = {
#             'Room 1': room1,
#             'Room 2': room2,
#             'Room 3': room3
#         }

#         # Set the starting room
#         self.current_room = room1

#     def start_the_game(self):
#         self.game_active = True  # Switch to game mode

#     def move_to_room(self, direction):
#         # Check if there's a room in the given direction from the current room
#         if direction in self.current_room.connections:
#             next_room_name = self.current_room.connections[direction]
#             self.current_room = self.rooms[next_room_name]
#             print(f"Moved to {self.current_room.name}")
#             # Update player position on the grid map
#             if direction == 'north':
#                 self.player_position[1] -= 1
#             elif direction == 'south':
#                 self.player_position[1] += 1
#             elif direction == 'east':
#                 self.player_position[0] += 1
#             elif direction == 'west':
#                 self.player_position[0] -= 1
#         else:
#             print("You can't move in that direction!")

#     def display_current_room(self):
#         # Display the current room's name and description
#         self.screen.fill((0, 0, 0))  # Clear screen with black
#         font = pygame.font.Font(None, 36)
#         text_surface = font.render(f"You are in {self.current_room.name}", True, (255, 255, 255))
#         self.screen.blit(text_surface, (50, 50))
        
#         description_surface = font.render(self.current_room.description, True, (255, 255, 255))
#         self.screen.blit(description_surface, (50, 100))

#     def display_map(self):
#         # Display the map in the top-right corner
#         font = pygame.font.Font(None, 36)
#         cell_size = 30  # Size of each cell in the grid
        
#         for row_idx, row in enumerate(self.map_grid):
#             for col_idx, cell in enumerate(row):
#                 # Mark the player's current location with 'X'
#                 if [col_idx, row_idx] == self.player_position:
#                     cell_text = 'X'
#                 else:
#                     cell_text = cell
                
#                 # Render each cell
#                 text_surface = font.render(cell_text, True, (255, 255, 255))
#                 self.screen.blit(text_surface, (self.WIDTH - 150 + col_idx * cell_size, 50 + row_idx * cell_size))

#     def run(self):
#         while True:
#             events = pygame.event.get()
#             for event in events:
#                 if event.type == pygame.QUIT:
#                     pygame.quit()
#                     sys.exit()

#             if self.game_active:
#                 keys = pygame.key.get_pressed()  # Get key inputs for navigation
#                 if keys[pygame.K_UP]:
#                     self.move_to_room('north')
#                 if keys[pygame.K_DOWN]:
#                     self.move_to_room('south')
#                 if keys[pygame.K_LEFT]:
#                     self.move_to_room('west')
#                 if keys[pygame.K_RIGHT]:
#                     self.move_to_room('east')

#                 # Display the current room information
#                 self.display_current_room()
#                 self.display_map()  # Display the map
#                 pygame.display.update()
#             else:
#                 # Show the menu until the player starts the game
#                 self.menu.update(events)
#                 self.menu.draw(self.screen)

#             self.clock.tick(self.FPS)

# # Run the game
# if __name__ == '__main__':
#     game = Game()
#     game.run()
