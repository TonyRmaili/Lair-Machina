import json

def remove_item_from_room(item_name: str):

    room_file='room_json.json'    
    # Load room from file
    with open(room_file, 'r') as file:
        room_json = json.load(file)

    
    item_found = False

    print(room_json)
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


item_name = input("test to remove item")
remove_item_from_room(item_name)
room_file='room_json.json'    
# Load room from file
with open(room_file, 'r') as file:
    room_json = json.load(file)

print(room_json)