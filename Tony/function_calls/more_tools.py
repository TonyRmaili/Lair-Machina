import ollama
from random import randint

def roll_dice(dice_size):
    roll = randint(1,dice_size)
    return roll


class TestTools:
    def __init__(self):
        self.model = 'llama3.1'

        self.messages = [
            {
                "role": "system",
                "content": "You are a dice roller expert. All you do is roll dice of differant sizes. You have access to all standard dice"
            },
            {
                "role":"user", "content":"roll a dice of your choosing"
            },
            {
                "role": "assistant",
                "tool_calls": [
                {
                    "type": "function",
                    "function": {
                    "name": "roll_dice",
                    "arguments": {
                        "dice_size": 8
                        
                    }
                    }
                }
                ]
            },
            {
                "role": "tool",
                "content": "4"
            },
            {
            "role": "assistant",
            "content": "dice size = 8 and the roll was 4"
            },
            {
            "role": "user",
            "content": "roll again ONLY 4 TIMES"
            }
        ]

        self.tools = [
              {
                'type':'function',
                'function':{
                    'name':'roll_dice',
                    'description':'rolls a dice of the AI;s choosing',
                    'parameters':
                      {
                        'type':'object',
                        'properties':{
                            'dice_size':{'type':'int'}
                           
                            
                        }
                    },
                    'required':['dice_size']
                }
            },
            
        ]

    def task(self):

        resp = ollama.chat(
            model=self.model,
            messages=self.messages,
            tools=self.tools

        )

        return resp['message']['tool_calls']

if __name__ == '__main__':
    tool = TestTools()
    resp = tool.task()
    print(resp)