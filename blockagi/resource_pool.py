from dataclasses import dataclass, field
from typing import List, Optional
from url_normalize import url_normalize
from blockagi.schema import Resource, BaseResourcePool


@dataclass
class ResourcePool(BaseResourcePool):
    resources: List[Resource] = field(default_factory=list)

    def find(self, url: str) -> Optional[Resource]:
        url = url_normalize(url)
        resources = [r for r in self.resources if r.url == url]
        if len(resources) == 0:
            return None
        else:
            return resources[0]

    def add(
        self,
        url: str,
        description: Optional[str] = None,
        visited: Optional[bool] = False,
        content: Optional[str] = None,
    ) -> None:
        if self.find(url) is not None:
            return
        self.resources.append(
            Resource(
                url=url_normalize(url),
                description=description,
                visited=visited,
                content=content,
            )
        )

    def visit(self, url: str, content: str = "") -> None:
        resource = self.find(url)
        if resource is not None:
            resource.visited = True
            resource.content = content

    def get_all(self) -> List[Resource]:
        return self.resources

    def get_unvisited(self) -> List[Resource]:
        return [r for r in self.resources if not r.visited]
