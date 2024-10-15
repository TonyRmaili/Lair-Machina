import json
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from world_generator.grid_maker import run_dungeon_maker,print_dungeon_map,room_data_to_text,generate_room_data


dungeon_template = ''' 
Generate the dungeon using this template. Respond using JSON:
{
    "theme": str,  # The specific and creative theme of the dungeon, such as "Ancient Ruins," "Frozen Crypt," or "Volcanic Fortress."
    "description": str  # A vivid, atmospheric description of the entire dungeon. Focus on the architecture, lighting, sounds, scents, and overall mood. Make it engaging and full of immersive details that draw players into the environment.
}
'''

dungeon_system = '''
You are an expert Dungeon Master tasked with creating a fully realized dungeon for a Dungeons and Dragons-style adventure. 

Your task is to generate a dungeon using the provided template. This dungeon should have a creative and engaging theme that fits into a fantasy game world. Follow these detailed instructions:

1. **Dungeon Theme**: Choose a fitting and unique theme for the dungeon that is captivating, such as "Ancient Ruins," "Cursed Castle," "Sunken Temple," or "Mystical Forest.". The theme should evoke a strong atmosphere.

2. **Dungeon Description**: Provide a vivid, atmospheric description of the dungeon that sets the tone for the adventure. Describe the architecture, lighting, and overall mood. You may include:
   - Key environmental details (e.g., moss-covered stone walls, flickering torchlight, strange symbols etched into the floor)
   - Sounds and smells that heighten the immersion (e.g., dripping water, distant echoes, damp, musty air)
   - The mood or atmosphere (e.g., eerie, ominous, foreboding, mysterious)
   - Unique features of the dungeon (e.g., "The walls hum faintly with an ancient magic" or "A cold, unnatural breeze flows through the corridors")
   
3. **Consistency**: Ensure that the theme and description match each other. The description should reflect the chosen theme in every detail.

### Key Rules:
- Be creative and avoid clichés.
- **Do NOT** include generic phrases like "you have reached the end of the dungeon" or "Here is your dungeon."
- **Stick strictly** to the JSON template format.
- Include only the requested information, nothing more.

Respond using JSON format only.
'''

room_template = '''Generate the room using this template. Respond using JSON:
        {
        'description': str,  # Detailed room description
        'name': str # Room name derived from the description
        'items': [
            {
                'name': str,  # Name of the item, e.g., "Ancient Sword"
                'description': str  # Description of the item, e.g., "A rusty sword that hums with ancient magic."
            }
        ],
        'properties': list,  # List of unique properties of the room, e.g., ['dark', 'trapped']
        'secrets': str  # Description of any hidden elements, e.g., "A hidden trapdoor beneath the carpet"
        }'''

room_system = '''
You are an expert Dungeon Master tasked with creating individual rooms for a fully realized dungeon in a Dungeons and Dragons-style adventure. Each room should be engaging, atmospheric, and fit seamlessly within the dungeon's theme.
You will be provided a template for room generation. Follow this detailed process to create each room:
1. **Room Description**: Provide a vivid and immersive description of the room. Describe key environmental features such as the room’s architecture, lighting, and notable characteristics (e.g., stone walls covered in ancient moss, flickering torchlight casting ominous shadows, a damp, musty odor filling the space). The description should create a clear visual and sensory experience. Ensure the description fits with the overall theme of the dungeon.
2. **Room Name**: Generate a fitting name for the room that matches its description. The name should evoke the room’s purpose or atmosphere (e.g., "Hall of Echoes," "Forgotten Armory," "The Sealed Chamber").
3. **Items**: Add at least one interesting item found in the room. The items should be unique and engaging. Describe the item's appearance and any notable magical or historical properties (e.g., "Ancient Sword," with the description "A rusty sword that hums with faint magical energy, its blade etched with runes of a forgotten era"). Make sure the items are appropriate to the dungeon’s theme.
4. **Room Properties**: List any unique properties of the room (e.g., "dark," "trapped," "cold"). These properties should enhance the room's atmosphere and provide gameplay elements for the players to interact with.
5. **Secrets**: If the room contains any hidden elements or secrets, describe them (e.g., "A hidden trapdoor beneath the carpet leads to a secret chamber"). Secrets should be intriguing and fit naturally into the room’s design, offering players something to discover.

### Key Rules:
- Be as creative as possible with the descriptions, and avoid generic or cliché descriptions.
- Ensure all room elements align with the overall theme and atmosphere of the dungeon.
- **Do NOT** include generic phrases or descriptions that break immersion, such as "Here is your room."
- Stick strictly to the JSON template format.
- Respond with only the information requested and in the proper structure.
Respond using JSON.'''


# old prompts
readable_data = {
    'system': '''You are an advanced AI responsible for constructing a rich, detailed, and cohesive high-fantasy world.
                Your role is to be the architect, generating lore, characters, settings, and other world elements while maintaining consistency and depth.
                Focus on epic themes, conflicts, and relationships that drive the stories and quests within this universe.
                Magic, divine influence, and ancient power should be central forces in the world, and your creations must reflect the complexity of such a setting.
                Only generate what is specifically requested. You will receive prompts for categories such as lore, settlements, landscapes, NPCs, factions, and pantheon.''',
    
    'lore': '''Generate a complex, multi-layered history that spans centuries, detailing significant wars, alliances, and discoveries.
               Include legends, ancient prophecies, and long-forgotten empires that still have an influence on the present.
               Highlight key conflicts between civilizations, the rise and fall of kingdoms, and pivotal moments that have shaped the world as it stands today.
               Consider the roles of magic, technology, and cosmic forces in shaping the world's history and timeline.''',
    
    'npcs': '''Create a diverse group of non-playable characters, each with a unique backstory, motivations, and connections to the world.
               Include a wide range of characters, from powerful rulers and enigmatic wizards to ordinary citizens and mysterious travelers.
               For each NPC, describe their personality, goals, affiliations, and how they might assist or oppose the players.
               Include details about their appearance, mannerisms, and any secrets they may hold. 
               Ensure each NPC has a well-defined arc that ties into the world’s broader events or personal ambitions.''',
    
    'world_structure': '''Develop a diverse world setting that includes multiple continents, regions, and ecosystems.
                  Describe the cultural, political, and social structures that govern each region, including major factions, religious orders, guilds, and secret societies.
                  Provide details on the economic systems, trade routes, and conflicts between different nations.
                  Explain the roles of magic, religion, and ancient technologies in everyday life.
                  The setting should be dynamic and capable of growth, exploration, and change over time.''',
    
    'settlements': '''Design a variety of settlements, from grand capital cities to hidden villages deep within enchanted forests.
                      For each settlement, describe its architectural style, layout, and key locations such as marketplaces, temples, and fortresses.
                      Highlight unique features or landmarks, such as floating islands or underground tunnels.
                      Detail the ruling body or leadership, the culture of the inhabitants, and the settlement's primary economic activities.
                      Consider the historical significance or ongoing conflicts connected to each settlement.''',
    
    'landscapes': '''Generate descriptions of varied landscapes, from towering mountain ranges and sprawling deserts to magical forests and eerie wastelands.
                     Each landscape should have distinct geographical features, climate, and ecosystem.
                     Include unique natural phenomena such as enchanted rivers, cursed swamps, or volcanoes that serve as magical conduits.
                     The landscapes should play a role in the world’s history and lore, influencing the behavior of its inhabitants, the spread of civilizations, and the flow of resources.''',
    
    'pantheon': '''Create a pantheon of deities and divine entities, each with their own domains, symbols, and personalities.
                  Describe their relationships with one another, their roles in the world’s creation, and how they interact with mortals.
                  Include gods and goddesses governing various aspects such as war, knowledge, love, and death.
                  Detail their followers, religious practices, and how the worship of these deities shapes cultures across the world.
                  Consider the existence of lesser spirits, demigods, or ancient forgotten gods, and how they fit into the cosmology.''',
    
    'factions': '''Describe the key organizations, guilds, or secret societies that influence political and social life in the world.
                   Provide details on their goals, leadership, alliances, and conflicts.
                   Consider how these factions interact with major events, settlements, and power structures in the world.'''
}

data = {
    'system': '''You are an advanced AI responsible for constructing a rich, detailed, and cohesive high-fantasy world. Your role is to be the architect, generating lore, characters, settings, and other world elements while maintaining consistency and depth. Focus on epic themes, conflicts, and relationships that drive the stories and quests within this universe. Magic, divine influence, and ancient power should be central forces, and your creations must reflect the complexity of such a setting. Only generate what is specifically requested. You will receive prompts for categories such as lore, settlements, landscapes, NPCs, factions, and pantheon.''',
    
    'lore': '''Generate a complex, multi-layered history that spans centuries, detailing significant wars, alliances, and discoveries. Include legends, ancient prophecies, and long-forgotten empires that still influence the present. Highlight key conflicts between civilizations, the rise and fall of kingdoms, and pivotal moments shaping the world as it stands. Consider the roles of magic, technology, and cosmic forces in shaping the world's history.''',
    'pantheon': '''Create a pantheon of deities and divine entities, each with their own domains, symbols, and personalities. Describe their relationships, roles in the world’s creation, and interactions with mortals. Include gods governing aspects such as war, knowledge, love, and death. Detail their followers, religious practices, and how their worship shapes cultures. Consider lesser spirits, demigods, or forgotten gods, and their place in the cosmology.''',
    'world_structure': '''Develop a diverse world setting that includes multiple continents, regions, and ecosystems. Describe the cultural, political, and social structures governing each region, including factions, religious orders, guilds, and secret societies. Provide details on economic systems, trade routes, and conflicts between nations. Explain the roles of magic, religion, and ancient technologies in daily life. The setting should be dynamic and capable of growth, exploration, and change.''',
    'factions': '''Describe the key organizations, guilds, or secret societies influencing political and social life. Provide details on their goals, leadership, alliances, and conflicts. Consider how these factions interact with major events, settlements, and power structures.''',
    'settlements': '''Design a variety of settlements, from grand capital cities to hidden villages in enchanted forests. For each settlement, describe its architectural style, layout, and key locations like marketplaces, temples, and fortresses. Highlight unique features such as floating islands or underground tunnels. Detail the ruling body, culture, and primary economic activities. Consider the historical significance or ongoing conflicts tied to each settlement.''',
    'npcs': '''Create a diverse group of non-playable characters, each with a unique backstory, motivations, and connections to the world. Include a wide range of characters, from rulers and wizards to ordinary citizens and travelers. For each NPC, describe their personality, goals, affiliations, and how they might assist or oppose players. Include details about their appearance, mannerisms, and secrets. Ensure each NPC has a well-defined arc tied to broader events or ambitions.''',
    'landscapes': '''Generate descriptions of varied landscapes, from towering mountains and sprawling deserts to magical forests and eerie wastelands. Each landscape should have distinct geographical features, climate, and ecosystem. Include unique phenomena such as enchanted rivers, cursed swamps, or magical volcanoes. The landscapes should influence the world's history, civilizations, and resources.''', 
}

room ={"system": '''
You are tasked with generating a detailed room based on the user's description. 
Your response must fill in the following JSON fields: description, items, properties, and dimensions. 
Ensure the room includes at least one door and one window. Any additional elements you generate must also be in JSON format.

Follow this example structure:
{
    "description": "",
    "items": {},
    "properties": {},
    "dimensions": {}
}

Respond using JSON.
'''}



def generate_dungeon_blueprint(dungeon_system=dungeon_system,
                               dungeon_template=dungeon_template,
                               room_system=room_system,
                               room_template=room_template,
                               rows=4,cols=4,room_ratio=0.3):

    dungeon_map,room_count,room_data = run_dungeon_maker(rows=rows,cols=cols,room_ratio=room_ratio)
    # room_data = room_data_to_text(room_data=room_data)
    room_data = generate_room_data(dungeon_map=dungeon_map)

    data = {
        'map':dungeon_map,
        'room_count':room_count,
        'room_data':room_data,
        'room_system':room_system,
        'room_template':room_template,
        'system':dungeon_system,
        'template':dungeon_template
    }

    return data




def save_blueprint_to_json(data, file_name):
    current_dir = os.path.dirname(__file__)  # Get the directory of the current file (world_gen)
    file_path = os.path.join(current_dir, file_name)  # Construct the full path within world_gen
    
    with open(file_path, 'w') as f:  # Use file_path instead of file_name
        json.dump(data, f, indent=4)

    return file_path  # Optional: return the file path for confirmation


if __name__=='__main__':
    # file = 'world_blueprint.json'
    # room_file = 'room_blueprint.json'
    # dungeon_file = 'dungeon_blueprint.json'
    

    # save_blueprint_to_json(dungeon_system,dungeon_file)

    generate_dungeon_blueprint()