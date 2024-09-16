import ollama

import json



# Function to handle LLM updates to room state --- not working as Llama3 is not great att categorizing JSON from text -- need to change approach

# def categorize(input_text):
#     response = ollama.chat(model="llama3", messages=[{"role": "user", "content": input_text}])
#     return response['message']['content']



test_room ="""{
  "room": {
    "name": "Living Room",
    "description": "A cozy living room with soft lighting, a fireplace in the corner, and a large window overlooking the garden. There are a few pieces of furniture neatly arranged.",
    "dimensions": {
      "length": "5 meters",
      "width": "4 meters"
    },
    "items": [
      {
        "name": "Lamp",
        "description": "A standing floor lamp with a dimmable light bulb. The lamp gives off a warm, ambient glow.",
        "location": "Next to the sofa, by the wall.",
        "weight": "4 kg",
        "status": "Functional"
      },
      {
        "name": "Book",
        "description": "A hardcover novel titled 'The Great Adventure.' The pages are slightly worn, suggesting it has been read multiple times.",
        "location": "On the coffee table, near the center.",
        "weight": "0.5 kg",
        "status": "Slightly worn"
      },
      {
        "name": "Coffee Table",
        "description": "A wooden coffee table with a smooth surface and sturdy legs. It has a small drawer on one side.",
        "location": "In the center of the room.",
        "weight": "15 kg",
        "status": "Functional",
        "items_on_table": [
          {
            "name": "Remote Control",
            "description": "A remote control for the television. It has several buttons for different settings.",
            "location": "On top of the coffee table.",
            "weight": "0.2 kg",
            "status": "Functional"
          },
          {
            "name": "Mug",
            "description": "A ceramic mug with a crack along the handle. It has a few coffee stains inside.",
            "location": "On the left side of the coffee table.",
            "weight": "0.3 kg",
            "status": "Broken"
          }
        ]
      }
    ]
  }
}"""

# example of a input text function

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

# example of a formatted response function - that takes instruction and prompt 

def formatted_response_function(format_instruction, prompt):
    response = ollama.chat(
        model="llama3", 
        messages=[
            {"role": "system", "content": f"Respond in the following format: {format_instruction}."},
            {"role": "user", "content": prompt}
        ]
    )
    return response['message']['content']



def text_to_dm(prompt):
    response = ollama.chat(model="llama3", messages=[
                                                 {"role": "user",
                                                "content": prompt}
                                                 ])
    return response['message']['content']



if __name__ == "__main__":
    print("""
        **********************************************
        *                                            *
        *    Welcome to Lair Machina                 *
        *                                            *
        *                                            *
        *                                            *
        *                                            *
        *                                            *
        *     Please pick a theme for the adventure  *
        *                                            *
        *                                            *
        *                                            *
        **********************************************
          """)
    x = input("Enter your choice and press enter: ")
    print(f"Your choice is {x}")
    input("Press Enter to continue...")
    
    
    # get a short overview of the game story - sort of works
    game_story = (text_to_dm(f"write a short overview of a setting, story and world on the theme of {x}"))    
    print(game_story)



    #sort of works, but is it good enough to be used in the game. may need to change approach? 
    system_prompt = "categorize following text into a JSON object with all the important information about locations and characters. ANSWER ONLY IN JSON FORMAT"
    user_prompt = game_story
    input("Press Enter to continue...")
    # test catergorize to JSON - sort of works
    response = system_prompt_function(system_prompt, user_prompt)
    print(response)
    input("Press Enter to continue...")
    

    # works worse or better than the above ?? more testing needed
    # format_instruction = "JSON"
    # prompt = f"categorize following text into a JSON object with all the important information about locations and characters: {game_story}"

    # response = formatted_response_function(format_instruction, prompt)
    # print(response)
    # input("Press Enter to continue...")



    # test the room state - works for "look around" - not sure how to handle other actions though
    playerinput=input("what do you wish to do?")

    # maybe change the JSON to have very destinct categories ?
    system_prompt = f"You are a DM for a text-based adventure game. this is the current room the player is in: {test_room}."
    user_prompt = f"this is the players request: '{playerinput}'"
    response = system_prompt_function(system_prompt, user_prompt)
    print(response)
    input("Press Enter to continue...")

    # Here I would need to update the JSON object based on the response from the Llama3 model - test more to see if it works
    playerinput = input("what do you wish to do? - action")
    user_prompt = f"this is the players request: '{playerinput}'"
    response = system_prompt_function(system_prompt, user_prompt)
    print(response)
    input("Press Enter to continue...")
    exit()
    #based on the response > change the JSON object to reflect the changes   
    # response = system_prompt_function(system_prompt, user_prompt)




# ###################################### test JSON change in room state - not working as Llama3 is not returning valid JSON ########################################
# import json

# # Initial room setup in JSON
# test_room = {
#     "room": {
#         "name": "Living Room",
#         "description": "A cozy living room with soft lighting, a fireplace in the corner, and a large window overlooking the garden. There are a few pieces of furniture neatly arranged.",
#         "dimensions": {
#             "length": "5 meters",
#             "width": "4 meters"
#         },
#         "items": [
#             {
#                 "name": "Lamp",
#                 "description": "A standing floor lamp with a dimmable light bulb. The lamp gives off a warm, ambient glow.",
#                 "location": "Next to the sofa, by the wall.",
#                 "weight": "4 kg",
#                 "status": "Functional"
#             },
#             {
#                 "name": "Book",
#                 "description": "A hardcover novel titled 'The Great Adventure.' The pages are slightly worn, suggesting it has been read multiple times.",
#                 "location": "On the coffee table, near the center.",
#                 "weight": "0.5 kg",
#                 "status": "Slightly worn"
#             },
#             {
#                 "name": "Coffee Table",
#                 "description": "A wooden coffee table with a smooth surface and sturdy legs. It has a small drawer on one side.",
#                 "location": "In the center of the room.",
#                 "weight": "15 kg",
#                 "status": "Functional",
#                 "items_on_table": [
#                     {
#                         "name": "Remote Control",
#                         "description": "A remote control for the television. It has several buttons for different settings.",
#                         "location": "On top of the coffee table.",
#                         "weight": "0.2 kg",
#                         "status": "Functional"
#                     },
#                     {
#                         "name": "Mug",
#                         "description": "A ceramic mug with a crack along the handle. It has a few coffee stains inside.",
#                         "location": "On the left side of the coffee table.",
#                         "weight": "0.3 kg",
#                         "status": "Broken"
#                     }
#                 ]
#             }
#         ]
#     }
# }

# # Function to handle LLM updates to room state
# def llm_update_room_state(system_prompt, user_prompt):
#     response = ollama.chat(
#         model="llama3",
#         messages=[
#             {"role": "system", "content": system_prompt},
#             {"role": "user", "content": user_prompt}
#         ]
#     )
#     return response['message']['content']

# # Function to ensure the LLM returns only valid JSON
# def parse_llm_response(response):
#     try:
#         # Try to parse the LLM response as JSON
#         updated_room = json.loads(response)
#         return updated_room
#     except json.JSONDecodeError:
#         print("Error: LLM did not return valid JSON.")
#         return None

# # Starting the game
# player_input = input("What do you wish to do? ")

# # Initial system prompt: describe the room and instruct the LLM to only return valid JSON
# system_prompt = (
#     f"You are the game engine for a text-based adventure game. The game environment is represented by JSON. "
#     f"Here is the current state of the room in JSON format: {json.dumps(test_room)}. "
#     f"Based on the player's request, update the JSON to reflect any changes. "
#     f"ONLY respond with valid JSON. Do NOT include explanations, text, or anything else. "
#     f"The updated JSON should reflect any changes based on the player's input."
# )
# user_prompt = f"The player has requested the following action: '{player_input}'"

# # Get the updated room state from the LLM
# response = llm_update_room_state(system_prompt, user_prompt)

# input(response)
# # Try to parse the LLM's response as JSON
# updated_room = parse_llm_response(response)

# # Check if the response was valid JSON, otherwise keep the original room state
# if updated_room:
#     test_room = updated_room
# else:
#     print("Room state could not be updated.")

# # Display the updated room state in the game
# print("Updated room state after player action:")
# print(json.dumps(test_room, indent=2))

# # Handle further actions
# player_input = input("What do you wish to do next? ")

# # Update the system prompt with the current room state
# system_prompt = (
#     f"You are the game engine for a text-based adventure game. The game environment is represented by JSON. "
#     f"Here is the current state of the room in JSON format: {json.dumps(test_room)}. "
#     f"Based on the player's request, update the JSON to reflect any changes. "
#     f"ONLY respond with valid JSON. Do NOT include explanations, text, or anything else. "
#     f"The updated JSON should reflect any changes based on the player's input."
# )
# user_prompt = f"The player has requested the following action: '{player_input}'"

# # Get the next updated room state from the LLM
# response = llm_update_room_state(system_prompt, user_prompt)

# # Parse the next LLM response as JSON
# updated_room = parse_llm_response(response)

# # Update room state if valid JSON is returned
# if updated_room:
#     test_room = updated_room

# # Print the final room state
# print("Final room state after the next action:")
# print(json.dumps(test_room, indent=2))