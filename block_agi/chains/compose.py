from typing import List, Dict, Any, Optional
from langchain.callbacks.base import BaseCallbackHandler
from langchain.chat_models.base import BaseChatModel
from langchain.callbacks.base import BaseCallbackHandler
from langchain.tools.base import BaseTool

from block_agi.schema import BaseResourcePool
from block_agi.chains.base import CustomCallbackChain
from block_agi.chains.plan import PlanChain
from block_agi.chains.research import ResearchChain
from block_agi.chains.narrate import NarrateChain
from block_agi.chains.evaluate import EvaluateChain


class BlockAGIChain(CustomCallbackChain):
    agent_role: str = None
    iteration_count: int
    chains: List[CustomCallbackChain] = []
    llm: BaseChatModel
    resource_pool: BaseResourcePool
    tools: List[BaseTool] = []
    callbacks: Optional[List[BaseCallbackHandler]] = None

    @property
    def input_keys(self) -> List[str]:
        return [
            'objectives',       # Primary input
            'findings',         # Previous findings
        ]

    @property
    def output_keys(self) -> List[str]:
        return [
            # Primary outputs
            'research_tasks',               # Plan       -> Research
            'research_results',             # Research   -> Understand
            'research_understandings',      # Understand -> Narrate
            'narrative',                    # Narrate    -> Evaluate

            # Feedback to next iteration
            'updated_findings',             # Evaluate   -> Plan
            'updated_objectives'            # Evaluate   -> Plan
        ]

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self.chains = [
            PlanChain(**kwargs),
            ResearchChain(**kwargs),
            NarrateChain(**kwargs),
            EvaluateChain(**kwargs),
        ]

    def _call(
        self,
        inputs: Dict[str, Any],
    ) -> Dict[str, Any]:
        # Run in multiple iterations
        for _ in range(self.iteration_count):
            outputs = None
            # Call the callback
            self.fire_callback(
                event='on_iteration_start',
                inputs=inputs
            )
            # Run through all the chains
            for chain in self.chains:
                # Call the callback
                self.fire_callback(
                    event='on_step_start',
                    step=chain.__class__.__name__,
                    inputs=inputs
                )
                # Call the current step
                outputs = chain(inputs=inputs)
                # Call the callback
                self.fire_callback(
                    event='on_step_end',
                    step=chain.__class__.__name__,
                    inputs=inputs,
                    outputs=outputs
                )
                # Update the inputs for the next step
                inputs = outputs

            # Call the callback
            self.fire_callback(
                event='on_iteration_end',
                outputs=outputs
            )
            # Set the inputs for the next iteration
            inputs = {
                'objectives': outputs['updated_objectives'],
                'findings': outputs['updated_findings']
            }
