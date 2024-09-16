import ollama
import json
import os
from system_prompt import fantasy_setting, small_prompt


class WorldGenerator:
    def __init__(self):
        self.model = 'llama3.1'
        

    def generate_world(self,prompt):
        response = ollama.generate(
            model=self.model,
            prompt=prompt
        )
        self.save_full_response(response=response)

        context = response['context']
        self.save_context(context=context)

        lore = response['response']
        self.save_lore(text=lore)


    def save_full_response(self,response):
        file_name = 'world.json'

        with open(file_name, 'w') as json_file:
            json.dump(response, json_file, indent=4)
    
    def save_context(self,context):
        file_name = 'context.json'
        with open(file_name, 'w') as json_file:
            json.dump(context, json_file, indent=4)
    
    def save_lore(self,text):
        file_name= 'world_lore.txt'
        with open(file_name, "w") as file:
            file.write(text)


    def try_context(self,prompt):
        file_name = 'context.json'
        with open(file_name,'r') as file:
            context = json.load(file)
        
        response = ollama.generate(
            model=self.model,
            prompt=prompt,
            context=context,
            
        )
        return response['response']

if __name__=='__main__':

    world_gen = WorldGenerator()
    # world_gen.generate_world(fantasy_setting)
    resp = world_gen.try_context(
        prompt='are blueberries ever mentioned in the original lore?'
    )

    print(resp)