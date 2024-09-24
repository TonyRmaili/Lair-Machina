import ollama
import json
import os

system = '''"You are the Game Master in a Dungeons and Dragons-style adventure. Your role is to guide the player through the game world using only the data provided,
which includes lore, descriptions, items, characters, and other elements. 
Respond only to the player's actions, revealing or updating the world based on their decisions.
You must adhere strictly to the provided data and cannot create new elements unless instructed. 
Do not include unnecessary or conversational filler such as 'Sure!' or 'I will do that.
Stay focused on maintaining the immersion of the game world. Your responses should be concise, informative, and descriptive, avoiding redundant phrases or breaking the flow of the narrative.
Your goal is to maintain a continuous, immersive storytelling experience by reacting only to player input. Always stay in character as the Game Master, and provide only relevant information that moves the game forward."
'''


class Game:
    def __init__(self):
        with open('../world_generator/room.json', 'r') as f:
            self.room = json.load(f)
        
        self.system = system
        self.model = 'llama3.1'
    

    def initial_prompt(self):
        resp = ollama.generate(
            model=self.model,
            prompt=f'''The player enters a room with this description {game.room}. What does he see?''',
            system=system,
            )

        text = resp['response']
        context = resp['context']
        self.save_context(context=context)
        return text


    def talk(self,prompt):
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
            model=self.model,
            prompt=prompt,
            system=system,
            context=context,
            )
        
        text = resp['response']
        context = resp['context']
        self.save_context(context=context)
        return text


    def save_context(self,context):
        file_name = 'context.json'
        with open(file_name, 'w') as json_file:
            json.dump(context, json_file, indent=4)


    def run(self):
        print("Welcome to the Dungeons and Dragons Game Master. Type 'quit' to exit the game.")
        init_text = self.initial_prompt()
        print(init_text)
        while True:
            # Get player's input
            player_input = input("Enter your action: ")
            
            # If the player wants to quit
            if player_input.lower() == 'quit':
                print("Thank you for playing! Exiting the game.")
                break
            
            # Send the player's input to the Game Master (AI)
            response = self.talk(player_input)
            
            # Output the AI's response
            print(response)


if __name__=='__main__':
    game = Game()
    game.run()


    