import sys
import ollama
from function_calls.functions_for_ollama_v2 import all_functions
import json

# Function to load the room JSON from a file
def load_room_from_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

class OllamaToolCallState:
    def __init__(self, messages, room_file, inventory_file):
        # Set model and format
        self.model = 'llama3.1'
        self.messages = [{"role": "user", "content": messages}]

        # Load the room JSON from the file
        self.room_json = load_room_from_file(room_file)
        self.inventory_json = load_room_from_file(inventory_file)

        # Define the tools available
        self.tools = [
           {
                "type": "function",
                "function": {
                    "name": "update_player_hp",
                    "description": "Updates the player's HP. Use to add or subtract health points based on player actions or damage taken.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "player_hp_path": {"type": "string", "description": "The JSON path to the player's HP value in the room JSON."},
                            "hp_change": {"type": "int", "description": "The amount to add or subtract from the player's HP. Use negative values to decrease HP."},
                            "reason": {"type": "string", "description": "The reason for the HP change (e.g., taking damage or healing)."}
                        },
                        "required": ["player_hp_path", "hp_change", "reason"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "update_room_item",
                    "description": "Replaces an item in the room with a new version. Removes the old item and inserts the updated item to reflect the new state after the event.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "old_item_name": {
                                "type": "string",
                                "description": "The name of the item to remove from the room (e.g., 'Chair')."
                            },
                            "new_item_name": {
                                "type": "string",
                                "description": "The name of the new item to add to the room (e.g., 'Broken Chair')."
                            },
                            "new_item_description": {
                                "type": "string",
                                "description": "A description of the new item to add (e.g., 'A chair that is now broken and unusable')."
                            },
                            "event": {
                                "type": "string",
                                "description": "The event that caused the item change (e.g., 'the chair got smashed by a giant')."
                            },
                            "room_file": {
                                "type": "string",
                                "description": "The file path to the JSON file that contains the room's items."
                            }
                        },
                        "required": ["old_item_name", "new_item_name", "new_item_description", "event", "room_file"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "update_inventory_item",
                    "description": "Replaces an item in the inventory with a new version. Removes the old item and inserts the updated item to reflect the new state after the event.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "old_item_name": {
                                "type": "string",
                                "description": "The name of the item to remove from the inventory (e.g., 'Shield')."
                            },
                            "new_item_name": {
                                "type": "string",
                                "description": "The name of the new item to add to the inventory (e.g., 'Broken Shield')."
                            },
                            "new_item_description": {
                                "type": "string",
                                "description": "A description of the new item to add (e.g., 'A shield that is now melted and unusable')."
                            },
                            "event": {
                                "type": "string",
                                "description": "The event that caused the item change (e.g., 'the shield got melted by dragon fire')."
                            },
                            "inventory_file": {
                                "type": "string",
                                "description": "The file path to the JSON file that contains the inventory's items."
                            }
                        },
                        "required": ["old_item_name", "new_item_name", "new_item_description", "event", "inventory_file"]
                    }
                }
            },
            
            # to do - add more functions here
            # update room description=
            # add event to logg? - like a short summary of what happened? > try to add RAG and context also?
            # add item to room pre function - like a is the player trying to loot or leave something?
            # 
            # a function that makes a list of function calls?
            
            
            
            #1 - player writes prompt
            # 2 > decide what type of action the player is trying to do - > loot / drop / > other
            ## 2.1 if loot > decide if just take item or if need to roll/cant take it? > make short flavor description + add to inventory/remove from room
            ## 2.2 if drop > decide if just drop or if other thing happens? > make short flavor description + add to room/remove from inventory
            # 3.3 if other > decide if roll - do roll - make short flavor description > resolve effect > (add to logg?)
            ## effects = update items, room, hp, add items, remove items, add to logg - could be several things so need to chain effects- first try this effect solver see limits?
            
            #testa: - kan den klara att kolla på en action/outcome-  
             
             
            {
                "type": "function",
                "function": {
                    "name": "update_que",
                    "description": "Replaces an item in the inventory with a new version. Removes the old item and inserts the updated item to reflect the new state after the event.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "old_item_name": {
                                "type": "string",
                                "description": "The name of the item to remove from the inventory (e.g., 'Shield')."
                            },
                            "new_item_name": {
                                "type": "string",
                                "description": "The name of the new item to add to the inventory (e.g., 'Broken Shield')."
                            },
                            "new_item_description": {
                                "type": "string",
                                "description": "A description of the new item to add (e.g., 'A shield that is now melted and unusable')."
                            },
                            "event": {
                                "type": "string",
                                "description": "The event that caused the item change (e.g., 'the shield got melted by dragon fire')."
                            },
                            "inventory_file": {
                                "type": "string",
                                "description": "The file path to the JSON file that contains the inventory's items."
                            }
                        },
                        "required": ["old_item_name", "new_item_name", "new_item_description", "event", "inventory_file"]
                    }
                }
            }
            ]


    def call_functions(self):
        # Get the tool calls from the model’s response
        response = ollama.chat(
            model=self.model,
            messages=self.messages,
            tools=self.tools
        )
        return response.get('message', {}).get('tool_calls', [])

    def activate_functions(self):
        tool_calls = self.call_functions()

        # Execute each tool call based on the function name
        for tool in tool_calls:
            name = tool['function']['name']
            args = tool['function']['arguments']

            if name in all_functions:
                print(f'Calling function {name} with args {args}')
                # Call the function with the room JSON context
                result = all_functions[name](**args)
                print(result)
                return result

