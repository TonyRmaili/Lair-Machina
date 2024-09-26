import ollama



def chat(question):
    messages = [{"role": "user", "content": question}]
    resp = ollama.chat(
        model='llama3.1',
        messages=messages,
        tools=[
            {
                'type':'function',
                'function':{
                    'name':'addition',
                    'description':'adds numbers',
                    'parameters':
                      {
                        'type':'object',
                        'properties':{
                            'a':{'type':'int'},
                            'b':{'type':'int'}
                            
                        }
                    },
                    'required':['a','b']
                    
                    
                }

            },

            {
                'type':'function',
                'function':{
                    'name':'subtraction',
                    'description':'subtracts two numbers',
                    
                }
            }
        ]
    )

    return resp

if __name__ == '__main__':

    resp = chat('activate the add function. all args > 20. and i want to subtract aswell')
    

    for tool in resp['message']['tool_calls']:
        print(tool['function']['name'])
    

    