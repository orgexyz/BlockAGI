from blockagi.chains import BlockAGIChain
from blockagi.schema import Findings
from blockagi.tools import DDGSearchAnswerTool, DDGSearchLinksTool, VisitWebTool
from langchain.chat_models import ChatOpenAI


def run_blockagi(
    agent_role,
    openai_api_key,
    openai_model,
    resource_pool,
    objectives,
    blockagi_callback,
    llm_callback,
    iteration_count,
):
    tools = [
        DDGSearchAnswerTool(),
        DDGSearchLinksTool(resource_pool),
        VisitWebTool(resource_pool),
    ]

    llm = ChatOpenAI(
        temperature=0,
        streaming=True,
        model=openai_model,
        openai_api_key=openai_api_key,
        callbacks=[llm_callback],
    )  # type: ignore

    inputs = {
        "objectives": objectives,
        "findings": Findings(
            narrative="Nothing", remark="", intermediate_objectives=[]
        ),
    }

    BlockAGIChain(
        iteration_count=iteration_count,
        agent_role=agent_role,
        llm=llm,
        tools=tools,
        resource_pool=resource_pool,
        callbacks=[blockagi_callback],
    )(inputs=inputs)
