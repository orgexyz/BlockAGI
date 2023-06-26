#!/usr/bin/env python3

import os
from typing import Any, Dict
from block_agi.chains import BlockAGIChain, BlockAGICallbackHandler
from block_agi.schema import Objective, Findings
from block_agi.tools import DDGSearchAnswerTool, DDGSearchLinksTool, VisitWebTool
from block_agi.resource_pool import ResourcePool
from langchain.chat_models import ChatOpenAI
from langchain.callbacks.base import BaseCallbackHandler

class CallbackHandler(BlockAGICallbackHandler):
    def on_step_start(self, step: str, inputs: Dict[str, Any], **kwargs: Any) -> Any:
        """Run on step start."""
        print("="*50)
        print(f"== Step: {step} ".ljust(50, "="))
        print("="*50)

    def on_step_end(self, step: str, inputs: Dict[str, Any], outputs: Dict[str, Any], **kwargs: Any) -> Any:
        """Run on step end."""
        pass
        # print(to_json_str(outputs))

class LLMCallback(BaseCallbackHandler):
    def on_llm_new_token(self, token: str, **kwargs: Any) -> Any:
        """Run on new LLM token. Only available when streaming is enabled."""
        print(token, end="", flush=True)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo-16k")

if __name__ == "__main__":
    resource_pool = ResourcePool()

    tools = [
        DDGSearchAnswerTool(),
        DDGSearchLinksTool(resource_pool),
        VisitWebTool(resource_pool)
    ]

    llm = ChatOpenAI(
        temperature=0,
        streaming=True,
        model=OPENAI_MODEL, 
        openai_api_key=OPENAI_API_KEY,
        callbacks=[LLMCallback()]
    )

    inputs = {
        "objectives": [
            Objective(
                topic="What is Neutron smart contract platform on cosmos?",
                expertise=0.,
            ),
            Objective(
                topic="How is Neutron different from Juno and Osmosis?",
                expertise=0.,
            ),
            Objective(
                topic="How is Neutron different from CosmWasm?",
                expertise=0.,
            ),
        ],
        "findings": Findings(
            narrative="Nothing",
            remark="",
            intermediate_objectives=[], 
        )
    }

    chain = BlockAGIChain(
        agent_role="BlockAGI, a Crypto Research Assistant",
        llm=llm,
        tools=tools,
        resource_pool=resource_pool,
        callbacks=[CallbackHandler()]
    )

    outputs = chain(
        inputs=inputs,
    )
    