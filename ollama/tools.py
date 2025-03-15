import datetime
import shlex
import subprocess

import ollama


def get_system_info(*args, **kwargs):
    """Get machine details using a subprocess call"""

    cmd = "sysctl -a | grep machdep"
    args = shlex.split(cmd)
    result = subprocess.run(args, capture_output=True, text=True)
    return result.stdout


def get_current_time(*args, **kwargs):
    """Get the current time as a string in the format of %Y-%m-%d %H:%M:%S"""

    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


response = ollama.chat(
    model="llama3.2:latest",
    messages=[
        {
            "role": "user",
            # "content": "What is the current time?"
            "content": "Tell me about my system"
        }
    ],
    tools=[
        get_current_time,
        get_system_info,
    ],
)

print(response)

# available_functions = {
#     "get_current_time": get_current_time,
#     "get_system_info": get_system_info,
# }
#
#
# for tool in response.message.tool_calls or []:
#     function_to_call = available_functions.get(tool.function.name)
#     if function_to_call:
#         print("Function output:", function_to_call(**tool.function.arguments))
#     else:
#         print("Function not found:", tool.function.name)
