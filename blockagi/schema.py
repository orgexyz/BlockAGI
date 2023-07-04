from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict, Any, Optional


@dataclass
class Objective:
    topic: str
    expertise: float


@dataclass
class Resource:
    url: str
    description: Optional[str]
    visited: Optional[bool]
    content: Optional[str] = None


@dataclass
class ResearchTask:
    tool: str
    args: Dict[str, Any]
    reasoning: str


@dataclass
class ResearchResult(ResearchTask):
    result: Any
    citation: Optional[str] = None


@dataclass
class Narrative:
    markdown: str


@dataclass
class Findings:
    narrative: str
    remark: str
    generated_objectives: List[Objective]


class BaseResourcePool(ABC):
    @abstractmethod
    def find(self, url: str) -> Optional[Resource]:
        pass

    @abstractmethod
    def add(
        self, url: str, description: Optional[str] = None, content: Optional[str] = None
    ) -> None:
        pass

    @abstractmethod
    def visit(self, url: str, content: Optional[str] = "") -> None:
        pass

    @abstractmethod
    def get_all(self) -> List[Resource]:
        pass

    @abstractmethod
    def get_unvisited(self) -> List[Resource]:
        pass
