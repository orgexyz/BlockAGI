import json
from typing import List, Dict, Any
from langchain.chat_models.base import BaseChatModel
from langchain.tools.base import BaseTool
from langchain.schema import HumanMessage, SystemMessage
from block_agi.chains.base import CustomCallbackChain
from block_agi.utils import (
    to_json_str,
    format_tools,
    format_objectives,
    format_resources
)

from block_agi.schema import BaseResourcePool, Objective, Findings, ResearchTask

class PlanChain(CustomCallbackChain):
    agent_role: str = "a Research Assistant"
    llm: BaseChatModel
    resource_pool: BaseResourcePool
    tools: List[BaseTool]

    @property
    def input_keys(self) -> List[str]:
        return [
            'objectives',       # Primary input
            'findings',         # Previous findings
        ]

    @property
    def output_keys(self) -> List[str]:
        return [
            'research_tasks'    # Plan -> Research
        ]
    
    def _call(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        objectives: List[Objective] = inputs['objectives']
        findings: Findings = inputs['findings']

        response_format = [
            ResearchTask(
                tool="ToolName",
                args="tool arguments",
                reasoning="why you choose this tool",
            ),
            "... more tools"
        ]

        messages = [
            SystemMessage(content=
                f"You are {self.agent_role}. "
                "Your job is to become an expert in the topics under the OBJECTIVES section, "
                "each with a weight (0 to 1) indicating your current expertise in that topic."
                "\n\n"
                "You will conduct research in multiple iterations, using the tools provided. "
                "Use the topics under INTERMEDIATE OBJECTIVES and REMARK to help you determine "
                "appropriate tools to refine PREVIOUS FINDINGS and fulfill the OBJECTIVES."
                "\n\n"
                "## KEY OBJECTIVES:\n"
                f"{format_objectives(objectives)}\n\n"
                "## INTERMEDIATE OBJECTIVES:\n"
                f"{format_objectives(findings.intermediate_objectives)}\n\n"
                "## REMARK:\n"
                f"{findings.remark}\n\n"
                "## RELEVANT LINKS\n"
                f"{format_resources(self.resource_pool.get_all())}\n\n"
                "You should ONLY respond in the JSON format as described below\n"
                "## RESPONSE FORMAT:\n"
                f"{to_json_str(response_format)}"
            ),
            HumanMessage(content=
                "## PREVIOUS FINDINGS:\n"
                "```\n"
                f"{findings.narrative}\n"
                "```\n\n"
                "## AVAILABLE TOOLS:\n"
                f"{format_tools(self.tools)}"
                "\n\n"
                "Please derive a plan to use up to 5 tools."
            )
        ]

        response = self.llm(messages)

        research_tasks = [
            ResearchTask(
                tool=task['tool'],
                args=task['args'],
                reasoning=task['reasoning'],
            ) for task in json.loads(response.content)
        ]
        
        return { 'research_tasks': research_tasks }
    
