"""
test for inventory - idea is that you have a txt file for inventory and for room states
-you can ask it to use a item from inventory - it will then decide if you have that item, if yes then it decides if the item is consumed/removed from inventory by doing this (if yes then it removes it) (OBS - need to implement so that it gets added to the room if dropped, also add lore description of the action, and the impact on the room/item)
-you can also ask it to take things from the room - it will first decide what you are trying to take and send that to next function - which then decide if the thing is in the room (looks at room desxription), if yes then it updates the room description to remove the item.

--still need to add the lore part so that it describes when you do the thing (take the books etc) - also need to update the room description if the player drops something--- maybe that is the same call- that always happens as long as it is a "Interact, action" and not ask/lore-


>>after that start working on rolls? + merge this with the dungeon map file- and lastly sort out the context generator thing so that it makes the whole castle in one go.

other idea for later? : -maybe separate class for consumables (potions etc), weapons (dmg etc), and for misc/others - so that use item can specify if with mechanics or just text?
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


def open_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def save_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)


# checks if the item the player want to use is in the inventory and return TRUE or FALSE 
def check_consumed(player_action, inventory_items):
    system_prompt = f"Is the item in the player action consumed, broken or dropped after the action? IF YES ANSWER ONLY WITH THE ITEM NAME IN CAPS, OTHERWISE ANSER NO. "
    user_prompt = f"Player action: {player_action}"
    item_consumed = system_prompt_function(system_prompt, user_prompt)
    input(item_consumed)
    if "NO" in item_consumed:
        input(f"Item is not consumed/is still in player inventory after {player_action} - debugg")
        return False
    else:
        input(f"debugg- LLM thinks the item is consmed/dropped/not in inventory after {player_action}")
        return item_consumed



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



def remove_from_inventory(player_action, item_name):
    file_path = 'inventory_test.txt'
    
    # Convert item_name to uppercase to match the LLM output if not already
    item_name_upper = item_name.upper()
    new_lines = []

    with open(file_path, 'r') as file:
        for line in file:
            print(line)
            if item_name_upper not in line.upper():  # Check if the line contains the item name in uppercase
                new_lines.append(line)  # Keep lines that do not contain the item name

    # Write the filtered lines back to the file
    with open(file_path, 'w') as file:
        file.writelines(new_lines)
    
    with open(file_path, 'r') as file:
        print(file)


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



# checks if the item the player want to take is in the room and return TRUE or FALSE 
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



def update_room_after_take(item_to_take, room_items):
    system_prompt = f"Update the following room description to NOT INCLUDE the item the player took, DO NOT WRITE 'here is the description:', ONLY ANSWER with the updated description of the room. room description: {room_items}"
    user_prompt = f"Item player took: {item_to_take}"
    modified_content = system_prompt_function(system_prompt, user_prompt)
    
    room_file = 'living_room_state.txt'
    # Save the new room state to the associated text file
    save_file(room_file, modified_content)
    
    print("\nUpdated room state:")
    print(modified_content)


# testrun-loads text
inventory_file = 'inventory_test.txt'
inventory_items=open_file(inventory_file)
# shows inventory text
print(inventory_items)



room_path = "living_room_state.txt"
current_room = open_file(room_path)

# test use item 
player_action = input("what would you like to do (use inventory item)?")
if check_inventory(player_action, inventory_items):
    item_consumed = check_consumed(player_action, inventory_items)
    if item_consumed:
        # update inventory
        remove_from_inventory(player_action, item_consumed)
        # give lore txt
        # update room state - is in the other file





print(current_room)

player_action = input("waht would you like to do ? - (take stuff)")
# add to inventory - needs to have similar LLM check if item is in the room
print(current_room)
item_to_add=check_room_items(player_action, current_room)
if item_to_add:
    add_to_inventory(item_to_add)
    # also needs to be removed from room
    update_room_after_take(item_to_add, current_room)


