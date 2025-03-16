import datetime
import json
import shlex
import subprocess
from typing import Optional, Union, Literal, Sequence, Any, Mapping, Callable

import ollama
from ollama import Message, Tool, Options
from pydantic.json_schema import JsonSchemaValue
from requests_html import HTMLSession

session = HTMLSession()


def get_current_time(*args, **kwargs) -> str:
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_system_information(*args, **kwargs) -> str:
    cmd = "sysctl -a | grep machdep"
    args = shlex.split(cmd)
    res = subprocess.run(args, capture_output=True, text=True).stdout
    return res


def get_current_weather(*args, **kwargs) -> str:
    return "Temperature: 68 F, Humidity: 33%, Wind Speed: 4 mph, Wind Direction: NW"


def add(x: int, y: int) -> int:
    return x + y


def subtract(x: int, y: int) -> int:
    return x - y


def web_request(url: str) -> str:
    # What is the latest version of Python available for download?
    # TODO: cache
    print(f"Requesting {url}")
    res = session.get(url)
    res.raise_for_status()
    return res.html.text


def handle_tool_calls(tool_calls) -> list:
    results = []
    for tool_call in tool_calls:
        function = available_tools[tool_call.function.name]
        result = function(**tool_call.function.arguments)
        results.append({
            "name": tool_call.function.name,
            "arguments": tool_call.function.arguments,
            "result": result,
        })
    return results


# (required) the model name
model: str = "llama3-groq-tool-use:latest"
# model: str = "llama3.2:latest"

# the messages of the chat, this can be used to keep a chat memory
messages: Optional[Sequence[Union[Mapping[str, Any], Message]]] = None

# list of tools in JSON for the model to use if supported
tools: Optional[Sequence[Union[Mapping[str, Any], Tool, Callable]]] = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Get datetime.datetime.now as a formatted string in the format of %Y-%m-%d %H:%M:%S",
            "parameters": None,
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_system_information",
            "description": "Get the result of `sysctl -a | grep machdep` as a string, which is concatenated by newline characters",
            "parameters": None,
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get the current temperature, humidity, wind speed, and wind direction",
            "parameters": None,
        },
    },
    {
        "type": "function",
        "function": {
            "name": "web_request",
            "description": "Submit a GET request using the Python requests library by providing a URL as a string. You will get the raw HTML for the webpage as a string.",
            "parameters": {
                "type": "object",
                "required": ["url"],
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The URL of the webpage to request the HTML for.",
                    },
                }
            }
        },
    },
]

available_tools = {
    "get_current_time": get_current_time,
    "get_system_information": get_system_information,
    "get_current_weather": get_current_weather,
    "web_request": web_request,
}

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
    seed=101,
    num_predict=None,
    top_k=None,
    top_p=None,
    tfs_z=None,
    typical_p=None,
    repeat_last_n=None,
    temperature=5,
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

messages = [
    {
        "role": "system",
        "content": "You have tools available to provide information that you do not know. "
                   "If you need information to answer a question, consider if a tool can provide that information. "
                   "Never ask the user for permission to make a tool call or if they want you to. "
                   "Less user interaction is desired. "
                   "If it is logical to make a tool call, make a tool call. "
                   "If you make a web request, do not describe the page. Read the text the tool provides and use the content to answer the user's question. "
                   "Be concise in your responses. "
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
        model=model,
        messages=messages,
        options=options,
        tools=tools,
    )

    while True:
        if not response.message.content and not response.message.tool_calls:
            print("Nothing")
            break
        elif not response.message.content and response.message.tool_calls:
            # print("Only tool_calls")
            results = handle_tool_calls(response.message.tool_calls)
            for result in results:
                print(result)
                messages.append({
                    "role": "tool",
                    "content": json.dumps(result),
                })
            response = ollama.chat(
                model=model,
                messages=messages,
                options=options,
                tools=tools,
            )
            continue
        elif response.message.content and response.message.tool_calls:
            print("Both")
            break
        elif response.message.content and not response.message.tool_calls:
            # print("Only message")
            messages.append({
                "role": "assistant",
                "content": response.message.content,
            })
            print(response.message.content)
            break
