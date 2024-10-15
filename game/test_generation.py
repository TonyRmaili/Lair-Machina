

import sys

sys.path.append('../world_generator/')  # Adjust the path
from define_world import generate_dungeon_blueprint
from generate_world import GenerateWorld


# make instans
world=GenerateWorld() 

# debug
print(world.dungeon_data['map'])

# run generation from instans
world.run_dungeon()

