from typing import Optional, Union, Literal, Sequence, Any, Mapping, Callable

import ollama
from ollama import Message, Tool, Options
from pydantic.json_schema import JsonSchemaValue

# (required) the model name
model: str = "llama3-groq-tool-use:latest"

# the messages of the chat, this can be used to keep a chat memory
messages: Optional[Sequence[Union[Mapping[str, Any], Message]]] = None

# list of tools in JSON for the model to use if supported
tools: Optional[Sequence[Union[Mapping[str, Any], Tool, Callable]]] = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get the current weather for a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The name of the city",
                    },
                },
                "required": [
                    "city"
                ],
            },
        },
        },
]

# if false the response will be returned as a single response object, rather than a stream of objects
stream: bool = False

# the format to return a response in. Format can be json or a JSON schema.
format: Optional[Union[Literal["", "json"], JsonSchemaValue]] = None

# additional model parameters listed in the documentation for the Modelfile such as temperature
options: Optional[Union[Mapping[str, Any], Options]] = Options(
    numa=None,
    num_ctx=None,
    num_batch=None,
    num_gpu=None,
    main_gpu=None,
    low_vram=None,
    f16_kv=None,
    logits_all=None,
    vocab_only=None,
    use_mmap=None,
    use_mlock=None,
    embedding_only=None,
    num_thread=None,
    num_keep=None,
    seed=128,
    num_predict=None,
    top_k=None,
    top_p=None,
    tfs_z=None,
    typical_p=None,
    repeat_last_n=None,
    temperature=None,
    repeat_penalty=None,
    presence_penalty=None,
    frequency_penalty=None,
    mirostat=None,
    mirostat_tau=None,
    mirostat_eta=None,
    penalize_newline=None,
    stop=None,
)

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

messages = [{
            "role": "system",
            "content": "You have tools available to provide information you do not know. "
                       "If you need information to answer a question, consider if a tool can provide that information. "
                       "If it can, make a tool call."
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
    )
    messages.append({
        "role": "assistant",
        "content": response.message.content,
    })
    print(response.message.content)
