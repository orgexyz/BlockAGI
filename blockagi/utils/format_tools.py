from typing import List, Union
from langchain.tools import Tool
import json


def generate_schema_dict(pydantic_model):
    schema = pydantic_model.schema()
    properties = schema.get("properties", {})
    required = schema.get("required", [])
    defaults = {
        name: field.default
        for name, field in pydantic_model.__fields__.items()
        if not field.required
    }

    result = {}
    for key, value in properties.items():
        title = value.get("title", "")
        type_ = value.get("type", "")
        description = value.get("description", "")
        optional_str = "" if key in required else ", optional"
        default_value = f" = {defaults[key]}" if key in defaults else ""
        result[key] = f"{title} ({type_}{default_value}{optional_str}) - {description}"

    return result


def format_tools(tools: Union[List[Tool], Tool]):
    if isinstance(tools, Tool):
        return format_tools([tools])
    else:
        return "\n".join(
            [
                f"{i + 1}. {tool.name} - {tool.description}\n"
                f"  usage: {json.dumps({'name':tool.name,'args':generate_schema_dict(tool.args_schema)})}"
                for (i, tool) in enumerate(tools)
            ]
        )
