import ollama

from random import randint
import json

import random

# TOO STUPID FOR THIS
# - does this action need to be resolved with a roll - yes/no 
# - does this item need to be updated - yes/no - what is the new item name and description 
# - will this action result in a change in the room - yes/no - what is the new room description
# - will this action consume the item - yes/no - what is the new item description ---- would instead need a USE keyword and some trigger to remove the item afterwards

# WORKS SORT OF
#  do action - will the player take damage - yes/no  - how much damage X


# TO DO:
# UPDATE ROOM DESCRIPTION
# UPDATE ITEM DESCRIPTION (BOTH INVENTORY AND ROOM)


# SOME SORT OF GAME LOGIC, like a locked door, need to find the key? - maybe LLM can have access to make key? tool? too messy? how else?
# MAYBE TRAPPED items?- so that if take- trigger TRAP?





#             #   "required": ["item_name", "new_item_description", "event", "room_file", "inventory_file"]
def update_item_description(item_name: str, new_item_description: str, event: str, room_file: str):
    inventory_file = '/home/student/harry_and_tony_project/Lair-Machina/game/inventory.json'
    prompt=f'current item:{item_name}, new description: {new_item_description}, what happened: {event}'
    
    # new_item_description=make_item_description(prompt=prompt)
    system= 'write a new description/state for the item to match the new state of the item after the event. write the same description if it doesnt change ONLY ANSWER with the new description'
    prompt = prompt


    try:    
        resp = ollama.generate(
            model='llama3.1',
            prompt=prompt,
            system=system

        )
        new_item_description= resp['response']

    except Exception as e:
        print(f"Error generating new item description: {e}")
        return "Failed to generate a new item description."    


    # Load the room JSON from the file (which is a list of items)
    with open(room_file, 'r') as file:
        room_json = json.load(file)

    item_found = False
    updated_room = []

    # Search for the item in the room's items list
    for item in room_json:
        if item['name'].lower() == item_name.lower():
            # Item found, replace it with the new item
            # print(f"Replacing {item_name} description : {new_item_description} ")
            updated_room.append({
                "name": item_name,
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

        return f"The {item_name}, got new description: {new_item_description} because {event}."
    else:
        print(f"{item_name} not found in the room.")
        # Load the inventory JSON from the file (which is a list of items)
        with open(inventory_file, 'r') as file:
            inventory_json = json.load(file)

        item_found = False
        updated_inventory = []

        # Search for the item in the inventory's items list
        for item in inventory_json:
            if item['name'].lower() == item_name.lower():
                # Item found, replace it with the new item
                # print(f"Replacing {item_name} description with {new_item_description}")
                updated_inventory.append({
                    "name": item_name,
                    "description": new_item_description
                })
                item_found = True
            else:
                # Keep other items unchanged
                updated_inventory.append(item)

        if item_found:
            # Save the updated inventory JSON back to the inventory file
            with open(inventory_file, 'w') as file:
                json.dump(updated_inventory, file, indent=4)
            
            print(f"The {item_name} has been replaced by a {item_name}, {new_item_description} in the inventory, because {event}.")
            return 
        else:
            print(f"{item_name} not found in inventory or the room.")
            return







# Register the function in the all_functions dictionary
all_functions = {
    'update_item_description': update_item_description
}
