from random import randint
import json

import random


# Function to REMOVE an item from the room JSON ####add , room_json as argument
def remove_item_from_room(item_name: str):

    # NEEDS TO BE DYNAMIC FOR THE ROOM WE ARE IN - SEND IN AS A ARG?
    room_file='room_json.json'    
    # Load room from file
    with open(room_file, 'r') as file:
        room_json = json.load(file)

    
    item_found = False

    # print(room_json)
    updated_items = []

    for item in room_json['items']:
        if item['name'].lower() == item_name.lower():
            item_found = True  # Item found, skip adding it to updated list
        else:
            updated_items.append(item)  # Keep the item if it doesn't match

    if item_found:
        room_json['items'] = updated_items
        
        # Save the updated room JSON back to the file
        with open(room_file, 'w') as file:
            json.dump(room_json, file, indent=4)
        
        return f"{item_name} has been removed from the room."
    else:
        return f"{item_name} not found in the room."




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
    'remove_item_from_room': remove_item_from_room
}



