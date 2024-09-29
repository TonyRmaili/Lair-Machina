import ollama
from functions import all_functions



class OllamaToolCall:
    def __init__(self,messages):

        self.model = 'llama3.1'
        self.messages =  [{"role": "user", "content": messages}]

        # self.tools = [
        #     {
        #         'type':'function',
        #         'function':{
        #             'name':'addition',
        #             'description':'adds numbers',
        #             'parameters':
        #               {
        #                 'type':'object',
        #                 'properties':{
        #                     'a':{'type':'int'},
        #                     'b':{'type':'int'}
                            
        #                 }
        #             },
        #             'required':['a','b']                             
        #         }

        #     },

        #     {
        #         'type':'function',
        #         'function':{
        #             'name':'subtraction',
        #             'description':'subtracts numbers',
        #             'parameters':
        #               {
        #                 'type':'object',
        #                 'properties':{
        #                     'a':{'type':'int'},
        #                     'b':{'type':'int'}
                            
        #                 }
        #             },
        #             'required':['a','b']
        #         }
        #     },
        # ]

        self.tools = [
            {
                'type':'function',
                'function':{
                    'name':'get_skill_mod',
                    'description':'fetches the skill modifier: THE ONLY Available skills are stealth, medicine',
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
                'type':'function',
                'function':{
                    'name':'roll_dice',
                    'description':'Roll the dice and adds a bonus integer to the roll. the integer CAN be negative or zero',
                    'parameters':
                      {
                        'type':'object',
                        'properties':{
                            'prof':{'type':'int'}
                           
                            
                        }
                    },
                    'required':['prof']
                }
            },
            {
                'type':'function',
                'function':{
                    'name':'no_function',
                    'description':'Calls this function when no other function call fits the description',
                    
                }
            },
        ]
    
    def call_functions(self):
        
        resp = ollama.chat(
            model=self.model,
            messages=self.messages,
            tools=self.tools

        )
        return resp['message']['tool_calls']


    def activate_functions(self):
        call = self.call_functions()

        for tool in call:
            name = tool['function']['name']
            args = tool['function']['arguments']

            if name in all_functions:
                print(f'function {name} with args {args}')
                print(all_functions[name](**args))

        
           

if __name__ == '__main__':

    functions = OllamaToolCall(messages='activate all functions')
    functions.activate_functions()