import ollama 


"""
This is a basic example of using ollama
you can make functions to call the LLM like blow, with or without instructions. 
It is good to add examples if you are looking to make it give a specific format (just add the examples in the system prompt)

I think the ollama eats all the GPU as it runs so cant have other things at the same time.
also, using Llama3.1 now, not sure if llama3 would be faster and good enough, will have to do some tests.
"""

# example of a input text function

def system_prompt_function(system_prompt, user_prompt):
    # Interacting with the LLaMA 3 model, with a system-level instruction
    response = ollama.chat(
        model="llama3.1", 
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    return response['message']['content']

system_prompt = "write a short intro text to a adventure in the following theme"
user_prompt = input("what theme would you like:") 

intro = system_prompt_function(system_prompt, user_prompt)

print(intro)


# example of a formatted response function - that takes instruction and prompt 

# def formatted_response_function(format_instruction, prompt):
#     response = ollama.chat(
#         model="llama3", 
#         messages=[
#             {"role": "system", "content": f"Respond in the following format: {format_instruction}."},
#             {"role": "user", "content": prompt}
#         ]
#     )
#     return response['message']['content']


