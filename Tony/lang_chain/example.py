def run(model: str, question: str):
    client = ollama.Client()

    # Initialize conversation with a user query
    messages = [{"role": "user", "content": question}]

    # First API call: Send the query and function description to the model
    response = client.chat(
        model=model,
        messages=messages,
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "get_flight_times",
                    "description": "Get the flight times between two cities",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "departure": {
                                "type": "string",
                                "description": "The departure city (airport code)",
                            },
                            "arrival": {
                                "type": "string",
                                "description": "The arrival city (airport code)",
                            },
                        },
                        "required": ["departure", "arrival"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "search_data_in_vector_db",
                    "description": "Search about Artificial Intelligence data in a vector database",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "The search query",
                            },
                        },
                        "required": ["query"],
                    },
                },
            },
        ],
    )

    # Add the model's response to the conversation history
    messages.append(response["message"])

    # Check if the model decided to use the provided function

    if not response["message"].get("tool_calls"):
        print("The model didn't use the function. Its response was:")
        print(response["message"]["content"])
        return

    # Process function calls made by the model
    if response["message"].get("tool_calls"):
        available_functions = {
            "get_flight_times": get_flight_times,
            "search_data_in_vector_db": search_data_in_vector_db,
        }

        for tool in response["message"]["tool_calls"]:
            function_to_call = available_functions[tool["function"]["name"]]
            function_args = tool["function"]["arguments"]
            function_response = function_to_call(**function_args)

            # Add function response to the conversation
            messages.append(
                {
                    "role": "tool",
                    "content": function_response,
                }
            )

    # Second API call: Get final response from the model
    final_response = client.chat(model=model, messages=messages)

    print(final_response["message"]["content"])
