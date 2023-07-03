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


@dataclass
class ResearchTask:
    tool: str
    args: Dict[str, Any]
    reasoning: str


@dataclass
class ResearchResult(ResearchTask):
    result: Any


@dataclass
class Narrative:
    markdown: str


@dataclass
class Findings:
    narrative: str
    remark: str
    intermediate_objectives: List[Objective]


class BaseResourcePool(ABC):
    @abstractmethod
    def add(self, url: str, description: Optional[str] = None) -> None:
        pass

    @abstractmethod
    def visit(self, url: str) -> None:
        pass

    @abstractmethod
    def get_all(self) -> List[Resource]:
        pass

    @abstractmethod
    def get_unvisited(self) -> List[Resource]:
        pass
