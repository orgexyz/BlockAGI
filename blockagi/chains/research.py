import json
from typing import List, Dict, Any
from dataclasses import asdict
from blockagi.chains.base import CustomCallbackChain
from langchain.tools.base import BaseTool

from blockagi.schema import ResearchTask, ResearchResult


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

        self.fire_log(f"Executing {len(research_tasks)} research tasks")

        # Use the tools to run the research tasks
        for index, task in enumerate(research_tasks):
            self.fire_log(f"  Task {index+1}) {task.tool} {json.dumps(task.args)}")
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
