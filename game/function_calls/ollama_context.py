import ollama
import json
import os
import time
import threading
import sys




"""
-generate - kan ta kontext och output text
-chat - kan använda tools

-båda kan köra json_format men

---order of operations---

1. player enters prompt > "I would like to throw my sword at the wall"
2. tool call - > check vilken action to do - typ leave/drop item
3. generate -> skriv en update på room state? - och en output text? "the sword flys out and sticks to the wall"




"""


class OllamaWithContext:
    def __init__(self,path):
        self.model = 'llama3.1'
        self.path = path

    def generate_context(self, prompt, system):
        # dungeon_path + context.json
        context_file_path = self.path+'context.json'
        if os.path.exists(context_file_path):
            try:
                # Try to load the JSON file
                with open(context_file_path, 'r') as file:
                    context = json.load(file)
            except json.JSONDecodeError:
                # If file is empty or invalid, assign an empty list
                context = []
        else:
            # If the file doesn't exist, assign an empty list
            context = []

        
        resp = ollama.generate(
            model=self.model,
            prompt=prompt,
            system=system,
            context=context,
            
        )

        # return LLM text response
        text = resp['response']

        # save context from latest output message
        context = resp['context']
        with open(context_file_path, 'w') as json_file:
            json.dump(context, json_file, indent=4)

        return text



if __name__=='__main__':
    prompt = 'Who are we?'

    with_context = OllamaWithContext()

    context,text = with_context.generate_context(prompt=prompt)
    # print(text)

