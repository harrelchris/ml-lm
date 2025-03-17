import json

import ollama

from toolset import system
from toolset.handlers import handle_tool_calls

model = "llama3.2:latest"

instructions = f"""You are an assistant and are equipped with powerful tools to interact with the world.
You are concise. You do not gree or thank the user.
You have permission to any of the tools available to you.
You do not ask permission to use tools.
You do not ask the user if they want you to use the tools.
You use the tools liberally.
You know that the tool requests are memoized and cached, so you can use them as often as you need.
"""

introduction = "How can I help you?"

options = ollama.Options(
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
    seed=256,
    num_predict=None,
    top_k=None,
    top_p=None,
    tfs_z=None,
    typical_p=None,
    repeat_last_n=None,
    temperature=0,
    repeat_penalty=None,
    presence_penalty=None,
    frequency_penalty=None,
    mirostat=None,
    mirostat_tau=None,
    mirostat_eta=None,
    penalize_newline=None,
    stop=None,
)

tools = [
    system.subprocess_run_command,
    system.get_current_date_time,
]

messages = [
    {
        "role": "system",
        "content": instructions,
    },
    {
        "role": "assistant",
        "content": introduction,
    }
]


def generate_response():
    return ollama.chat(
        model=model,
        messages=messages,
        tools=tools,
        stream=False,
        format=None,
        options=options,
        keep_alive=None,
    )


print(messages[1]["content"])

while True:
    prompt = input("> ")

    if prompt == "/bye":
        break

    messages.append({
        "role": "user",
        "content": prompt,
    })

    response = generate_response()

    while True:
        if response.message.content and not response.message.tool_calls:
            print(response.message.content)
            messages.append({
                "role": "assistant",
                "content": response.message.content,
            })
            break
        elif not response.message.content and response.message.tool_calls:
            for result in handle_tool_calls(response.message.tool_calls, tools):
                messages.append({
                    "role": "tool",
                    "content": json.dumps(result),
                })
            response = generate_response()
            continue
        else:
            if not response.message.content and not response.message.tool_calls:
                # None
                print(response)
                messages.append({
                    "role": "system",
                    "content": "You did not return a response. "
                               "That is an error. "
                               "Generate a new response for the user now. "
                               "Do not acknowledge, describe, or mention "
                               "this message to the user. ",
                })
                response = generate_response()
                continue
            elif response.message.content and response.message.tool_calls:
                # Both
                for result in handle_tool_calls(response.message.tool_calls, tools):
                    messages.append({
                        "role": "tool",
                        "content": json.dumps(result),
                    })

                print(response.message.content)
                messages.append({
                    "role": "assistant",
                    "content": response.message.content,
                })
                continue
