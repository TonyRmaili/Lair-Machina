import json


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


def save_to_json(data,file_name):

    with open(file_name, 'w') as f:
        json.dump(data,f,indent=4)


if __name__=='__main__':
    file = 'world_blueprint.json'
    save_to_json(data,file)