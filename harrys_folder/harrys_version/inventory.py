"""
test for inventory - idea is that each item has attributes and that the LLM can update the JSON to add or remove things as needed
-maybe separate class for consumables (potions etc), weapons (dmg etc), and for misc/others - so that use item can specify if with mechanics or just text?
"""

import json
import ollama



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


# def load_inventory(file_path):
#     with open(file_path, 'r') as file:
#         data = json.load(file)
#     return data['inventory']


def load_inventory(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
     # Properly extracting item names using list comprehension
    item_names = [item['name'] for item in data['player_inventory']['items']]
    return item_names


def open_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def save_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)


# checks if the item the player want to use is in the inventory and return TRUE or FALSE 
def check_consumed(player_action, inventory_items):
    system_prompt = f"Is the item in the player action consumed, broken or dropped after the action? answer YES or NO. and what item in CAPS. why?"
    user_prompt = f"Player action: {player_action}"
    item_consumed = system_prompt_function(system_prompt, user_prompt)
    input(item_consumed)
    if "YES" in item_consumed:
        input(f"debugg- LLM thinks the item is consmed/dropped/not in inventory after {player_action}")
        return item_consumed
    elif "NO" in item_consumed:
        input(f"Item is not consumed/is still in player inventory after {player_action} - debugg")
        return False



# checks if the item the player want to use is in the inventory and return TRUE or FALSE 
def check_inventory(player_action, inventory_items):
    system_prompt = f"is the item refered to in the player action in the current inventory(of things they own or wear):{inventory_items}? answer YES or NO, why? EXAMPLE: Player action: i take of my armor. ['Sword', 'Health Potion', 'Leather Armor'] YES. LEATHER ARMOR. because take of my armor referes to leather armor in the inventory "
    user_prompt = f"Player action: {player_action}"
    item_exists = system_prompt_function(system_prompt, user_prompt)
    input(item_exists)
    if "YES" in item_exists:
        input(f"debugg- LLM thinks the item for {player_action} exists in inventory")
        return True
    elif "NO" in item_exists:
        input(f"it appears you cant do following action {player_action} with regards to your current inventory")
        return False




def remove_from_inventory(player_action, llm_output):
    inventory_file = 'inventory_test.json'
     
    system_prompt = f"inventory JSON to match the action, DO NOT WRITE 'here is the description:', ONLY ANSWER with the updated JSON."
    user_prompt = f"Player action: {player_action}, what what item to remove from JSON: {llm_output}"
    modified_inventory = system_prompt_function(system_prompt, user_prompt)
    # Save the new room state to the associated text file
    save_file(inventory_file, modified_inventory)


inventory_file = 'inventory_test.json'
inventory_items = load_inventory(inventory_file)
print(inventory_items)
player_action = input("what would you like to do?")
if check_inventory(player_action, inventory_items):
    item_consumed = check_consumed(player_action, inventory_items)
    if item_consumed:
        # update inventory JSON
        remove_from_inventory(player_action, item_consumed)
        # give lore txt