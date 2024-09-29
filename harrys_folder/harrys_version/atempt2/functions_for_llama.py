import ollama

from random import randint
import json

import random



# need to add current location as arg
def look_at_room(current_location):
    #make dynamic  - like = current location instead
    room_file='room_json.json'    
    # Load room from file
    with open(room_file, 'r') as file:
        room_json = json.load(file)
        
    # make description of the room for the player
    system_prompt = f"The player is in a room with following items and properties: {room_json}. Describe what the player sees when they look around as if you were a dungeon master based on the info you have about the room"
    user_prompt = "Player action: I look around, what do I see?"
    
    
    # Interacting with the LLaMA 3 model, with a system-level instruction
    response = ollama.chat(
        model="llama3.1", 
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    room_intro = response['message']['content']
    
    return room_intro
        
def ask_stuff(player_question):

    #make dynamic 
    lore_file='lore.txt'
    # Load room from file
    with open(lore_file, 'r') as file:
        lore = file.read()

    # make description of the room for the player - need to work on prompt and the lore its given /scope etc- but works as POC
    system_prompt = f"The game is set in this world: {lore}. try to answer any questions the player has with only describing some parts that a player character may know. Answer with describing what the character knows and how they know it as if you are the dungeon master"
    user_prompt = f"Player action: {player_question}"
        
    
    # Interacting with the LLaMA 3 model, with a system-level instruction
    response = ollama.chat(
        model="llama3.1", 
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    
    dm_answer = response['message']['content']

    
    return dm_answer
# make a similar for action/roll result descriptions
# Describe the result as the player tries to do the action as if you were a dungeon master based on the info you have



# WORKS
# Function to REMOVE/loot an item from the room JSON - and add it to the player inventory -  ####add , room_json as argument
def loot_item_from_room(item_name: str):

    # NEEDS TO BE DYNAMIC FOR THE ROOM WE ARE IN - SEND IN AS A ARG?
    room_file='room_json.json'    
    # Load room from file
    with open(room_file, 'r') as file:
        room_json = json.load(file)
    
    item_found = False
    item_looted = None

    # print(room_json)
    updated_items = []

    for item in room_json['items']:
        if item['name'].lower() == item_name.lower():
            looted_item = item
            item_found = True  # Item found, skip adding it to updated list
        else:
            updated_items.append(item)  # Keep the item if it doesn't match

    if item_found:
        room_json['items'] = updated_items
        
        # Save the updated room JSON back to the file
        with open(room_file, 'w') as file:
            json.dump(room_json, file, indent=4)
        
        print(f"{item_name} has been removed from the room.")
        # NEEDS TO BE DYNAMIC FOR THE ROOM WE ARE IN - SEND IN AS A ARG?
        inventory_file='character_inventory.json'    
        # Load room from file
        with open(inventory_file, 'r') as file:
            inventory_json = json.load(file)
        
        # Add the looted item to the inventory
        inventory_json['items'].append(looted_item)
        
        # Save the updated inventory JSON back to the file
        with open(inventory_file, 'w') as file:
            json.dump(inventory_json, file, indent=4)

        return (f"{looted_item} now in player inventory")
        
    else:
        return f"{item_name} not found in the room."




# 
# Function to ADD an item to the room JSON - AND remove it from the players inventory
# def leave_item_from_inventory_in_room(item_name: str, item_description: str, room_json, file_path: str):
def leave_item_from_inventory_in_room(item_name: str):
    
    
    inventory_file='character_inventory.json'    
    # Load inventory from file
    with open(inventory_file, 'r') as file:
        inventory_json = json.load(file)

    
    item_found = False

    updated_items = []

    for item in inventory_json['items']:
        if item['name'].lower() == item_name.lower():
            # set the item player wants to leave to variable for adding in room later
            item_to_leave = item_name
            item_found = True  # Item found, skip adding it to updated list
        else:
            updated_items.append(item)  # Keep the item if it doesn't match

    if item_found:
        inventory_json['items'] = updated_items
        
        # Save the updated inventory JSON back to the file
        with open(inventory_file, 'w') as file:
            json.dump(inventory_json, file, indent=4)
        
        print(f"{item_name} has been removed from inventory.")
    else:
        return f"{item_name} not found in inventory."

    ### ADDS ITEM REMOVED FROM INVENTORY TO ROOM JSON ###
    # NEEDS TO BE DYNAMIC FOR THE ROOM WE ARE IN - SEND IN AS A ARG?
    room_file='room_json.json'    
    # Load room from file
    with open(room_file, 'r') as file:
        room_json = json.load(file)

    updated_items = []


    for item in room_json['items']:
        updated_items.append(item)  # Keep the item if it doesn't match

        
    # # Create a new item dictionary
    # new_item = {
    #     "name": item_name,
    #     "description": item_description,
    #     "properties": {
    #         "interact": True,
    #         "examine": True
    #     }
    # }
    
    new_item = item_to_leave
    
    # Add the new item to the room's items list
    updated_items.append(new_item)

    #change the json to updated 
    room_json['items'] = updated_items
    
    # Save the updated room JSON back to the file
    with open(room_file, 'w') as file:
        json.dump(room_json, file, indent=4)
        
    return f"{item_name} has been added to the room."






# MAKE SKILLCHECK - works
def roll_skill_with_mod(skill: str) -> str:
    # Dictionary of D&D skills with corresponding modifiers
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
        return f"Rolled {roll} for {skill}, with a modifier of {mod}. Total: {total}"
    else:
        return "Invalid skill."


# name all functions that the LLM has access to
all_functions = {
    
    'roll_skill_with_mod':roll_skill_with_mod,
    'loot_item_from_room': loot_item_from_room,
    'leave_item_from_inventory_in_room': leave_item_from_inventory_in_room,
    'ask_stuff': ask_stuff,
    'look_at_room': look_at_room
}



