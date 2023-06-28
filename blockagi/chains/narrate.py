from typing import List, Dict, Any
from langchain.chat_models.base import BaseChatModel
from langchain.tools.base import BaseTool
from langchain.schema import HumanMessage, SystemMessage
from blockagi.chains.base import CustomCallbackChain
from blockagi.utils import to_json_str, format_objectives

from blockagi.schema import Objective, Findings, ResearchResult, Narrative


class NarrateChain(CustomCallbackChain):
    llm: BaseChatModel
    tools: List[BaseTool]

    @property
    def input_keys(self) -> List[str]:
        return [
            "objectives",  # Primary input
            "findings",  # Previous findings
            "research_results",  # Research -> Narrate
        ]

    @property
    def output_keys(self) -> List[str]:
        return [
            "narrative",  # Narrate -> Evaluate
        ]

    def _call(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        # As research results can be large, we chunk them into smaller pieces
        # Max size of each chunk is 20,000 characters, approximately
        findings: Findings = inputs["findings"]
        research_results: List[ResearchResult] = inputs["research_results"]

        chunks = []
        current_chunk = []
        current_size = 0

        # Sort research results by size (smaller first)
        sorted_results = sorted(research_results, key=lambda x: len(to_json_str(x)))

        # Put researches into chunks
        for research_result in sorted_results:
            research_result_size = len(to_json_str(research_result))
            if len(current_chunk) > 0 and current_size + research_result_size > 20000:
                # Cannot fit into current chunk, start a new one
                chunks.append(current_chunk)
                current_chunk = [research_result]
                current_size = research_result_size
            else:
                current_chunk.append(research_result)
                current_size += research_result_size

        if len(current_chunk) > 0:
            chunks.append(current_chunk)

        self.fire_log(
            f"Applying {len(research_results)} results splitting into {len(chunks)} chunks"
        )
        # Call each chunk and pass the narrative to the next chunk
        current_narrative = findings.narrative
        for index, chunk in enumerate(chunks):
            self.fire_log(f"  Narating chunk {index+1}/{len(chunks)}")
            current_narrative = self._call_chunk(
                {
                    **inputs,
                    "research_results": chunk,
                    "findings": Findings(
                        intermediate_objectives=findings.intermediate_objectives,
                        remark=findings.remark,
                        narrative=current_narrative,
                    ),
                }
            )

        return {"narrative": Narrative(markdown=current_narrative)}

    def _call_chunk(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        objectives: List[Objective] = inputs["objectives"]
        findings: Findings = inputs["findings"]
        research_results: List[ResearchResult] = inputs["research_results"]

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
                "## PREVIOUS FINDINGS:\n"
                "```\n"
                f"{findings.narrative}\n"
                "```\n\n"
                "You should ONLY respond in the JSON format as described below\n"
                "## RESPONSE FORMAT:\n"
                "- Markdown document with up to 10 sections, each with up to 500 words.\n"
            ),
            HumanMessage(
                content="You just finished a research iteration. Here are the raw results:\n\n"
                "## RESEARCH RESULTS:\n"
                f"{to_json_str(research_results)}"
                "\n\n"
                "Please edit the PREVIOUS FINDINGS by adding new info from the RESEARCH RESULTS.\n"
                "- The goal is to have a complete narrative that fulfills the KEY OBJECTIVES.\n"
                "- Take into account the INTERMEDIATE OBJECTIVES and REMARK when editing the narrative.\n"
                "- The narrative should be a markdown document with up to 10 sections, each with up to 500 words.\n"
                "- Make sure to include citations and links in your markdown document in every sentence.\n"
                "- Do NOT mention the tools used in the narrative.\n"
                "- Do NOT include `## PREVIOUS FINDINGS` section in the markdown. Return new content only.\n\n"
                "Respond with the new narrative in the RESPONSE FORMAT."
            ),
        ]

        response = self.llm(messages)

        return response.content
