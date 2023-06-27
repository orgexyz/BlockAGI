import json
from typing import List, Dict, Any
from langchain.chat_models.base import BaseChatModel
from langchain.tools.base import BaseTool
from langchain.schema import HumanMessage, SystemMessage
from blockagi.chains.base import CustomCallbackChain
from blockagi.utils import to_json_str, format_objectives

from blockagi.schema import Objective, Findings, Narrative


class EvaluateChain(CustomCallbackChain):
    llm: BaseChatModel
    tools: List[BaseTool]

    @property
    def input_keys(self) -> List[str]:
        return [
            "objectives",  # Primary input
            "findings",  # Previous findings
            "narrative",  # Narrate    -> Evaluate
        ]

    @property
    def output_keys(self) -> List[str]:
        return [
            # Feedback to next iteration
            "updated_findings",  # Evaluate   -> Plan
            "updated_objectives",  # Evaluate   -> Plan
        ]

    def _call(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        objectives: List[Objective] = inputs["objectives"]
        findings: Findings = inputs["findings"]
        narrative: Narrative = inputs["narrative"]

        response_format = {
            "updated_findings": {
                "intermediate_objectives": [
                    Objective(
                        topic="additional objective that helps achieve the key objectives",
                        expertise="a new float value in [0, 1] range indicating the expertise of this objective",
                    )
                ],
                "remark": "a note to the next iteration of BlockAGI to help it improve",
            },
            "updated_objectives": [
                Objective(
                    topic="same as the key objectives",
                    expertise="a new float value in [0, 1] range indicating the expertise of this objective",
                ),
                "... include all objectives",
            ],
        }

        messages = [
            SystemMessage(
                content="You are BlockAGI, a Crypto Research Assistant. "
                "Your job is to become an expert in the topics under the OBJECTIVES section, "
                "each with a weight (0 to 1) which indicates your current expertise in that topic."
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
                "You should ONLY respond in the JSON format as described below\n"
                "## RESPONSE FORMAT:\n"
                f"{to_json_str(response_format)}"
            ),
            HumanMessage(
                content="You just finished a research iteration and formulated a narrative with the following instruction.\n"
                "- The goal is to have a complete narrative that fulfills the KEY OBJECTIVES.\n"
                "- Take into account the INTERMEDIATE OBJECTIVES and REMARK when editing the narrative.\n"
                "- The narrative should be a markdown document with up to 10 sections, each with up to 500 words.\n"
                "- Make sure to include citations and links in your markdown document in every sentence.\n"
                "\n"
                "## YOUR FINDINGS:\n"
                "```\n"
                f"{narrative.markdown}\n"
                "```\n\n"
                "Please give a thorough an evaluation for the insights found by BlockAGI. "
                "Your evaluation should include:\n"
                "- Up to 5 intermediate_objectives, which helps the next iteration of BlockAGI become "
                "an expert in all the OBJECTIVES. Be critical and detail-focused. Take into account "
                "the PREVIOUS FINDINGS and carry over the unfulfilled objectives as needed.\n"
                "- A remark to help the next iteration of BlockAGI improve. Be critical and suggest "
                "only concise and helpful feedback for the AI agent.\n"
                "- A new weight of OBJECTIVES for the next iteration of BlockAGI. Make sure to keep the exact same topics. "
                "For each objective, if the information is already known, its weight should be lower."
                "\n\n"
                "Respond using ONLY the format specified above:"
            ),
        ]

        response = self.llm(messages)

        result = json.loads(response.content)

        updated_findings = Findings(
            intermediate_objectives=[
                Objective(
                    topic=obj["topic"],
                    expertise=obj["expertise"],
                )
                for obj in result["updated_findings"]["intermediate_objectives"]
            ],
            remark=result["updated_findings"]["remark"],
            narrative=narrative.markdown,
        )

        updated_objectives = [
            Objective(
                topic=obj["topic"],
                expertise=obj["expertise"],
            )
            for obj in result["updated_objectives"]
        ]

        return {
            "updated_findings": updated_findings,
            "updated_objectives": updated_objectives,
        }
