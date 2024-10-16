import json
import os


# Load dungeon JSON from a file
with open('dungeon.json', 'r') as dungeon_file:
    dungeon = json.load(dungeon_file)
    
# Directory where you want to save the item JSON files
output_directory = "room_items"

# Create directory for room items if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Loop through each room and create a JSON file for the items
for room in dungeon['rooms']:
    # Extract room name or room_id to name the file
    room_id = room['room_id']
    
    # Define the file name and path
    item_file_name = f"room_{room_id}_items.json"
    item_file_path = os.path.join(output_directory, item_file_name)
    
    # Extract items
    room_items = room.get('items', [])
    
    # Save items as a JSON file
    with open(item_file_path, 'w') as item_file:
        json.dump(room_items, item_file, indent=4)
    
    # Update the original dungeon room to include the path to the items file
    room['items_file'] = item_file_path
    
    # Remove the inline items array from the room
    del room['items']

# Save the modified dungeon JSON
with open('updated_dungeon.json', 'w') as dungeon_file:
    json.dump(dungeon, dungeon_file, indent=4)

print("Room item files and updated dungeon JSON have been saved.")