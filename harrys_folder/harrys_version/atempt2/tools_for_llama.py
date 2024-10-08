import ollama
from functions_for_llama import all_functions
import json

# Function to load the room JSON from a file - not part of the LLM-class
def load_room_from_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)




class OllamaToolCall:
    def __init__(self,messages, room_file):

        #set model and format 
        self.model = 'llama3.1'
        self.messages =  [{"role": "user", "content": messages}]

        # Load the room JSON from the file
        self.room_json = load_room_from_file(room_file)


        #define the tool - so far - skillcheckroll and remove item from room JSON 
        self.tools = [
            {
                'type':'function',
                'function':{
                    'name':'roll_skill_with_mod',
                    'description':'Rolls for using a skill and displayes result: THE ONLY Available skills are acrobatics, animal handling, arcana, athletics, deception, history, insight, intimidation, investigation, medicine, nature, perception, performance, persuasion, religion, sleight of hand, stealth, survival',
                    'parameters':
                      {
                        'type':'object',
                        'properties':{
                            'skill':{'type':'str'}
                           
                            
                        }
                    },
                    'required':['skill']
                }
            },
            {
                'type': 'function',
                'function': {
                    'name': 'loot_item_from_room',
                    'description': 'Removes an item from the room and adds it to the players inventory based on the players action, use it if the player wants to take something in the room',
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
                    'name': 'leave_item_from_inventory_in_room',
                    'description': 'Removes an item from the player inventory and adds it to the room JSON based on the players action, use it if the player wants to leave something from their inventory in the room',
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
                    'name': 'look_at_room',
                    'description': 'gives a description of the room',
                    'parameters': {
                        'type': 'object',
                        'properties': {
                            'current_location': {'type': 'string'}
                        }
                    },
                    'required': ['current_location']
                }
            },                                           {
                'type': 'function',
                'function': {
                    'name': 'ask_stuff',
                    'description': 'gives the in lore answer about things, use when the player makes a question about the world',
                    'parameters': {
                        'type': 'object',
                        'properties': {
                            'player_question': {'type': 'string'}
                        }
                    },
                    'required': ['player_question']
                }
            }
        ]
    
    # this is what the LLM will use to see all the functions it has
    def call_functions(self):
        
        resp = ollama.chat(
            model=self.model,
            messages=self.messages,
            tools=self.tools

        )
        return resp['message']['tool_calls']

    # this is what the LLM will use to activate the function it wants to use
    # Get the function calls from the model's response
    def activate_functions(self):
        call = self.call_functions()

        # Execute each tool call based on the function name
        for tool in call:
            name = tool['function']['name']
            args = tool['function']['arguments']

            if name in all_functions:
                print(f'function {name} with args {args}')
                # Call the function with the room JSON context ### add room_json=self.room_json
                print(all_functions[name](**args))
           

if __name__ == '__main__':
        

    # Load room data from file and use it in the game
    # functions = OllamaToolCall(messages='I steal the bookshelf', room_file='room_json.json')
    # functions.activate_functions()

    testing = input("what would you like to do")
    functions = OllamaToolCall(messages=testing, room_file='room_json.json')
    functions.activate_functions()



# # Example file path for the room JSON
# room_file = 'room_json.json'

# # Load the room JSON from the file
# with open(room_file, 'r') as file:
#     room_json = json.load(file)

# # Add an item to the room
# result = add_item_to_room('Lantern', 'A bright lantern with a flickering flame.', room_json, room_file)
# print(result)  # Output: "Lantern has been added to the room."



    # # works sort of!
    # functions = OllamaToolCall(messages='I try to tell the dragon to stand back')
    
    # functions.activate_functions()