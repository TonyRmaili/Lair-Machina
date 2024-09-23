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
        self.blue_print_path= 'world_blueprint.json'
        self.model = 'llama3.1'

        with open(self.blue_print_path,'r') as f:
            self.data = json.load(f)


        self.system = self.data['system']
        
        self.world_data = self.data.copy()
        del self.world_data['system']



    def lore(self):
        resp = ollama.generate(
            system=self.system,
            model=self.model,
            prompt=self.data['lore']
            
        )

        context = resp['context']
        text = resp['response']

        self.save_context(context,'lore')
        self.save_text(text=text,name='lore')


        return resp['response']
    

    def run(self):
        for key,value in self.world_data.items():
            if os.path.exists('context.json'):
                try:
                    # Try to load the JSON file
                    with open('context.json', 'r') as file:
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
                context=context

            )
            text = resp['response']
            context = resp['context']

            self.save_context(context=context)
            self.save_text(text=text,name=key)
        

    def save_context(self,context):
        file_name = 'context.json'
        with open(file_name, 'w') as json_file:
            json.dump(context, json_file, indent=4)

    def save_text(self,text,name):
        file_name = './texts/' + name + '.txt'

        with open(file_name,'w') as f:
            f.write(text)



if __name__=='__main__':
    world = GenerateWorld()
    start_time = time.time()


    world.run()


    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Script runtime: {execution_time} seconds")