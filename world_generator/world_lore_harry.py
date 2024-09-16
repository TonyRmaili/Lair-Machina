import ollama


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
    
    game_theme = x
    
    
    print(text_to_dm(f"write a sentence about {x}"))
    
    input("Press Enter to continue...")

# response = ollama.chat(model="llama3", messages=[
#                                                  {"role": "user",
#                                                 "content": "What is the capital of France?"}
#                                                  ])
# print(response['message']['content'])
