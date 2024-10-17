import ollama

from random import randint
import json

import random



def update_player_hp(player_hp_path: str, hp_change: int, reason: str):
    with open(player_hp_path, 'r') as file:
        player_data = json.load(file)
        
    
    # Update the player's HP
    player_data["hp"] += hp_change
    
    # Ensure HP doesn't drop below 0 or exceed a maximum (if applicable)
    player_data["hp"] = max(0, player_data["hp"])  # Min HP is 0, adjust as needed
    
    # Generate a message based on the HP change
    if hp_change > 0:
        message = f"Player healed by {hp_change} points due to: {reason}. Current HP: {player_data['hp']}."
    else:
        message = f"Player took {abs(hp_change)} damage due to: {reason}. Current HP: {player_data['hp']}."
    
    # Return the message as the function output
    return message

# Register the function in the all_functions dictionary
all_functions = {
    # ... (existing functions)
    'update_player_hp': update_player_hp,
    # add other functions here
}

def update_room_item(old_item_name: str, new_item_name: str, new_item_description: str, event: str, room_file: str):
    # Load the room JSON from the file (which is a list of items)
    with open(room_file, 'r') as file:
        room_json = json.load(file)

    item_found = False
    updated_room = []

    # Search for the item in the room's items list
    for item in room_json:
        if item['name'].lower() == old_item_name.lower():
            # Item found, replace it with the new item
            print(f"Replacing {old_item_name} with {new_item_name}")
            updated_room.append({
                "name": new_item_name,
                "description": new_item_description
            })
            item_found = True
        else:
            # Keep other items unchanged
            updated_room.append(item)

    if item_found:
        # Save the updated room JSON back to the room file
        with open(room_file, 'w') as file:
            json.dump(updated_room, file, indent=4)

        return f"The {old_item_name} has been replaced by a {new_item_name}, {new_item_description} in the room, because {event}."
    else:
        return f"{old_item_name} not found in the room."



def update_inventory_item(old_item_name: str, new_item_name: str, new_item_description: str, event: str, inventory_file: str):
    # Load the player's inventory JSON from the file
    with open(inventory_file, 'r') as file:
        inventory_json = json.load(file)

    item_found = False
    updated_inventory = []

    # Search for the item in the player's inventory list
    for item in inventory_json['inventory']:
        if item['name'].lower() == old_item_name.lower():
            # Item found, replace it with the new item
            print(f"Replacing {old_item_name} with {new_item_name} in inventory.")
            updated_inventory.append({
                "name": new_item_name,
                "description": new_item_description
            })
            item_found = True
        else:
            # Keep other items unchanged
            updated_inventory.append(item)

    if item_found:
        # Save the updated inventory JSON back to the inventory file
        with open(inventory_file, 'w') as file:
            json.dump({"inventory": updated_inventory}, file, indent=4)

        return f"The {old_item_name} has been replaced by a {new_item_name}, {new_item_description} in the inventory, because {event}."
    else:
        return f"{old_item_name} not found in the inventory."





# name all functions that the LLM has access to
all_functions = {
    
    'update_player_hp': update_player_hp,
    'update_room_item': update_room_item,
    'update_inventory_item': update_inventory_item
        
    
}
