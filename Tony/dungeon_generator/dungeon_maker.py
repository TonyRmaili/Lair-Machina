import ollama
import os
import json
import sys


dungeon_blueprint = {
'system':'''You are an expert Dungeon Master tasked with creating a fully realized dungeon for a Dungeons and Dragons-style adventure.
The dungeon should be generated with a specific theme that fits the tone of the game. You will determine the number of rooms and how they are connected.

Please use the following template to generate the first steps into making the whole dungeon. DO NOT generate any rooms until asked so:

{
  "dungeon_name": "string",
  "dungeon_description": "string",
  "dungeon_lore: "string",
  "room_amount: "int"  # between 3 to 7 rooms ONLY
Respond using JSON.'''
}

dungeon_room = {
'prompt':'''Generate a room based on the theme and description. Please use the following template to generate the room. Make sure to generate more than 1 item.

{
    "room_id": "int",
    "room_description: "string",
    "room_passages": "string",
    "room_coordinates_x: "int", 
    "room_coordinates_y: "int" 
    "items": [
        {
         "item_name":"string",
         "item_description": "string"
        }
    ]

}
Respond using JSON.
'''
}



def fix_json_string(json_string):
    try:
        json_data = json.loads(json_string)
        # Optional: Pretty print or format the JSON if needed
        formatted_json = json.dumps(json_data, indent=4)

        return formatted_json
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None


def save_context(context):
    current_dir = os.path.dirname(__file__) 
    context_file_path = os.path.join(current_dir, 'context.json') 
    with open(context_file_path, 'w') as json_file:
        json.dump(context, json_file, indent=4)


def save_text_to_json(json_data,file_path):
    with open(file_path, "w") as file:
        file.write(json_data)

def save_json(json_data,file_path):
    with open(file_path,'w') as f:
        json.dump(json_data,f,indent=4)

def load_json(file_path):
    with open(file_path,'r') as f:
        data = json.load(f)
    return data



def dungeon_generate():

    data = load_json(file_path='dungeon.json')

    resp = ollama.chat(
        model='llama3.1',
        messages=[
            {'role':'system','content':'''You are an expert Dungeon Master tasked with creating a fully realized dungeon for a Dungeons and Dragons-style adventure. Respond using JSON'''},
            {'role':'user','content':'make a dungeon with a theme and a description'},
            {'role':'assistant','content':f'{data}'},
            {'role':'user','content':'update the dungeon with traps'}
                ],
        format='json'

    )

    content = resp['message']['content']

    save_text_to_json(json_data=content,file_path='dungeon.json')
    


if __name__=='__main__':
    resp = dungeon_generate()

    # data = load_json('dungeon.json')
    # save_json(json_data=data,file_path='dungeon.json')
   
