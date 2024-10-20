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



# maybe with ADD keyword?

# def does_this_action_lead_to_adding_a_new_item(prompt: str):
#     system= 'how would you update the room if the player does this action? YOU ONLY ANSWER with ADD_ITEM: item_name, item_description, REMOVE_ITEM: item_name, item_description, CHANGE_ITEM: item_name, item_description, or NO_CHANGE'
#     prompt = prompt
    
#     resp = ollama.generate(
#         model='llama3.1',
#         prompt=prompt,
#         system=system

#     )
    
#     return resp['response']



# def does_this_item_need_to_be_updated(prompt: str):
#     system= 'You must evaluate if the item needs to be updated. YOU ONLY ANSWER yes OR no'
#     prompt = prompt
    
#     resp = ollama.generate(
#         model='llama3.1',
#         prompt=prompt,
#         system=system

#     )
    
#     return resp['response']



# def make_item_description(prompt: str):
#     system= 'write a new description/state for the item to match the new state of the item after the event. write the same description if it doesnt change ONLY ANSWER with the new description'
#     prompt = prompt
    
#     resp = ollama.generate(
#         model='llama3.1',
#         prompt=prompt,
#         system=system

#     )
    
#     return resp['response']


#             #   "required": ["item_name", "new_item_description", "event", "room_file", "inventory_file"]
def update_item_description(item_name: str, new_item_description: str, event: str, room_file: str, inventory_file: str):

    prompt=f'current item:{item_name}, new description: {new_item_description}, what happened: {event}'
    
    # new_item_description=make_item_description(prompt=prompt)
    system= 'write a new description/state for the item to match the new state of the item after the event. write the same description if it doesnt change ONLY ANSWER with the new description'
    prompt = prompt
    
    resp = ollama.generate(
        model='llama3.1',
        prompt=prompt,
        system=system

    )
    
    new_item_description= resp['response']

    # Load the room JSON from the file (which is a list of items)
    with open(room_file, 'r') as file:
        room_json = json.load(file)

    item_found = False
    updated_room = []

    # Search for the item in the room's items list
    for item in room_json:
        if item['name'].lower() == item_name.lower():
            # Item found, replace it with the new item
            print(f"Replacing {item_name} description : {new_item_description} ")
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
            print(f"Replacing {item_name} description with {new_item_description}")
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

        return f"The {item_name} has been replaced by a {item_name}, {new_item_description} in the inventory, because {event}."
    else:
        return f"{item_name} not found in inventory or the room."





# 1 player does action
# 2 generate context blablab det vi har gjort hittills
# 3 - did it do dmg ? - return yes/no? - and how much
# 4 - how much dmg, why?

# def update_player_hp(player_hp_path: str, hp_change: int, reason: str):
#     with open(player_hp_path, 'r') as file:
#         player_data = json.load(file)
        
    
#     # Update the player's HP
#     player_data["hp"] += hp_change
    
#     # Ensure HP doesn't drop below 0 or exceed a maximum (if applicable)
#     player_data["hp"] = max(0, player_data["hp"])  # Min HP is 0, adjust as needed
    
#     # Generate a message based on the HP change
#     if hp_change > 0:
#         message = f"Player healed by {hp_change} points due to: {reason}. Current HP: {player_data['hp']}."
#     else:
#         message = f"Player took {abs(hp_change)} damage due to: {reason}. Current HP: {player_data['hp']}."
    
#     # Return the message as the function output
#     return message

# Register the function in the all_functions dictionary
all_functions = {
    'update_item_description': update_item_description
}




# def update_inventory_item(old_item_name: str, new_item_name: str, new_item_description: str, event: str, inventory_file: str):
#     # Load the player's inventory JSON from the file
#     with open(inventory_file, 'r') as file:
#         inventory_json = json.load(file)

#     item_found = False
#     updated_inventory = []

#     # Search for the item in the player's inventory list
#     for item in inventory_json['inventory']:
#         if item['name'].lower() == old_item_name.lower():
#             # Item found, replace it with the new item
#             print(f"Replacing {old_item_name} with {new_item_name} in inventory.")
#             updated_inventory.append({
#                 "name": new_item_name,
#                 "description": new_item_description
#             })
#             item_found = True
#         else:
#             # Keep other items unchanged
#             updated_inventory.append(item)

#     if item_found:
#         # Save the updated inventory JSON back to the inventory file
#         with open(inventory_file, 'w') as file:
#             json.dump({"inventory": updated_inventory}, file, indent=4)

#         return f"The {old_item_name} has been replaced by a {new_item_name}, {new_item_description} in the inventory, because {event}."
#     else:
#         return f"{old_item_name} not found in the inventory."





# name all functions that the LLM has access to
# all_functions = {
    
#     'update_player_hp': update_player_hp,
#     'update_room_item': update_room_item,
#     'update_inventory_item': update_inventory_item
        
    
# }


# if __name__=='__main__':
#     # prompt= 'the music box explodes upon pickup! sending sparks and flame everywere'
#     # resp = will_the_player_take_damage(prompt)

#     # if resp.lower() == 'yes':
#     #     damamge_resp = player_takes_damage(prompt)
#     #     print(damamge_resp)
    
#     # else:
#     #     print('no damage')
    
#     # prompt = 'item: wood sword. description: a wooden sword made out of oak. Event: you hit the wall with the sword but nothing happens'
#     # resp = update_item_name_and_description(prompt)
#     # print(resp)
    
#     prompt = 'flip the desk over'
#     items = 'music box, star map, mirror, wooden desk'
#     resp = does_this_action_lead_to_adding_a_new_item(prompt=f'action:{prompt}. current items in room: {items}')
#     print(resp)
    