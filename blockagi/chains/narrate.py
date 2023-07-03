from typing import List, Dict, Any
from langchain.chat_models.base import BaseChatModel
from langchain.tools.base import BaseTool
from langchain.schema import HumanMessage, SystemMessage
from blockagi.chains.base import CustomCallbackLLMChain
from blockagi.utils import to_json_str, format_objectives

from blockagi.schema import Objective, Findings, ResearchResult, Narrative


class NarrateChain(CustomCallbackLLMChain):
    agent_role: str = "a Research Assistant"
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
            self.fire_log(f"Narrating chunk {index+1}/{len(chunks)}")
            current_narrative = self._call_chunk(
                {
                    **inputs,
                    "research_results": chunk,
                    "findings": Findings(
                        generated_objectives=findings.generated_objectives,
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
                content=f"You are {self.agent_role}. "
                "Your job is to write a comprehensive report to fulfill the primary goals "
                "under OBJECTIVES and the secondary goals under GENERATED_OBJECTIVES."
                "\n\n"
                "## USER OBJECTIVES:\n"
                f"{format_objectives(objectives)}\n\n"
                "## GENERATED OBJECTIVES:\n"
                f"{format_objectives(findings.generated_objectives)}\n\n"
                "## REMARK:\n"
                f"{findings.remark}\n\n"
                "## PREVIOUS FINDINGS:\n"
                "```\n"
                f"{findings.narrative}\n"
                "```\n\n"
                "You should ONLY respond in the JSON format as described below\n"
                "## RESPONSE FORMAT:\n"
                "- Markdown document with up to 8 sections, each with up to 350 words.\n"
                "- The content should be concise and easy to digest. Avoid repeating yourself.\n"
                "- First section is ALWAYS about what you learned from the research results "
                "and how you plan to rewrite the report.\n"
                "- Start the markdown with a H1 heading with emoji (e.g. `# ⛳️ Title`).\n"
                "- Start each section with a H2 heading with emoji (e.g. `## 🤖 Section Title`).\n"
                "- Use approritate emoji for each section's content.\n"
                "- Use bullet points when appropriate to make the document easy to digest.\n"
                "- Use footnote for citations (e.g. `[^1^]` for refering to link [1]).\n"
                "- Add footnotes at the end of markdown document "
                "(e.g `[^1^]: [<description>](<link>)` for describing link [1]). Note the colon (:) sign."
                "\n\n"
                "## EXAMPLE RESPONSE:\n"
                "```\n"
                "> Plan: based on the results, I will revise ... I will add ... I will remove ..."
                "Finally I will add all the references at the end.\n"
                "# 🤔 What is BlockAGI\n"
                "## 🌈 Automated AI Agent \n"
                "BlockAGI is an open-source research agent built with Python3, "
                "utilizing the capabilities of LangChain and OpenAI [^1^]. ...\n"
                "## 📚 Capabilities of BlockAGI\n"
                "Users can interact with BlockAGI through self-hosing the software [^2^].\n\n"
                "[^1^]: [BlockAGI Github](https://github.com/blockpipe/blockagi)\n"
                '[^2^]: Research Result: WebSearch "BlockAGI"\n'
                "```"
            ),
            HumanMessage(
                content="You just finished a research iteration. Here are the raw results:\n\n"
                "## RESEARCH RESULTS:\n"
                f"{to_json_str(research_results)}"
                "\n\n"
                "## YOUR TASK:\n"
                "Write a report on the USER OBJECTIVES by iterating over the PREVIOUS FINDINGS "
                "and adding new information from RESEARCH RESULTS. Use ALL the facts and citation in the PREVIOUS FINDINGS. "
                "All new facts must be supported by references to RESEARCH RESULTS."
                "\n"
                "Important notes:\n"
                "- Always write plan first. The plan should focus on new information you received, "
                "and what would you like to revise. Keep it concise and avoid using bullet points. Then write the report.\n"
                "- Preserve all the footnote references. Make sure mention mention of `[^<number>]` has a link in the footnote.\n"
                "- Make sure the number of footnote references is greater or equal to PREVIOUS FINDINGS footnotes.\n"
                f"- Avoid mentioning how {self.agent_role} works.\n"
                "- Avoid mentioning tools used in the writing. If result is not helpful then exclude it.\n"
                "- Avoid mentioning `## PREVIOUS FINDINGS` section in the markdown. Return new content only.\n"
                "Respond using ONLY the markdown format specified above:"
            ),
        ]

        response = self.retry_llm(messages)

        return response.content
