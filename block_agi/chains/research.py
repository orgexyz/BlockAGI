from typing import List, Dict, Any
from dataclasses import asdict
from block_agi.chains.base import CustomCallbackChain
from langchain.tools.base import BaseTool

from block_agi.schema import ResearchTask, ResearchResult


class ResearchChain(CustomCallbackChain):
    tools: List[BaseTool]

    @property
    def input_keys(self) -> List[str]:
        return ["research_tasks"]  # Plan -> Research

    @property
    def output_keys(self) -> List[str]:
        return ["research_results"]  # Research -> Understand

    def _call(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        research_tasks: List[ResearchTask] = inputs["research_tasks"]

        research_results = []

        # Use the tools to run the research tasks
        for task in research_tasks:
            tool = [t for t in self.tools if t.name == task.tool][0]
            if tool is None:
                continue
            task_result = tool.run(task.args)
            research_results.append(
                ResearchResult(
                    result=task_result,
                    **asdict(task),
                )
            )

        return {"research_results": research_results}
