import json
from typing import List, Dict, Any
from langchain.chat_models.base import BaseChatModel
from langchain.tools.base import BaseTool
from langchain.schema import HumanMessage, SystemMessage
from blockagi.chains.base import CustomCallbackLLMChain
from blockagi.utils import (
    to_json_str,
    format_tools,
    format_objectives,
    format_resources,
)

from blockagi.schema import BaseResourcePool, Objective, Findings, ResearchTask


class PlanChain(CustomCallbackLLMChain):
    agent_role: str = "a Research Assistant"
    llm: BaseChatModel
    resource_pool: BaseResourcePool
    tools: List[BaseTool]

    @property
    def input_keys(self) -> List[str]:
        return [
            "objectives",  # Primary input
            "findings",  # Previous findings
        ]

    @property
    def output_keys(self) -> List[str]:
        return ["research_tasks"]  # Plan -> Research

    def _call(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        objectives: List[Objective] = inputs["objectives"]
        findings: Findings = inputs["findings"]

        self.fire_log(
            f"Planning to fulfill {len(inputs['objectives'])} objectives\n"
            + "\n".join([f"- {o.topic}" for o in inputs["objectives"]])
        )

        response_format = [
            ResearchTask(
                tool="ToolName",
                args="tool arguments",
                reasoning="why you choose this tool",
            ),
            "... use up to 3 tools",
        ]

        messages = [
            SystemMessage(
                content=f"You are {self.agent_role}. "
                "Your job is to create a plan to utilize tools to become expert in the primary goals "
                "under OBJECTIVES and the secondary goals under GENERATED_OBJECTIVES. "
                "Take into account the limitation of all the tools available to you."
                "\n\n"
                "## USER OBJECTIVES:\n"
                f"{format_objectives(objectives)}\n\n"
                "## GENERATED OBJECTIVES:\n"
                f"{format_objectives(findings.generated_objectives)}\n\n"
                "## REMARK:\n"
                f"{findings.remark}\n\n"
                "You should ONLY respond in the JSON format as described below\n"
                "## RESPONSE FORMAT:\n"
                f"{to_json_str(response_format)}"
            ),
            HumanMessage(
                content="## PREVIOUS FINDINGS:\n"
                "```\n"
                f"{findings.narrative}\n"
                "```\n\n"
                "## RESOURCE POOL\n"
                f"{format_resources(self.resource_pool.get_unvisited())}\n\n"
                "## AVAILABLE TOOLS:\n"
                f"{format_tools(self.tools)}"
                "\n\n"
                "# YOUR TASK:\n"
                "Consider PREVIOUS FINDINGS and derive a plan to use up to 3 tools to become expert. "
                "Only use tools and links specified above. Do NOT use tools to visit unknown links.\n"
                "Prioritize visiting links under RESOURCE POOL over searching the internet "
                "unless the existing resources are not enough to answer your research questions.\n"
                "\n"
                "Important notes:\n"
                "- Prioritize finding more about topics with low expertise.\n"
                "- When your expertise is low, consider finding more resource and gather generic information.\n"
                "- When your expertise is high, consider visiting specific resources over finding generic answer.\n"
                '- When "No resources available", do not visit any link.\n'
                "\n"
                "Respond using ONLY the format specified above:"
            ),
        ]

        response = self.retry_llm(messages)

        research_tasks = [
            ResearchTask(
                tool=task["tool"],
                args=task["args"],
                reasoning=task["reasoning"],
            )
            for task in json.loads(response.content)
        ]

        return {"research_tasks": research_tasks}
