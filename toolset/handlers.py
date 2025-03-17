

def handle_tool_calls(tool_calls, tools: list) -> list:
    tools_dict = {f.__name__: f for f in tools}
    res = []
    for tool_call in tool_calls:
        function = tools_dict[tool_call.function.name]
        if tool_call.function.arguments:
            result = function(**tool_call.function.arguments)
        else:
            result = function()
        res.append({
            "name": tool_call.function.name,
            "arguments": tool_call.function.arguments,
            "result": result,
        })
    return res
