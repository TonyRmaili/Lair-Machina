# import ollama
# import json
# import pyttsx3


# class ToolCall:
#     def __init__(self, messages):
#         self.model = 'llama3.1'
#         self.messages = [{"role": "user", "content": messages}]

#         self.tools = [
#            {
#                 "type": "function",
#                 "function": {
#                     "name": 'look_at_room',
#                     "description": 'Provides a description of the room and its contents. Use when the player asks to look around.',
#                     "parameters": {
#                         "type": "object",
#                         "properties": {
#                             "current_room_description": {"type": "string", "description": "The description of the current room."},
#                             "room_file": {"type": "string", "description": "The file path to the JSON file that contains the room's items."}
#                         },
#                         "required": ["current_room_description", "room_file"]
#                     }
#                 }
#             },
#            {
#                 "type": "function",
#                 "function": {
#                     "name": 'add',
#                     "description": 'adds two numbers',
#                     "parameters": {
#                         "type": "object",
#                         "properties": {
#                             "a": {"type": "int", "description": "first number."},
#                             "b": {"type": "int", "description": "second number."}
#                         },
#                         "required": ["a", "b"]
#                     }
#                 }
#             }
#         ]

#     def call_functions(self):
#         # Get the tool calls from the model’s response
#         response = ollama.chat(
#             model=self.model,
#             messages=self.messages,
#             tools=self.tools
#         )
#         return response.get('message', {}).get('tool_calls', [])

#     def activate_functions(self):
#         tool_calls = self.call_functions()
#         # Execute each tool call based on the function name
#         for tool in tool_calls:
#             name = tool['function']['name']
#             args = tool['function']['arguments']
#             print(f'function name {name}')
#             print(f'function args {args}')
#             if name in all_functions:
#                 print(f'Calling function {name} with args {args}')
#                 # Call the function with the room JSON context
#                 result = all_functions[name](**args)
#                 print(result)
#                 return result



# def look_at_room(current_room_description, room_file):
#     #make dynamic  - like = current location instead
#     room_file=room_file    
#     # Load room from file
#     with open(room_file, 'r') as file:
#         room_json = json.load(file)
    
#     # make description of the room for the player
#     system_prompt = f"The player is in a room with following items: {room_json}. and following room description: {current_room_description}. Describe what the player sees when they look around as if you were a dungeon master based on the info you have about the room"
#     user_prompt = "Player action: I look around, what do I see?"
    
    
#     # Interacting with the LLaMA 3 model, with a system-level instruction
#     response = ollama.chat(
#         model="llama3.1", 
#         messages=[
#             {"role": "system", "content": system_prompt},
#             {"role": "user", "content": user_prompt}
#         ]
#     )

#     room_intro = response['message']['content']
#     return room_intro


# def add(a,b):
#     return a+b

# all_functions = {
#     'look_around': look_at_room,
#     'add':add
# }

# if __name__=='__main__':
    
#     engine = pyttsx3.init()
#     engine.say('hello')
#     engine.runAndWait()

    
