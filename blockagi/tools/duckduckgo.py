from itertools import islice
from typing import Optional, Type

from langchain.tools import DuckDuckGoSearchRun
from langchain.tools import Tool
from pydantic import BaseModel, Field
from langchain.tools.base import BaseTool
import json

from blockagi.schema import BaseResourcePool
from duckduckgo_search import DDGS

# Search Answer Tool =================================


class SearchAnswerSchema(BaseModel):
    query: str = Field(title="QUESTION", description="A well formed question.")


def DDGSearchAnswerTool():
    def searchAnswerDDG(query: str):
        result = DuckDuckGoSearchRun().run(query)
        return {
            "citation": f"DuckDuckGo Search Answer: {query}",
            "result": result
        }

    return Tool.from_function(
        name="DuckDuckGoSearchAnswer",
        func=searchAnswerDDG,
        description="Useful for when you need an answer to a QUESTION on current event over the internet using DuckDuckGo.",
        args_schema=SearchAnswerSchema,
    )


# Search Links Tool ===============================


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
