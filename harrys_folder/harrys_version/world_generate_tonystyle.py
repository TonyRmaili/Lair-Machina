import ollama
import json
import os
import time

'''
order to pass in data

lore > pantheon > world_structure > factions > settlements > npcs > landspaces  

'''


class GenerateWorld:
    def __init__(self):
        # uses prompt from json
        self.blue_print_path= 'world_blueprint_tonystyle.json'
        self.model = 'llama3.1'

        with open(self.blue_print_path,'r') as f:
            self.data = json.load(f)


        self.system = self.data['system']
        
        self.world_data = self.data.copy()
        del self.world_data['system']



    def run(self):
        for key,value in self.world_data.items():
            # THIS IS THE MAGIC?
            # context here is a JSON but will include numbers, is it like a vector?
            if os.path.exists('testcontext.json'):
                try:
                    # Try to load the JSON file
                    with open('testcontext.json', 'r') as file:
                        context = json.load(file)
                except json.JSONDecodeError:
                    # If file is empty or invalid, assign an empty list
                    context = []
            else:
                # If the file doesn't exist, assign an empty list
                context = []
            resp = ollama.generate(
                system=self.system,
                model=self.model,
                prompt=value,
                # gets used here when generating
                context=context

            )
            text = resp['response']
            context = resp['context']

            self.save_context(context=context)
            self.save_text(text=text,name=key)
        

    def room(self):
        with open('room_blueprint_tonystyle.json','r') as f:
            data = json.load(f)
        

        system = data['system']

        resp = ollama.generate(
            model=self.model,
            system=system,
            prompt='Make a small room with fantasy rpg style. Have various objects in the room so that the players can interact or inspect them.',
            format='json'
        )
        
        resp = resp['response']

        resp = self.fix_json_string(json_string=resp)

        with open("room.json", "w") as file:
            file.write(resp)

    def fix_json_string(self,json_string):
        try:
            json_data = json.loads(json_string)
            
            # Optional: Pretty print or format the JSON if needed
            formatted_json = json.dumps(json_data, indent=4)
            
            return formatted_json
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return None


    def save_context(self,context):
        file_name = 'testcontext.json'
        with open(file_name, 'w') as json_file:
            json.dump(context, json_file, indent=4)

    def save_text(self,text,name):
        file_name = './worldtext/' + name + '.txt'

        with open(file_name,'w') as f:
            f.write(text)



if __name__=='__main__':
    world = GenerateWorld()
    start_time = time.time()


    world.run()
    # world.room()


    end_time = time.time()
    execution_time = end_time - start_time