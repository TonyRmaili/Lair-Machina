import sys
import ollama
from function_calls.functions_for_ollama_state import all_functions
import json

# Function to load the room JSON from a file
def load_room_from_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

class OllamaToolCallState:
    def __init__(self, messages):
        # Set model and format
        self.model = 'llama3.1'
        self.messages = [{"role": "user", "content": messages}]

        # # Load the room JSON from the file
        # self.room_json = load_room_from_file(room_file)
        # self.inventory_json = load_room_from_file(inventory_file)

        # Define the tools available
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "update_item_description",
                    "description": "Updates the description of a item to reflect the new state after the event.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "item_name": {
                                "type": "string",
                                "description": "The name of the item to update"
                            },
                            "new_item_description": {
                                "type": "string",
                                "description": "A new description for the item (e.g., 'A chair that is now broken and unusable')."
                            },
                            "event": {
                                "type": "string",
                                "description": "The event that caused the item change (e.g., 'the chair got smashed by a giant')."
                            },
                            "room_file": {
                                "type": "string",
                                "description": "The file path to the JSON file that contains the room's items."
                            },
                            "inventory_file": {
                                "type": "string",
                                "description": "The file path to the JSON file that contains the inventory's items."
                            }
                        },
                        "required": ["item_name", "new_item_description", "event", "room_file", "inventory_file"]
                    }
                }
            }
            ]
            # {
            #     "type": "function",
            #     "function": {
            #         "name": "update_inventory_item",
            #         "description": "Replaces an item in the inventory with a new version. Removes the old item and inserts the updated item to reflect the new state after the event.",
            #         "parameters": {
            #             "type": "object",
            #             "properties": {
            #                 "old_item_name": {
            #                     "type": "string",
            #                     "description": "The name of the item to remove from the inventory (e.g., 'Shield')."
            #                 },
            #                 "new_item_name": {
            #                     "type": "string",
            #                     "description": "The name of the new item to add to the inventory (e.g., 'Broken Shield')."
            #                 },
            #                 "new_item_description": {
            #                     "type": "string",
            #                     "description": "A description of the new item to add (e.g., 'A shield that is now melted and unusable')."
            #                 },
            #                 "event": {
            #                     "type": "string",
            #                     "description": "The event that caused the item change (e.g., 'the shield got melted by dragon fire')."
            #                 },
            #                 "inventory_file": {
            #                     "type": "string",
            #                     "description": "The file path to the JSON file that contains the inventory's items."
            #                 }
            #             },
            #             "required": ["old_item_name", "new_item_name", "new_item_description", "event", "inventory_file"]
            #         }
            #     }
            # }, 
            # {
            #     "type": "function",
            #     "function": {
            #         "name": "update_que",
            #         "description": "Replaces an item in the inventory with a new version. Removes the old item and inserts the updated item to reflect the new state after the event.",
            #         "parameters": {
            #             "type": "object",
            #             "properties": {
            #                 "old_item_name": {
            #                     "type": "string",
            #                     "description": "The name of the item to remove from the inventory (e.g., 'Shield')."
            #                 },
            #                 "new_item_name": {
            #                     "type": "string",
            #                     "description": "The name of the new item to add to the inventory (e.g., 'Broken Shield')."
            #                 },
            #                 "new_item_description": {
            #                     "type": "string",
            #                     "description": "A description of the new item to add (e.g., 'A shield that is now melted and unusable')."
            #                 },
            #                 "event": {
            #                     "type": "string",
            #                     "description": "The event that caused the item change (e.g., 'the shield got melted by dragon fire')."
            #                 },
            #                 "inventory_file": {
            #                     "type": "string",
            #                     "description": "The file path to the JSON file that contains the inventory's items."
            #                 }
            #             },
            #             "required": ["old_item_name", "new_item_name", "new_item_description", "event", "inventory_file"]
            #         }
            #     }
            # }


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

