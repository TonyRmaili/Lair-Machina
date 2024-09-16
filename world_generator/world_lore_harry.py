import ollama


def categorize(input_text):
    response = ollama.chat(model="llama3", messages=[{"role": "user", "content": input_text}])
    return response['message']['content']


# system_prompt = "You are a helpful assistant that explains complex topics in simple terms."
# user_prompt = "Can you explain quantum physics to a beginner?"

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
    
    
    game_story = (text_to_dm(f"write a short overview of a setting, story and world on the theme of {x}"))    


    system_prompt = "categorize following text into a JSON object with all the important information about locations and characters. ANSWER ONLY IN JSON FORMAT"
    user_prompt = game_story



    print(text_to_dm(f"write a short intro to a text based adventure ont he theme of {x}"))
    input("Press Enter to continue...")
    response = system_prompt_function(system_prompt, user_prompt)
    print(response)
    input("Press Enter to continue...")
    
    format_instruction = "JSON"
    prompt = f"categorize following text into a JSON object with all the important information about locations and characters: {game_story}"

    response = formatted_response_function(format_instruction, prompt)
    print(response)
    input("Press Enter to continue...")
# response = ollama.chat(model="llama3", messages=[
#                                                  {"role": "user",
#                                                 "content": "What is the capital of France?"}
#                                                  ])
# print(response['message']['content'])
