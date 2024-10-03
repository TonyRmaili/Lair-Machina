import pygame
import pygame_menu
import sys



# IT WORKS TO MOVE AROUND AND CHANGE FLOOR. Need to have dynamic function for change floor, so takes floor as argument from list of floors, and import the room info etc

# TO DO:
# make floor change dynamic
# add items to rooms
# add inventory/hp etc screen 
# import the loot actions from before
# add the img generation call from before

# test to add music generation and speech and see how slow it gets

###make combat loop###
# add monsters, call for initative, combat mode etc



# Define a Room class to represent each room
class Room:
    def __init__(self, name, description, connections, special=None):
        self.name = name  # Room name
        self.description = description  # Room description
        self.connections = connections  # Dictionary mapping directions (e.g., 'north') to connected rooms
        self.special = special  # Special feature (e.g., 'exit', 'up-floor', 'down-floor')


class Game:
    def __init__(self):
        # Basic setup
        self.WIDTH = 800
        self.HEIGHT = 600
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()  # Clock object to control the game's framerate
        self.FPS = 60

        # Game state: track the current room and position in the grid
        self.current_room = None
        self.player_position = [2, 2]  # Starting position in the map (Room 1)
        self.special_action_available = None  # To track if a special action is available
        self.game_exit = False  # Flag to handle game exit

        # Create rooms and set up the initial floor
        self.create_rooms()

        # Create a custom theme
        my_theme = pygame_menu.themes.THEME_DARK.copy()  # Start with the dark theme
        my_theme.title_font_color = (255, 215, 0)  # Set title color to gold
        my_theme.widget_font_color = (0, 255, 0)  # Set button text color to green
        my_theme.background_color = (50, 50, 50)  # Set the background to a dark grey
        my_theme.widget_font = pygame_menu.font.FONT_FRANCHISE  # Custom font (optional)

        # Set up a menu with custom colors
        self.menu = pygame_menu.Menu('Welcome Adventurer', self.WIDTH, self.HEIGHT, theme=my_theme)
        self.menu.add.button('Play', self.start_the_game)
        self.menu.add.button('Quit', pygame_menu.events.EXIT)

        self.game_active = False  # The game is inactive until the player presses "Play"

    def create_rooms(self):
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

    def start_the_game(self):
        self.game_active = True  # Switch to game mode

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
        self.game_active = False
        self.game_exit = True  # Add a new attribute to handle game exit

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

    def run(self):
        self.game_exit = False  # Initialize the game exit flag

        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if self.game_active:
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
                else:
                    # Update menu
                    self.menu.update(events)

            if self.game_active:
                # Display the current room information
                self.display_current_room()
                self.display_map()  # Display the map
                pygame.display.update()
            else:
                # Draw the menu
                self.menu.draw(self.screen)
                pygame.display.update()

            self.clock.tick(self.FPS)

            # If game_exit is triggered, exit the loop
            if self.game_exit:
                pygame.quit()
                sys.exit()


if __name__ == '__main__':
    game = Game()
    game.run()