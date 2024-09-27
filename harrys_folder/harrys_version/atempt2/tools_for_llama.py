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
                    'name': 'remove_item_from_room',
                    'description': 'Removes an item from the room based on the player’s action, use it if the player takes something',
                    'parameters': {
                        'type': 'object',
                        'properties': {
                            'item_name': {'type': 'string'}
                        }
                    },
                    'required': ['item_name']
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
                # Call the function with the room JSON context
                print(all_functions[name](**args, room_json=self.room_json))
           

if __name__ == '__main__':
        

    # Load room data from file and use it in the game
    functions = OllamaToolCall(messages='I steal the old wooden desk', room_file='room_json.json')
    functions.activate_functions()





    # # works sort of!
    # functions = OllamaToolCall(messages='I try to tell the dragon to stand back')
    
    # functions.activate_functions()