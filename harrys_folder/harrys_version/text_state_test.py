

"""
the idea is to save each room state in a text block, so that it can change it easy, seems to work? will need more tests to find the problems
---need a JSON style, thing with names for next room - and then that it knows to switch


"""


import ollama


# example of a input text function

def system_prompt_function(system_prompt, user_prompt):
    # Interacting with the LLaMA 3 model, with a system-level instruction
    response = ollama.chat(
        model="llama3.1", 
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    return response['message']['content']





import requests
import json

import os


def open_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def save_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)


    
# Load rooms from a JSON file
def load_rooms(json_file):
    with open(json_file, 'r') as file:
        return json.load(file)['rooms']

# Switch room based on player input (movement logic)
def move_player(current_coordinates, direction, rooms):
    x, y = map(float, current_coordinates.split('.'))
    
    if direction == 'up':
        x += 1
    elif direction == 'down':
        x -= 1
    elif direction == 'left':
        y -= 1
    elif direction == 'right':
        y += 1
    else:
        print("Invalid direction.")
        return current_coordinates  # No movement
   
    new_coordinates = f"{int(x)}.{int(y)}"
    
    if new_coordinates in rooms:
        return new_coordinates  # Valid move
    else:
        print("You can't move in that direction.")
        return current_coordinates  # Invalid move, stay in the same room


def print_map(rooms, current_location):
    # Create a fixed 10x10 grid initialized with "-" for impassable areas
    grid = [[' - ' for _ in range(10)] for _ in range(10)]
    
    # Populate the grid with "O" where there are rooms
    for coord in rooms:
        x, y = map(int, coord.split('.'))
        if 0 <= x < 10 and 0 <= y < 10:
            grid[x][y] = ' O '  # Mark room locations

    # Mark the current player location with "X"
    x, y = map(int, current_location.split('.'))
    if 0 <= x < 10 and 0 <= y < 10:
        grid[x][y] = ' X '  # Override with player's current location

    # Print the grid with coordinates
    print("Map Layout (you are at X):")
    print("    " + "   ".join(str(i) for i in range(10)))  # Print top coordinate row
    for i, row in enumerate(grid):
        print(f"{i} |" + "|".join(row))  # Print each row with left coordinate column


def get_adjacent_moves(current_coordinates, rooms):
    x, y = map(int, current_coordinates.split('.'))
    directions = {
        'up': f"{x + 1}.{y}",
        'down': f"{x - 1}.{y}",
        'left': f"{x}.{y - 1}",
        'right': f"{x}.{y + 1}"
    }
    valid_moves = {dir: coord for dir, coord in directions.items() if coord in rooms}
    return valid_moves


def main():
    
    json_file = 'castle_map.json'  # JSON file containing rooms and coordinates
    rooms = load_rooms(json_file)  # Load the rooms from JSON
    player_location = '0.1'  # Default starting location (Living Room)
    first_entry = True  # Flag to check if the player has just entered a room

    
    
    while True:
        # setting current room from JSON with castle layout
        current_room = rooms[player_location]
        # setting text file for current room
        room_file = current_room['file']
        # opening it to read and get/edit content
        room_description = open_file(room_file)
        
        print(f"\nYou are in: {current_room['name']} at {player_location}")
        # print(f"Description: {room_description}")
        
        # Display room intro only on entering the room or first start
        if first_entry:
            # call map print
            print_map(rooms, player_location)  # Display the map
            
            # make description of new room for the player
            system_prompt = f"The player is in {current_room['name']} room description: {room_description}, describe the room as if you were a dungeon master based on the info you have"
            user_prompt = "Player action: I enter the room and look around, what do I see?"
            room_intro = system_prompt_function(system_prompt, user_prompt)
            
            input("press enter to continue")
            # clear terminal of map
            os.system('clear')
            
            print(room_intro)
            first_entry = False  # Set the flag to False after the first entry
        
        
        
        # Player action menu
        print("Choose an action:")
        print("1. Move")
        print("2. Interact with the environment")
        action_choice = input("Enter your choice (1 or 2): ")
        # clear after made choice
        os.system('clear')

        if action_choice == '1':  # Movement logic
            valid_moves = get_adjacent_moves(player_location, rooms)
            print("Available moves:")
            for direction, location in valid_moves.items():
                print(f"{direction} to {rooms[location]['name']} at {location}")
            move_choice = input("Which direction? ")
            if move_choice in valid_moves:
                player_location = valid_moves[move_choice]
                print(f"Moving {move_choice} to {rooms[player_location]['name']}...\n")
                # Handle room movement
                first_entry = True #update so it makes a description of the new room
                # clear
                os.system('clear')
                continue  # Restart loop to show new room info
            else:
                print("Invalid move. Try again.")
        elif action_choice == '2':  # Interaction logic
            player_action = input("What do you want to do? ")
            # Further interaction logic goes here
            print(f"You chose to: {player_action}")
            # update the current room description
            system_prompt = f"Update the following room description based on the player's action, DO NOT WRITE 'here is the description:', ONLY ANSWER with the updated description of the room. room name: {current_room['name']} room description: {room_description}"
            user_prompt = f"Player action: {player_action}"
            modified_content = system_prompt_function(system_prompt, user_prompt)
            
            # Save the new room state to the associated text file
            save_file(room_file, modified_content)
            
            print("\nUpdated room state:")
            print(modified_content)
            
            # maybe add a separate layer that changes the text, so that it describes the action, and a separate call updates the text
            
        else:
            print("Invalid choice. Please select 1 or 2.")

        



if __name__ == '__main__':
    main()