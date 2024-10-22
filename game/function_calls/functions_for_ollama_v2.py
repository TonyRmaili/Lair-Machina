import ollama
from random import randint
import json
import random
import ast


from function_calls.ollama_context import OllamaWithContext
from function_calls.ollama_dmg import OllamaDmg


# > ACTIONS

# > loot/leave - funkar - men är för stupid
# BONUS - gör så att rummen i sig har typ chest/skåp etc som kan ha items i



# > look - funkar? > bonus - gör så att rummen har beskrivningar som kan variera
# > ask > anpassa? beror på hur genererar lore
# > skillcheck (behöver göra den som layer) > describe(som slutlayer)
# > talk? > gör sen när har NPCs



# >>>>>>> combat loop/function + roll initiative call

# >>>> prova lager av llama3.2 3B - Tools om blir stökigt med massa Tools för en 3.1 8b

# >>>> prova annan språkigenkänning än whisper


# need to add current location as arg
def look_at_room(player_request: str, current_room_description: str, room_file: str):
    #make dynamic  - like = current location instead
    room_file=room_file    
    # Load room from file
    with open(room_file, 'r') as file:
        room_json = json.load(file)
        
    # make description of the room for the player
    system_prompt = f"The player is in a room with following items: {room_json}. and following room description: {current_room_description}. DO NOT DESCRIBE NEW PEOPLE OR ITEMS THAT ARE NOT IN THE INFO"
    user_prompt = player_request
    tool_used = "look_at_room"
    
    
    # Interacting with the LLaMA 3 model, with a system-level instruction
    # response = ollama.chat(
    #     model="llama3.1", 
    #     messages=[
    #         {"role": "system", "content": system_prompt},
    #         {"role": "user", "content": user_prompt}
    #     ]
    # )

    # room_intro = response['message']['content']
    return user_prompt,system_prompt, tool_used
        

# WORKS
# Function to REMOVE/loot an item from the room JSON - say LOOT to trigger 
def loot_item_from_room(item_name: str, room_file: str):
    # room file with items for current room
    room_file=room_file    
    # Load room from file
    with open(room_file, 'r') as file:
        room_json = json.load(file)
    
    item_found = False
    looted_item = None

    # print(room_json)
    updated_items = []

    for item in room_json:
        if item['name'].lower() == item_name.lower():
            looted_item = item
            item_found = True  # Item found, skip adding it to updated list
        else:
            updated_items.append(item)  # Keep the item if it doesn't match

    if item_found:
        room_json = updated_items
        
        # Save the updated room JSON back to the file
        with open(room_file, 'w') as file:
            json.dump(room_json, file, indent=4)
        
        print(f"{item_name} has been removed from the room.")
        # NEEDS TO BE DYNAMIC FOR THE ROOM WE ARE IN - SEND IN AS A ARG?
        inventory_file='inventory.json'    
        # Load room from file
        with open(inventory_file, 'r') as file:
            inventory_json = json.load(file)
        
        # Add the looted item to the inventory
        inventory_json.append(looted_item)

        # Save the updated inventory JSON back to the file
        with open(inventory_file, 'w') as file:
            json.dump(inventory_json, file, indent=4)

        # this needs fixing so not part of prompt but separate message
        user_prompt = f"item:{looted_item}"
        system_prompt = 'Give a VERY short description of the following item being looted, example: you grab the sword and put it in your backpack'
        tool_used = "loot_item_from_room"

        return user_prompt,system_prompt, tool_used

    # error handles so that if item not found it wont do the flavortext outside
    else:
        user_prompt = f"{item_name} not found in the room."
        system_prompt = False
        tool_used = "loot_item_from_room"

        return user_prompt,system_prompt, tool_used


def leave_drop_throw_item(item_name: str, room_file: str, player_action: str):
    # Path to the player's inventory file
    inventory_file = 'inventory.json'    
    
    # Load the player's inventory from file
    with open(inventory_file, 'r') as file:
        inventory_json = json.load(file)

    item_found = False
    item_to_leave = None
    updated_inventory = []

    # Search for the item in the player's inventory
    for item in inventory_json:
        if item['name'].lower() == item_name.lower():
            # Set the item player wants to leave to a variable for adding to the room later
            item_to_leave = item
            item_found = True
        else:
            updated_inventory.append(item)  # Keep the item in inventory if it doesn't match

    if item_found:
        # Update the player's inventory after removing the item
        inventory_json = updated_inventory
        
        # Save the updated inventory back to the file
        with open(inventory_file, 'w') as file:
            json.dump(inventory_json, file, indent=4)
        
        print(f"{item_name} has been removed from the inventory.")
    else:
        # if item not found - this will error handle
        user_prompt = f"{item_name} not found in the inventory."
        system_prompt = False
        
        tool_used = "leave_drop_throw_item"
        return user_prompt,system_prompt, tool_used

    ### Add the item removed from the inventory into the room JSON ###
    
    # Load the room from the room file (which is a list of items)
    with open(room_file, 'r') as file:
        room_json = json.load(file)

    # Add the removed item to the room's list
    room_json.append(item_to_leave)

    # Save the updated room JSON back to the room file
    with open(room_file, 'w') as file:
        json.dump(room_json, file, indent=4)    


    # no context here - but returns to LLM outside that uses context
    system_prompt="Give a VERY short description of the following player action, example: you gently put the sword on the floor"
    user_prompt=f"player action: {player_action}. Item refered to: {item_name} room context/items {room_json}."
    tool_used = "leave_drop_throw_item"
    
    return user_prompt,system_prompt, tool_used


def resolve_hard_action(skill: str, dc: int, player_action: str, current_room_description: str, room_file: str):
    skills = {
        'acrobatics': 2,      # Dexterity
        'animal handling': 1, # Wisdom
        'arcana': 0,          # Intelligence
        'athletics': 3,       # Strength
        'deception': 2,       # Charisma
        'history': 0,         # Intelligence
        'insight': 1,         # Wisdom
        'intimidation': 2,    # Charisma
        'investigation': 1,   # Intelligence
        'medicine': 2,        # Wisdom
        'nature': 0,          # Intelligence
        'perception': 1,      # Wisdom
        'performance': 2,     # Charisma
        'persuasion': 2,      # Charisma
        'religion': 0,        # Intelligence
        'sleight of hand': 3, # Dexterity
        'stealth': 3,         # Dexterity
        'survival': 1         # Wisdom
    }

    # Check if the skill exists in the dictionary
    if skill.lower() in skills:
        mod = skills[skill.lower()]
        roll = random.randint(1, 20)  # Roll a d20
        total = roll + mod    

    
        #make dynamic  - like = current location instead
        room_file=room_file    
        # Load room from file
        with open(room_file, 'r') as file:
            room_json = json.load(file)
            
        # add context here
        system_prompt=f"You are the dungeon master, the given the attempted action and roll, describe the outcome based on the roll and the DC. Do not mention the DC or the roll just give the description, refer to the player as 'you'. The player is in a room with following items: {room_json}. and following room description: {current_room_description}. DO NOT DESCRIBE NEW PEOPLE OR ITEMS THAT ARE NOT IN THE INFO"
        user_prompt=f"action: {player_action}, {skill} roll: {total}, vs task DC {dc}."
        tool_used = "resolve_hard_action"
        # response = ollama.chat(
        #     model="llama3.1", 
        #     messages=[
        #         {"role": "system", "content": system_prompt},
        #         {"role": "user", "content": user_prompt}
        #     ]
        # )
        
        # action_outcome = f"player attempted action: {player_action}, {skill} roll: {total}, vs task DC {dc}. {response['message']['content']}"
        
        # idea: here it could make a toolcall - > with the outcome, what should it do with the room? - remove item/HP other? update something etc
        
        
    return user_prompt,system_prompt, tool_used


def simple_task(player_action: str, current_room_description: str, room_file: str):
    
    room_file=room_file    
    # Load room from file
    with open(room_file, 'r') as file:
        room_json = json.load(file)
        
    # add context here
    system_prompt=f"You are the dungeon master, describe the player preforming the action and succeeding, make the text short and simple. ONLY ANSWER WITH the description, refer to the player as 'you'. The player is in a room with following items: {room_json}. and following room description: {current_room_description}. DO NOT DESCRIBE NEW PEOPLE OR ITEMS THAT ARE NOT IN THE INFO"
    user_prompt=f"action: {player_action}"
    tool_used = "simple_task"

    return user_prompt, system_prompt, tool_used


# name all functions that the LLM has access to
all_functions = {
    
    'look_at_room': look_at_room,
    'loot_item_from_room': loot_item_from_room,
    'leave_drop_throw_item': leave_drop_throw_item,
    'resolve_hard_action': resolve_hard_action,
    'simple_task': simple_task
    
}
