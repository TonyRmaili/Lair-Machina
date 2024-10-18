import ollama
from function_calls.functions_for_ollama_v2 import all_functions
import json

# Function to load the room JSON from a file
def load_room_from_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)
    

class OllamaToolCall:
    def __init__(self, messages, room_file):
        # Set model and format
        self.model = 'llama3.1'
        self.messages = [{"role": "user", "content": messages}]

        
        # Load the room JSON from the file
        self.room_json = load_room_from_file(room_file)
        # self.context_path_save= context_path_save
    
        # Define the tools available
        self.tools = [
            {
                'type': 'function',
                'function': {
                    'name': 'resolve_hard_action',
                    'description': 'Rolls for using a skill and displays the result. use if player types TRY in caps Available skills: acrobatics, animal handling, arcana, athletics, deception, history, insight, intimidation, investigation, medicine, nature, perception, performance, persuasion, religion, sleight of hand, stealth, survival.',
                    'parameters': {
                        'type': 'object',
                        'properties': {
                            "skill": {"type": "string", "description": "The name of the skill to use."},
                            "dc": {"type": "int", "description": "The difficulty level of the task (between 10-20)."},
                            "player_action": {"type": "string", "description": "The action the player is attempting."}
                        },
                        'required': ['skill', 'dc', 'player_action']
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "loot_item_from_room",
                    "description": "Removes an item from the room and adds it to the player's inventory. use if player types LOOT in caps",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "item_name": {"type": "string", "description": "The name of the item the player wants to loot."},
                            "room_file": {"type": "string", "description": "The file path to the JSON file that contains the room's inventory."}                           
                        },
                        "required": ["item_name", "room_file"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": 'leave_drop_throw_item',
                    "description": 'Removes an item from the player’s inventory and adds it to the room JSON. Use if the player writes DROP in caps.',
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "item_name": {"type": "string", "description": "The name of the item the player wants to leave. The item needs to exist in the player’s current inventory."},
                            "room_file": {"type": "string", "description": "The file path to the JSON file that contains the room's inventory."},
                            "player_action": {"type": "string", "description": "The action the player is attempting."}
                            
                        },
                        "required": ["item_name", "room_file", "player_action"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": 'look_at_room',
                    "description": 'Provides a description of the room and its contents. Use when the player asks to look around or types LOOK in caps.',
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "current_room_description": {"type": "string", "description": "The description of the current room."},
                            "room_file": {"type": "string", "description": "The file path to the JSON file that contains the room's items."}
                        },
                        "required": ["current_room_description", "room_file"]
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

# if __name__ == '__main__':
    
    # load_room_from_file(game/room_items/room_1_items.json')
    # Ask for player input
    # player_input = input("What would you like to do? ")
    # # Create an instance of OllamaToolCall with the player's input and room JSON file
    # functions = OllamaToolCall(messages=player_input, room_file='../game/room_items/room_1_items.json')
    # # Activate the functions based on the player's input
    # functions.activate_functions()