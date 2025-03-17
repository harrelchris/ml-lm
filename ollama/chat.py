from typing import Optional, Union, Literal, Sequence, Any, Mapping, Callable

import ollama
from ollama import Message, Tool, Options
from pydantic.json_schema import JsonSchemaValue

# (required) the model name
model: str = "gemma3:4b"

# the messages of the chat, this can be used to keep a chat memory
messages: Optional[Sequence[Union[Mapping[str, Any], Message]]] = None

# list of tools in JSON for the model to use if supported
tools: Optional[Sequence[Union[Mapping[str, Any], Tool, Callable]]] = None

# if false the response will be returned as a single response object, rather than a stream of objects
stream: bool = False

# the format to return a response in. Format can be json or a JSON schema.
format: Optional[Union[Literal['', 'json'], JsonSchemaValue]] = None

# additional model parameters listed in the documentation for the Modelfile such as temperature
options: Optional[Union[Mapping[str, Any], Options]] = None

# controls how long the model will stay loaded into memory following the request (default: 5m)
keep_alive: Optional[Union[float, str]] = None


example_message = {
    # the role of the message, either system, user, assistant, or tool
    "role": "system",

    # the content of the message
    "content": "",

    # (optional): a list of images to include in the message (for multimodal models such as llava)
    "images": [],

    # (optional): a list of tools in JSON that the model wants to use
    "tool_calls": []
}

messages = [
        {
            "role": "system",
            "content": "You are a concise assistant who answers briefly. "
        },
        {
            "role": "assistant",
            "content": "What can I help you with?",
        }
]

print(messages[1]["content"])

while True:
    prompt = input("> ")

    if prompt == "q":
        break

    messages.append({
        "role": "user",
        "content": prompt,
    })

    response = ollama.chat(
        model="llama3.2:latest",
        messages=messages,
        tools=tools,
        stream=stream,
        format=format,
        options=options,
        keep_alive=keep_alive,
    )
    messages.append({
        "role": "assistant",
        "content": response.message.content,
    })
    print(response.message.content)
