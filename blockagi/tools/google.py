import json
import os
from langchain.tools.base import BaseTool
from pydantic import BaseModel, Field
from typing import Optional, Type

from blockagi.schema import BaseResourcePool
from googleapiclient.discovery import build


class GoogleLinksSchema(BaseModel):
    query: str = Field(
        title="TOPIC", description="any topic you want find relevant links."
    )
    limit: Optional[int] = Field(
        title="NUMBER", description="amount of links you want", default=20
    )


class GoogleSearchLinksTool(BaseTool):
    name = "GoogleSearchLinks"
    description = "Useful for when you need more links to website that points to information about a TOPIC over the internet using Google."
    args_schema: Type[GoogleLinksSchema] = GoogleLinksSchema
    resource_pool: BaseResourcePool = None

    def __init__(self, resource_pool: BaseResourcePool):
        super().__init__()
        self.resource_pool = resource_pool

    def _run(self, query: str, limit: int = 10):
        if not os.getenv("GOOGLE_API_KEY") or not os.getenv("GOOGLE_CSE_ID"):
            raise ValueError("Cannot use Google; No GOOGLE_API_KEY and GOOGLE_CSE_ID")
        service = build("customsearch", "v1", developerKey=os.getenv("GOOGLE_API_KEY"))
        result = (
            service.cse()
            .list(q=query, cx=os.getenv("GOOGLE_CSE_ID"), num=limit)
            .execute()
        )
        for e in result["items"]:
            self.resource_pool.add(url=e["link"], description=e["title"], content=None)
        return {
            "citation": f"Google Search Links: {query}",
            "result": json.dumps(
                [
                    {
                        "title": e["title"],
                        "link": e["link"],
                        "snippet": e["snippet"],
                    }
                    for e in result["items"]
                ],
                indent=2,
            ),
        }

    def _arun(self, query: str, limit: int = 20):
        raise NotImplementedError("custom_search does not support async")
