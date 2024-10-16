import ollama

from random import randint
import json

import random


# DONE:
# 1 install ComfyUI + flux on server  - WORKS
# 2 when it works - try to set up api/fetch thing to generate img - WORKS (maybe try websocket later if time)






# TO DO : 

# > prova ljud generator - antingen jukebox eller midi style
# >fixa bättre calls för bild och musik > så hamnar i rätt mapp etc (eventuellt funkar bättre med sockets?)


# > ACTIONS
# > loot/leave - funkar - men behöver ta in room_json som argument > BONUS - gör så att rummen i sig har typ chest/skåp etc som kan ha items i
# > look - funkar? > bonus - gör så att rummen har beskrivningar som kan variera
# > ask > anpassa? beror på hur genererar lore
# > skillcheck (behöver göra den som layer) > describe(som slutlayer)

# > talk? > gör sen när har NPCs


# Generators/functions to make:
# >>>>>>> generate dungeon/castle/etc loop 
# >>>>>>> create character loop/stage
# >>>>>>> create state/json - time/location/hp/etc

# >>>>>>> combat loop/function + roll initiative call

# >>>> prova lager av llama3.2 3B - Tools om blir stökigt med massa Tools för en 3.1 8b

# >>>> prova annan språkigenkänning än whisper



# need to add current location as arg
def look_at_room(current_room_description: str, room_file: str):
    #make dynamic  - like = current location instead
    room_file=room_file    
    # Load room from file
    with open(room_file, 'r') as file:
        room_json = json.load(file)
        
    # make description of the room for the player
    system_prompt = f"The player is in a room with following items: {room_json}. and following room description: {current_room_description}. Describe what the player sees when they look around as if you were a dungeon master based on the info you have about the room"
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
        
# def ask_stuff(player_question: str, room_file: str):

#     #make dynamic 
#     lore_file='lore.txt'
#     # Load room from file
#     with open(lore_file, 'r') as file:
#         lore = file.read()

#     # make description of the room for the player - need to work on prompt and the lore its given /scope etc- but works as POC
#     system_prompt = f"The game is set in this world: {lore}. try to answer any questions the player has with only describing some parts that a player character may know. Answer with describing what the character knows and how they know it as if you are the dungeon master"
#     user_prompt = f"Player action: {player_question}"
        
    
#     # Interacting with the LLaMA 3 model, with a system-level instruction
#     response = ollama.chat(
#         model="llama3.1", 
#         messages=[
#             {"role": "system", "content": system_prompt},
#             {"role": "user", "content": user_prompt}
#         ]
#     )
    
#     dm_answer = response['message']['content']

    
#     return dm_answer
# make a similar for action/roll result descriptions
# Describe the result as the player tries to do the action as if you were a dungeon master based on the info you have



# WORKS
# Function to REMOVE/loot an item from the room JSON - and add it to the player inventory -  ####add , room_json as argument
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
        inventory_file='inventory_json.json'    
        # Load room from file
        with open(inventory_file, 'r') as file:
            inventory_json = json.load(file)
        
        # Add the looted item to the inventory
        inventory_json['inventory'].append(looted_item)
        
        # Save the updated inventory JSON back to the file
        with open(inventory_file, 'w') as file:
            json.dump(inventory_json, file, indent=4)

        return (f"{looted_item} now in player inventory")
        
    else:
        return f"{item_name} not found in the room."


# # Function to ADD an item to the room JSON - AND remove it from the players inventory
# # def leave_item_from_inventory_in_room(item_name: str, item_description: str, room_json, file_path: str):
# def leave_item_from_inventory_in_room(item_name: str, room_file: str):
    
#     room_file = room_file
#     inventory_file='inventory_json.json'    
#     # Load inventory from file
#     with open(inventory_file, 'r') as file:
#         inventory_json = json.load(file)

    
#     item_found = False

#     updated_items = []

#     for item in inventory_json['inventory']:
#         if item['name'].lower() == item_name.lower():
#             # set the item player wants to leave to variable for adding in room later
#             item_to_leave = item_name
#             item_found = True  # Item found, skip adding it to updated list
#         else:
#             updated_items.append(item)  # Keep the item if it doesn't match

#     if item_found:
#         inventory_json['inventory'] = updated_items
        
#         # Save the updated inventory JSON back to the file
#         with open(inventory_file, 'w') as file:
#             json.dump(inventory_json, file, indent=4)
        
#         print(f"{item_name} has been removed from inventory.")
#     else:
#         return f"{item_name} not found in inventory."

#     ### ADDS ITEM REMOVED FROM INVENTORY TO ROOM JSON ###
#     # NEEDS TO BE DYNAMIC FOR THE ROOM WE ARE IN - SEND IN AS A ARG?
#     room_file=room_file    
#     # Load room from file
#     with open(room_file, 'r') as file:
#         room_json = json.load(file)

#     updated_items = []


#     for item in room_json:
#         updated_items.append(item)  # Keep the item if it doesn't match

        
#     # # Create a new item dictionary
#     # new_item = {
#     #     "name": item_name,
#     #     "description": item_description,
#     #     "properties": {
#     #         "interact": True,
#     #         "examine": True
#     #     }
#     # }
    
#     new_item = item_to_leave
    
#     # Add the new item to the room's items list
#     updated_items.append(new_item)

#     #change the json to updated 
#     room_json = updated_items
    
#     # Save the updated room JSON back to the file
#     with open(room_file, 'w') as file:
#         json.dump(room_json, file, indent=4)
        
#     return f"{item_name} has been added to the room."

def leave_item_from_inventory_in_room(item_name: str, room_file: str):
    # Path to the player's inventory file
    inventory_file = 'inventory_json.json'    
    
    # Load the player's inventory from file
    with open(inventory_file, 'r') as file:
        inventory_json = json.load(file)

    item_found = False
    item_to_leave = None
    updated_inventory = []

    # Search for the item in the player's inventory
    for item in inventory_json['inventory']:
        if item['name'].lower() == item_name.lower():
            # Set the item player wants to leave to a variable for adding to the room later
            item_to_leave = item
            item_found = True
        else:
            updated_inventory.append(item)  # Keep the item in inventory if it doesn't match

    if item_found:
        # Update the player's inventory after removing the item
        inventory_json['inventory'] = updated_inventory
        
        # Save the updated inventory back to the file
        with open(inventory_file, 'w') as file:
            json.dump(inventory_json, file, indent=4)
        
        print(f"{item_name} has been removed from the inventory.")
    else:
        return f"{item_name} not found in the inventory."

    ### Add the item removed from the inventory into the room JSON ###
    
    # Load the room from the room file (which is a list of items)
    with open(room_file, 'r') as file:
        room_json = json.load(file)

    # Add the removed item to the room's list
    room_json.append(item_to_leave)

    # Save the updated room JSON back to the room file
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
    'look_at_room': look_at_room
}


    # 'ask_stuff': ask_stuff,

# to do:
# make sure look, skill, loot and leave works
# add flavor call at the end of action