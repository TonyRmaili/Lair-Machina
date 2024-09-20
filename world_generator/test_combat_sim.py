


from TTS.api import TTS

# Initialize the model
tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC")

# # Convert text to speech and save it to a file
# tts.tts_to_file(text="Hello, welcome to TTS!", file_path="output.wav")




import ollama






def system_prompt_function(system_prompt, user_prompt):
    # Interacting with the LLaMA 3 model, with a system-level instruction
    response = ollama.chat(
        model="llama3", 
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    return response['message']['content']


import random

# Dice rolling function
def roll_dice(number_of_dice, die_size):
    return sum(random.randint(1, die_size) for _ in range(number_of_dice))




# Initiative calculation
def calculate_initiative(entity_name, initiative_modifier):
    roll = roll_dice(1, 20)
    return {"name": entity_name, "initiative": roll + initiative_modifier}



# Player and monster JSON-like objects
player = {
    "name": "Aric, the Ranger",
    "initiative_modifier": 4,
    "hit_points": {"current": 38, "maximum": 38},
    "armor_class": 16
}

monster = {
    "name": "Troll",
    "initiative_modifier": 1,
    "hit_points": {"current": 84, "maximum": 84},
    "armor_class": 15
}


current_location = {
    "name": "Cavern",
    "description": "A dark cavern with damp walls and a foul smell."
}

    # Start of combat description
start_description = system_prompt_function(
        "Describe the beginning of a fantasy combat encounter SHORT ANSWER, DO NOT DESCRIBE ANY ATTACKS, ROLLS OR NUMBERS . example: The Ogre roars, its eyes locking onto you with predatory intent. You grip your weapon as the tension thickens. Roll for initiative as the fight begins. example: The Bugbear glares at you with a primal fury, its muscles tensing as it prepares to strike. You feel your heart race, but your grip tightens on your weapon. The air grows heavy as the battle is about to begin. Roll for initiative!",
        f"The combat begins between {player['name']} and {monster['name']} in {current_location['name']}: {current_location['description']}."
    )

# # # Convert text to speech and save it to a file
tts.tts_to_file(text=start_description, file_path="output2.wav")



from pydub import AudioSegment

# Load audio and adjust speed
audio = AudioSegment.from_file("output2.wav")
faster_audio = audio.speedup(playback_speed=1.25)

# Export faster audio
faster_audio.export("output_fast1.wav", format="wav")

import pygame
import time

# Initialize pygame mixer
pygame.mixer.init()

# Load and play background music (loop indefinitely)
pygame.mixer.music.load('C:/Users/harry/Documents/Lair-Machina/world_generator/The_journey(2).mp3')
pygame.mixer.music.play(1)  # -1 means the music will loop indefinitely

# Load and play the .wav file
output_file = "./output_fast1.wav"
voice_over = pygame.mixer.Sound(output_file)
voice_over.play()


pygame.mixer.music.set_volume(0.3)  # Set background music volume (0.0 to 1.0)
voice_over.set_volume(0.8)  # Set sound effect volume (0.0 to 1.0)


# Get the duration of the voiceover
voiceover_length = voice_over.get_length()

# Wait for the voiceover to finish playing
time.sleep(voiceover_length)  # Sleep for the duration of the voiceover

# Stop the background music once the voiceover finishes
pygame.mixer.music.stop()

# Wait for the audio to finish playing
while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)

# print it out
input(start_description + "(press enter to roll initiative)")





# Example: Roll 1d20 for initiative
# initiative_roll = roll_dice(1, 20)
# input(f"Rolled initiative: {initiative_roll}")


# Roll initiative for both player and monster
player_initiative = calculate_initiative(player["name"], player["initiative_modifier"])
monster_initiative = calculate_initiative(monster["name"], monster["initiative_modifier"])

# Store both in a list
combatants = [player_initiative, monster_initiative]

# Sort combatants by initiative rolls in descending order
combatants.sort(key=lambda x: x["initiative"], reverse=True)

# Display turn order
print("Turn Order:")
for combatant in combatants:
    print(f"{combatant['name']} - Initiative: {combatant['initiative']}")
input("Press enter to begin combat!")


# Function to handle an attack action
def attack(attacker, defender):
    print(f"{attacker['name']} is attacking {defender['name']}!")
    
    # Roll to hit
    attack_roll = roll_dice(1, 20) + attacker['attack_bonus']
    print(f"{attacker['name']} rolls a {attack_roll} to hit!")
    
    if attack_roll >= defender['armor_class']:
        # Successful hit, roll for damage *attacker = * is used to unpack the tuple into arguments - roll_dice(1, 8) for longbow damage as an example
        damage = roll_dice(*attacker['damage']['formula'])
        defender['hit_points']['current'] -= damage
        print(f"Hit! {attacker['name']} deals {damage} {attacker['damage']['type']} damage to {defender['name']}.")
            # Start of combat description
        attack_description = system_prompt_function(
            "Describe this happening SHORT ANSWER, DO NOT DESCRIBE ANY ATTACKS, ROLLS OR NUMBERS . example: You draw your bow and aim for the dragons neck. The dragonscale are thick but the arrow manages to pierce through and the dragon roars in pain as a steam of thick blood starts to stream down. example: The Bugbear is much too slow and as you strike out with your sword you manage to cut a deep gash into its side. The Bugbear howls in pain and anger as it prepares to retaliate.",
            f"Hit! {attacker['name']} deals {damage} {attacker['damage']['type']} damage to {defender['name']}.")
            # # Convert text to speech and save it to a file
        tts.tts_to_file(text=attack_description, file_path="output3.wav")



        from pydub import AudioSegment

        # Load audio and adjust speed
        audio = AudioSegment.from_file("output3.wav")
        faster_audio = audio.speedup(playback_speed=1.25)

        # Export faster audio
        faster_audio.export("output_fast3.wav", format="wav")

        import pygame

        # Initialize pygame mixer
        pygame.mixer.init()

        # Load and play background music (loop indefinitely)
        pygame.mixer.music.load('C:/Users/harry/Documents/Lair-Machina/world_generator/The_journey(2).mp3')
        pygame.mixer.music.play(1)  # -1 means the music will loop indefinitely
        # to play the music only once 

        # Load and play the .wav file
        output_file = "./output_fast3.wav"
        voice_over = pygame.mixer.Sound(output_file)
        voice_over.play()


        pygame.mixer.music.set_volume(0.3)  # Set background music volume (0.0 to 1.0)
        voice_over.set_volume(0.8)  # Set sound effect volume (0.0 to 1.0)

        # Get the duration of the voiceover
        voiceover_length = voice_over.get_length()

        # Wait for the voiceover to finish playing
        time.sleep(voiceover_length)  # Sleep for the duration of the voiceover

        # Stop the background music once the voiceover finishes
        pygame.mixer.music.stop()

        # Wait for the audio to finish playing
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    else:
        print(f"{attacker['name']} misses!")

# Function to handle the Dodge action (disadvantage on attacks against the dodger)
def dodge(player):
    print(f"{player['name']} takes the Dodge action!")
    # This would impose disadvantage on attacks against the player until next turn
    player['is_dodging'] = True

# Function to handle the use of an item (example: healing potion)
def use_item(player):
    healing = roll_dice(2, 4) + 2  # 2d4+2 healing potion
    player['hit_points']['current'] = min(player['hit_points']['current'] + healing, player['hit_points']['maximum'])
    print(f"{player['name']} uses a healing potion and regains {healing} HP!")

# Combat loop with options for player actions
def combat(player, monster):
    # Roll initiative for both
    player_initiative = calculate_initiative(player["name"], player["initiative_modifier"])
    monster_initiative = calculate_initiative(monster["name"], monster["initiative_modifier"])

    # Sort combatants by initiative
    combatants = sorted([player_initiative, monster_initiative], key=lambda x: x["initiative"], reverse=True)

    # Combat loop
    turn = 1
    while player['hit_points']['current'] > 0 and monster['hit_points']['current'] > 0:
        print(f"\n-- Turn {turn} --")
        
        for combatant in combatants:
            # If the player is acting
            if combatant['name'] == player['name'] and player['hit_points']['current'] > 0:
                print("It's your turn!")
                print("Choose an action:")
                print("1. Attack")
                print("2. Dodge")
                print("3. Use Item (Healing Potion)")
                
                action = input("Enter the number of the action you wish to take: ")
                
                if action == "1":
                    attack(player, monster)
                elif action == "2":
                    dodge(player)
                elif action == "3":
                    use_item(player)
                else:
                    print("Invalid action, turn skipped.")
                
                # Reset dodging status at the end of the player's turn
                player['is_dodging'] = False

            # If the monster is acting
            elif combatant['name'] == monster['name'] and monster['hit_points']['current'] > 0:
                # Monster attacks normally, but check if the player is dodging
                if player.get('is_dodging', False):
                    print(f"The {monster['name']} attacks with disadvantage because {player['name']} is dodging!")
                    # Roll twice and take the lower roll
                    attack_roll_1 = roll_dice(1, 20) + monster['attack_bonus']
                    attack_roll_2 = roll_dice(1, 20) + monster['attack_bonus']
                    attack_roll = min(attack_roll_1, attack_roll_2)
                    print(f"{monster['name']} rolls a {attack_roll} to hit!")
                else:
                    attack(monster, player)

            # Check if someone has dropped to 0 HP
            if player['hit_points']['current'] <= 0:
                print(f"{player['name']} has fallen! {monster['name']} wins!")
                return
            elif monster['hit_points']['current'] <= 0:
                print(f"{monster['name']} has fallen! {player['name']} wins!")
                return

        turn += 1



# Player and monster stats (simplified JSON-like)
player = {
    "name": "Aric, the Ranger",
    "initiative_modifier": 4,
    "hit_points": {"current": 38, "maximum": 38},
    "armor_class": 16,
    "attack_bonus": 7,
    "damage": {
        "type": "piercing",
        "formula": (1, 8),  # 1d8 for longbow damage
    }
}

monster = {
    "name": "Cave Troll",
    "initiative_modifier": 1,
    "hit_points": {"current": 84, "maximum": 84},
    "armor_class": 15,
    "attack_bonus": 6,
    "damage": {
        "type": "slashing",
        "formula": (2, 6),  # 2d6 for claw damage
    }
}

# Start combat
combat(player, monster)