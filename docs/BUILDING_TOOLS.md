# 🔧 Building Tools for BlockAGI

Tools in BlockAGI follow the same standard as LangChain tools, with a slight addition of a `citation` field to ensure the agent can make the correct references. This guide will help you understand how to build your own tools for BlockAGI.

## 📝 Convention

Here's an example of how to implement a DuckDuckGo Search Links tool:

```python
from itertools import islice
from typing import Optional, Type

from langchain.tools import Tool
from pydantic import BaseModel, Field
from langchain.tools.base import BaseTool
import json

from blockagi.schema import BaseResourcePool
from duckduckgo_search import DDGS

class SearchLinksSchema(BaseModel):
    query: str = Field(
        title="TOPIC", description="any topic you want find relevant links."
    )
    limit: Optional[int] = Field(
        title="NUMBER", description="amount of links you want", default=20
    )

class DDGSearchLinksTool(BaseTool):
    name = "DuckDuckGoSearchLinks"
    description = "Useful for when you need more links to website that points to information about a TOPIC over the internet using DuckDuckGo."
    args_schema: Type[SearchLinksSchema] = SearchLinksSchema
    resource_pool: BaseResourcePool = None

    def __init__(self, resource_pool: BaseResourcePool):
        super().__init__()
        self.resource_pool = resource_pool

    def _run(self, query: str, limit: int = 20):
        ddg = DDGS()
        results = list(islice(ddg.text(query), limit))
        for result in results:
            self.resource_pool.add(url=result["href"], description=result["title"], content=None)
        return {
            "citation": f"DuckDuckGo Search Links: {query}",
            "result": json.dumps(results, indent=2)
        }

    def _arun(self, query: str, limit: int = 20):
        raise NotImplementedError("custom_search does not support async")
```

First, define the `Schema` by extending the LangChain's `BaseModel`. Each field is annotated with

`title`, `description`, and `default` value. Make sure the annotations are descriptive so that LLM can understand what they do.

Next, create a class that extends LangChain's `BaseTool`. Implement the `_run` method which takes the arguments as specified in the schema. Return a dictionary of `citation` and `result` appropriately.

Once you've created the tool, you can import and add the tool in `run.py`.

## 🛠️ Building Your Own Tools

Building your own tools for BlockAGI can greatly enhance its capabilities. Whether you're incorporating on-chain data for blockchain research, or formatting the output for specific needs, the possibilities are endless.

Remember, the goal is to make BlockAGI a powerful and flexible tool for a wide range of research tasks. Your contributions are a big part of that.
