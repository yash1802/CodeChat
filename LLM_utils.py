def add_message(messages, role, content):
    """
    Adds a message to the conversation history.
    """
    messages.append({"role": role, "content": content})

def get_response_text(llm_response):
    """
    Extracts the text from Claude's response object
    """
    return "\n".join([block.text.strip() for block in llm_response.content])


def make_system_prompt(client, system_prompt, messages, query):
    """
    Makes a system prompt to Claude.
    To be used during LLM object instantiation to ensure this prompt is made only once at the start.
    """

    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1500,
        temperature=0.7,
        system=system_prompt,
        messages=[{"role": "user", "content": query}]
    )

    response_text = get_response_text(response)
    print("\nSummary of the code base: ")
    print(response_text)
    add_message(messages, "assistant", response_text)


def make_user_prompt(client, system_prompt, messages, query):
    """
    Makes a user prompt to Claude.
    """

    # Add user's query to the conversation history
    add_message(messages, "user", query)

    # Send the full conversation history to Claude
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1500,
        temperature=0.7,
        system=system_prompt,
        messages=messages
    )

    response_text = get_response_text(response)

    # Adding Claude's reply to the conversation history
    add_message(messages, "assistant", response_text)
    return response_text

