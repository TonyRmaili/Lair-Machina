

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


# returns the possible moves from the room you are in
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



# INVENTORY FUNCTIONS 
# checks if the item the player want to take is in the room and return FALSE or the name of the item in CAPS 
def check_room_items(player_action, room_items):
    system_prompt = f"What item does the player want to take in the player action? answer ONLY WITH THE ITEM NAME IN CAPS            exampel: player action: I want to take the robe. ROBE"
    user_prompt = f"Player action: {player_action}"
    item_to_take = system_prompt_function(system_prompt, user_prompt)
    input(item_to_take)
    
    system_prompt = f"Does the item to take, exists in the current room inventory/description:{room_items}? answer in caps YES or NO? why?"
    user_prompt = f"item to take: {item_to_take}"
    item_exists = system_prompt_function(system_prompt, user_prompt)
    input(item_exists)
    if "NO" in item_exists:
        input(f"debugg- LLM think {item_to_take} does not exists in the room {room_items}")
        return False
    else:
        input(f"it appears you can do following action {player_action} with regards to items in the room")
        return item_to_take


# ######### need to change room state in less drastic way- maybe have some things that cant be changed? -like a base - then lists of current items > then state log?
# update room txt to no longer have looted item
def update_room_after_take(item_to_take, room_items):
    system_prompt = f"Update the following room description to NOT INCLUDE the item the player took, DO NOT WRITE 'here is the description:', ONLY ANSWER with the updated description of the room where you removed the item that was taken. room description: {room_items}"
    user_prompt = f"Item player took: {item_to_take}"
    modified_content = system_prompt_function(system_prompt, user_prompt)
    
    room_file = 'living_room_state.txt'
    # Save the new room state to the associated text file
    save_file(room_file, modified_content)
    
    print("\nUpdated room state:")
    print(modified_content)

# add, item_description as input later
def add_to_inventory(item_name):
    file_path = 'inventory_test.txt'
    
    item_name_upper = item_name.upper()
    
    # Construct the line to add to the inventory file
    new_line = f"{item_name_upper}\n"  #, {item_description}
    
    # Append the new item to the file
    with open(file_path, 'a') as file:
        file.write(new_line)
    
    # Read the updated inventory and print it
    with open(file_path, 'r') as file:
        inventory_contents = file.read()
        print(inventory_contents)





# loop for entering a castle/dungeon whatever - dungeon crawl mode (still need way to end/exit cave, and go to "world mode")
def main():
    
    json_file = 'castle_map.json'  # JSON file containing rooms and coordinates
    rooms = load_rooms(json_file)  # Load the rooms from JSON
    player_location = '0.1'  # Default starting location (Living Room)
    first_entry = True  # Flag to check if the player has just entered a room

    
    
    while True:
        
        """
        the loop works by -
        1. telling you where you are - show the map.
        1.1 - if it "first_entry" - a new room, give you a description > WORKS, doesnt change anything- maybe add so that you can choose to skipp room description?- (like if you want to go back its not fun to load all text again)
        2. chose a action - move or action/interact 
        2.1 - if move -> move options by getting adjacent rooms and ask where you want to go > WORKS
        2.2 - if action - ask for action (expand this to include take, use item, or other? (maybe talk/lore- later? )) > need to find a good way to handle this. - > states change too much - > maybe JSON anyway? 
        3. gives text/description what happend and updates the room txt 
        """
        
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
        print("3. take item")
        print("4. use item in inventory")
        # print("5. ask/look/lore")
        
        
        action_choice = input("Enter your choice (1, 2, 3 or 4): ")
        # clear after made choice
        os.system('clear')


        # MOVE
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
        # INTERACT
        elif action_choice == '2':  # Interaction logic
            player_action = input("What do you want to do? ")
            # Further interaction logic goes here
            print(f"You chose to: {player_action}")
            # describe the action -- maybe ask for a roll here(?)
            system_prompt = f"You are the dungeon master describe what happens as the player attempts given Player action. room name: {current_room['name']} room description: {room_description}"
            user_prompt = f"Player action: {player_action}"
            flavor_text_player_action = system_prompt_function(system_prompt, user_prompt)
            print(flavor_text_player_action)


            # maybe instead of update have a separate log for actions and for room state? - problem now is it changes the room description too much - 
            # update the current room description
            system_prompt = f"Update the following room description based on the player's action and the description, DO NOT WRITE 'here is the description:', ONLY ANSWER with the updated description/state of the room. room name: {current_room['name']} room description/state: {room_description}"
            user_prompt = f"Player action: {player_action}, {flavor_text_player_action}"
            modified_content = system_prompt_function(system_prompt, user_prompt)
            
            # Save the new room state to the associated text file - maybe append instead? - with date log? - then summerize once each X actions?
            save_file(room_file, modified_content)
            
            print("\nUpdated room state:")
            print(modified_content)
            input("press enter to continue..")
            # maybe add a separate layer that changes the text, so that it describes the action, and a separate call updates the text
        # TAKE ITEM FROM ROOM
        elif action_choice == '3':
            
            player_action = input("what would you like to loot /take ?")
            # add to inventory - needs to have similar LLM check if item is in the room
            print(room_description)
            item_to_add=check_room_items(player_action, room_description)
            if item_to_add:
                add_to_inventory(item_to_add)
                # also needs to be removed from room
                update_room_after_take(item_to_add, room_description)

            
        else:
            print("Invalid choice. Please select 1-4.")

        



if __name__ == '__main__':
    main()