# it works to -
# 1 - add things to the room X (# fix som add thing to room - both adds to room and removes from inventory X)
# 2 - remove things from the room X (# fix so stealing things removes from room and adds to inventory ?  X)
# 3 - toll skillchecks X


# --- next step ---

# ---> make some sort of update description for item? > maybe same as add? but with new description?
# put in the room/action flavor text
# add combat call ?
# add move? -or better hardcoded?
# 






# EXTRA FUNCTIONS - not needed anymore??



# Function to ADD an item to the room JSON
# def add_item_to_room(item_name: str, item_description: str, room_json, file_path: str):
def add_item_to_room(item_name: str, item_description: str):

    # NEEDS TO BE DYNAMIC FOR THE ROOM WE ARE IN - SEND IN AS A ARG?
    room_file='room_json.json'    
    # Load room from file
    with open(room_file, 'r') as file:
        room_json = json.load(file)

    updated_items = []


    for item in room_json['items']:
        updated_items.append(item)  # Keep the item if it doesn't match

        
    # Create a new item dictionary
    new_item = {
        "name": item_name,
        "description": item_description,
        "properties": {
            "interact": True,
            "examine": True
        }
    }
    # Add the new item to the room's items list
    updated_items.append(new_item)

    #change the json to updated 
    room_json['items'] = updated_items
    
    # Save the updated room JSON back to the file
    with open(room_file, 'w') as file:
        json.dump(room_json, file, indent=4)
        
    return f"{item_name} has been added to the room."



# WORKS_ but is it needed?
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



# add to the rest if turns out is still usfull. for now just makes the LLM confused
all_functions = {
    

    'remove_item_from_room': remove_item_from_room,
    'add_item_to_room': add_item_to_room,
}




# ############################TO add in function calls if want to use above ########################3
            {
                'type': 'function',
                'function': {
                    'name': 'remove_item_from_room',
                    'description': 'Removes an item from the room (WITHOUT putting in the players inventory) based on the players action, use it if the player burns, or some how removes something',
                    'parameters': {
                        'type': 'object',
                        'properties': {
                            'item_name': {'type': 'string'}
                        }
                    },
                    'required': ['item_name']
                }
            },
            {
                'type': 'function',
                'function': {
                    'name': 'add_item_to_room',
                    'description': 'Adds an item to the room based on the players action, use it if the player wants to leave something in the room',
                    'parameters': {
                        'type': 'object',
                        'properties': {
                            'item_name': {'type': 'string'},
                            'item_description': {'type': 'string'}
                        }
                    },
                    'required': ['item_name', 'item_description']
                }
            },
