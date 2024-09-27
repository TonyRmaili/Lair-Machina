# import json

# # The initial room setup
# room_json = {
#   "room": {
#     "name": "Living Room",
#     "description": "A cozy room with a fireplace and a bookshelf.",
#     "items": [
#       {"name": "book", "description": "A dusty old book on the shelf.", "location": "room"},
#       {"name": "key", "description": "A small rusty key lying on the table.", "location": "room"}
#     ]
#   },
#   "inventory": []
# }

# # Function to move item from room to inventory
# def move_item_to_inventory(item_name, room_file):
#     room_items = room_json['room']['items']
#     for item in room_items:
#         if item['name'].lower() == item_name.lower() and item['location'] == 'room':
#             # Move the item to the inventory
#             item['location'] = 'inventory'
#             room_json['inventory'].append(item)
#             room_json['room']['items'].remove(item)
#             return f"{item_name} has been moved to your inventory."
#     return f"{item_name} is not available in the room."

# # Example interaction:
# player_input = "Take the key"
# item_to_move = "key"  # The model can extract this from player_input
# result = move_item_to_inventory(item_to_move, room_json)

# # Output
# print(result)
# print(json.dumps(room_json, indent=2))