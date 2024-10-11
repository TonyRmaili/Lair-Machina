import ollama
import json
import os
import time
import threading
import matplotlib.pyplot as plt
from define_world import generate_dungeon_blueprint

'''
order to pass in data

lore > pantheon > world_structure > factions > settlements > npcs > landspaces  

'''


# gå till comfy foldern. source comfyUIvenv/bin/activate
# kör python3 main.py

# steaming option for både text och tts generation?


class GenerateWorld:
    def __init__(self):
        # Save all generated files in the same folder as this script
        self.current_dir = os.path.dirname(__file__)  # Get the directory of the current file (world_gen)
        self.blue_print_path = os.path.join(self.current_dir, 'world_blueprint.json')  # Path to world blueprint
        self.model = 'llama3.1'
        
        # Load blueprint data
        with open(self.blue_print_path, 'r') as f:
            self.data = json.load(f)

        self.system = self.data['system']
        self.world_data = self.data.copy()
        del self.world_data['system']

        self.is_generating = False

        # dungeon maker

        self.dungeon_data = generate_dungeon_blueprint(rows=3,cols=2,room_ratio=0.5)


    def run_in_thread(self):
        # Run the text generation in a separate thread
        thread = threading.Thread(target=self.run)
        thread.start()

    def run(self):
        self.is_generating = True
        for key, value in self.world_data.items():
            context_file_path = os.path.join(self.current_dir, 'context.json')  # Ensure the context.json is in world_gen

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
                system=self.system,
                model=self.model,
                prompt=value,
                context=context
            )
            text = resp['response']
            context = resp['context']

            self.save_context(context=context)
            self.save_text(text=text, name=key)
        self.is_generating = False

    def room(self):
        room_blueprint_path = os.path.join(self.current_dir, 'room_blueprint.json')  # Ensure it reads from world_gen
        with open(room_blueprint_path, 'r') as f:
            data = json.load(f)

        system = data['system']

        resp = ollama.generate(
            model=self.model,
            system=system,
            prompt='Make a small room with fantasy RPG style. Have various objects in the room so that the players can interact or inspect them.',
            format='json'
        )

        resp = resp['response']
        resp = self.fix_json_string(json_string=resp)

        room_file_path = os.path.join(self.current_dir, "room.json")  # Save room.json in world_gen
        with open(room_file_path, "w") as file:
            file.write(resp)


    def dungeon_overview(self):
        resp = ollama.generate(
           model=self.model,
           system=self.dungeon_data['system'],
           prompt=self.dungeon_data['template'],
           format='json'
       )
        resp = resp['response']
        return resp

    def dungeon_rooms(self,theme,description):
        previous_rooms = []
        dungeon_theme = theme
        dungeon_description = description
        room_template = self.dungeon_data['room_template']
        room_system = self.dungeon_data['room_system']
        room_count = self.dungeon_data['room_count']
        room_data = self.dungeon_data['room_data']
        
        for i in range(room_count):
            count = i+1
            resp= ollama.generate(
                model=self.model,
                system=f'{room_system}.This is the dungeons theme {dungeon_theme} and the dungeons description {dungeon_description}',
                prompt=f'{room_template} and these are the previous rooms {previous_rooms}',
                format='json'
            )

            resp = resp['response']
            resp_dict = json.loads(resp)
            resp_dict['room_id'] = count
            resp_dict['coordinates'] = room_data[count]['coord']
            resp_dict['connections'] = room_data[count]['connections']

            previous_rooms.append(resp_dict)

        return previous_rooms

    def run_dungeon(self):
        self.is_generating = True
        overview_resp = self.dungeon_overview()
        overview_dict = json.loads(overview_resp)
        theme = overview_dict['theme']
        description = overview_dict['description']
        rooms = self.dungeon_rooms(theme=theme,description=description)

        overview_dict['rooms'] = rooms

        # self.save_to_json(resp=overview_dict,name='dungeon')
        with open('dungeon.json', 'w') as json_file:
            json.dump(overview_dict, json_file, indent=4)
        self.is_generating = False



 # old methods 
    def plot_dungeon(self):
        '''Deprecated'''
        rooms = self.extract_dungeon_coords()
        fig, ax = plt.subplots()

        # Plot each room
        for i, room in enumerate(rooms):
            x, y = room['coordinates']
            ax.plot(x, y, 'bo')  # plot the room as a blue dot
            ax.text(x, y, f'Room {i+1}', fontsize=9, ha='right')  # label the room

            # Plot passage connections (straight lines between rooms)
            if i > 0:
                prev_x, prev_y = rooms[i-1]['coordinates']
                ax.plot([prev_x, x], [prev_y, y], 'k-', lw=1)  # draw line between current and previous room

        # Setting up the plot limits and grid
        ax.set_xlim(-5, 5)
        ax.set_ylim(-5, 5)
        ax.grid(True)
        ax.set_title("Dungeon Map")

        plt.show()

    def fix_json_string(self, json_string):
        '''seems not to be needed'''
        try:
            json_data = json.loads(json_string)

            # Optional: Pretty print or format the JSON if needed
            formatted_json = json.dumps(json_data, indent=4)

            return formatted_json
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return None

    def save_to_json(self,resp,name):
        path = os.path.join(self.current_dir, name+".json")  
        with open(path, "w") as file:
            file.write(resp)

    def load_json(self,name):
        path = os.path.join(self.current_dir,name+".json")
        with open(path,'r') as file:
            data = json.load(file)
        return data

    def save_context(self, context):
        context_file_path = os.path.join(self.current_dir, 'context.json')  # Save context.json in world_gen
        with open(context_file_path, 'w') as json_file:
            json.dump(context, json_file, indent=4)

    def save_text(self, text, name):
        texts_dir = os.path.join(self.current_dir, 'texts')  # Create texts folder in world_gen

        # Ensure the texts directory exists
        os.makedirs(texts_dir, exist_ok=True)

        file_name = os.path.join(texts_dir, name + '.txt')  # Save the text file in the texts folder

        with open(file_name, 'w') as f:
            f.write(text)


if __name__=='__main__':
    world = GenerateWorld()
    start_time = time.time()


    # world.run()
    # world.room()
    # world.dungeon()

    # world.dungeon_overview()
    # world.dungeon_rooms()

    world.run_dungeon()



    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Script runtime: {execution_time} seconds")