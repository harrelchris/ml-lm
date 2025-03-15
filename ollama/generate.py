"""Ollama Generate

https://github.com/ollama/ollama/blob/main/docs/api.md
"""
from typing import Optional, Union, Literal, Sequence, Any, Mapping

from ollama import generate, Options
from pydantic.json_schema import JsonSchemaValue

# (required) the model name
model: str = "gemma3:4b"

# the prompt to generate a response for
prompt: Optional[str] = None

# the text after the model response
suffix: Optional[str] = None

# system message to (overrides what is defined in the Modelfile)
system: Optional[str] = None

# the prompt template to use (overrides what is defined in the Modelfile)
template: Optional[str] = None

# DEPRECATED
# the context parameter returned from a previous request to /generate,
# this can be used to keep a short conversational memory
context: Optional[Sequence[int]] = None

# if false the response will be returned as a single response object, rather than a stream of objects
stream: bool = False

# if true no formatting will be applied to the prompt. You may choose to use the raw
# parameter if you are specifying a full templated prompt in your request to the API
raw: Optional[bool] = None

# the format to return a response in. Format can be json or a JSON schema
format: Optional[Union[Literal['', 'json'], JsonSchemaValue]] = None

# (optional) a list of base64-encoded images (for multimodal models such as llava)
images: Optional[Sequence[Union[str, bytes]]] = None

# additional model parameters listed in the documentation for the Modelfile such as temperature
options: Optional[Union[Mapping[str, Any], Options]] = None

# controls how long the model will stay loaded into memory following the request (default: 5m)
keep_alive: Optional[Union[float, str]] = None

response = generate(
    model=model,
    prompt="How are you?",
    suffix=suffix,
    system=system,
    template=template,
    context=context,
    stream=stream,
    raw=raw,
    format=format,
    images=images,
    options=options,
    keep_alive=keep_alive,
)

text = response.response
created_at = response.created_at
total_duration = response.total_duration

print(text)
