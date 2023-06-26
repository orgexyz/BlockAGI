import os
import dotenv
import typer
import uvicorn
import webbrowser
import threading
from datetime import datetime
from dataclasses import dataclass
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from langchain.callbacks.base import BaseCallbackHandler
from starlette.responses import FileResponse


from block_agi.chains.base import BlockAGICallbackHandler
from block_agi.schema import Objective, Findings, Narrative, Resource
from block_agi.resource_pool import ResourcePool
from block_agi.run import run_blockagi


app = FastAPI()
app.mount('/dist', StaticFiles(directory='dist'), name='dist')


@app.get('/',)
def get_index():
    return FileResponse('dist/index.html')


@dataclass
class StepHistory:
    timestamp: str
    value: str


@dataclass
class Status:
    step: str
    round: int


@dataclass
class LLMLog:
    prompt: str
    response: str


@dataclass
class BlockAGIState:
    agent_role: str
    status: Status
    historical_steps: list[StepHistory]
    objectives: list[Objective]
    findings: list[Findings]
    resources: list[Resource]
    llm_logs: list[LLMLog]
    narratives: list[Narrative]


@app.get('/api/state')
def get_api_state():
    app.state.blockagi_state.resources = app.state.resource_pool.resources
    return app.state.blockagi_state


@app.on_event('startup')
def on_startup():
    app.state.resource_pool = ResourcePool()
    threading.Thread(
        target=run_blockagi,
        kwargs=dict(
            agent_role=app.state.blockagi_state.agent_role,
            openai_api_key=app.state.openai_api_key,
            openai_model=app.state.openai_model,
            resource_pool=app.state.resource_pool,
            objectives=app.state.blockagi_state.objectives,
            blockagi_callback=BlockAGICallback(app.state.blockagi_state),
            llm_callback=LLMCallback(app.state.blockagi_state),
        )
    ).start()
    webbrowser.open(f'http://{app.state.host}:{app.state.port}')


@app.on_event('shutdown')
def on_shutdown():
    os._exit(0)


class BlockAGICallback(BlockAGICallbackHandler):
    state: BlockAGIState

    def __init__(self, blockagi_state):
        self.state = blockagi_state

    def on_step_start(self, step, inputs, **kwargs):
        round = self.state.status.round
        if step == 'PlanChain':
            round += 1
        self.state.status = Status(step=step, round=round)
        value = None
        if step == 'PlanChain':
            value = f'R#{round}: Planning for {len(inputs["objectives"])} objectives'
        elif step == 'ResearchChain':
            value = f'R#{round}: Executing {len(inputs["research_tasks"])} research tasks'
        elif step == 'NarrateChain':
            value = f'R#{round}: Applying {len(inputs["research_results"])} results to the narrative'
        elif step == 'EvaluateChain':
            value = f'R#{round}: Evaluation for new objectives'
        if value:
            self.state.historical_steps.append(StepHistory(
                timestamp=datetime.utcnow().isoformat(),
                value=value,
            ))

    def on_step_end(self, step, inputs, outputs, **kwargs):
        if step == 'PlanChain':
            pass
        elif step == 'ResearchChain':
            pass
        elif step == 'NarrateChain':
            self.state.narratives.append(outputs['narrative'])
        elif step == 'EvaluateChain':
            self.state.objectives = outputs['updated_objectives']
            self.state.findings = outputs['updated_findings']


class LLMCallback(BaseCallbackHandler):
    state: BlockAGIState

    def __init__(self, blockagi_state):
        self.state = blockagi_state

    def on_llm_start(self, serialized, prompts, **kwargs):
        self.state.llm_logs.append(LLMLog(
            prompt=''.join(prompts),
            response='',
        ))

    def on_llm_new_token(self, token: str, **kwargs):
        self.state.llm_logs[-1].response += token


def main(
    host: str = typer.Option(envvar='WEB_HOST'),
    port: int = typer.Option(envvar='WEB_PORT'),
    agent_role: str = typer.Option(envvar='BLOCKAGI_AGENT_ROLE'),
    objectives: list[str] = typer.Option(None, '--objectives', '-o'),
    openai_api_key: str = typer.Option(envvar='OPENAI_API_KEY'),
    openai_model: str = typer.Option(envvar='OPENAI_MODEL'),
):
    app.state.host = host
    app.state.port = port
    if not objectives:
        for objective in os.getenv('BLOCKAGI_OBJECTIVES', '').split(','):
            objective = objective.strip()
            if objective:
                objectives.append(objective)
    if not objectives:
        raise ValueError('No objectives specified')

    app.state.openai_api_key = openai_api_key
    app.state.openai_model = openai_model
    app.state.blockagi_state = BlockAGIState(
        agent_role=agent_role,
        status=Status(step='PlanChain', round=0),
        historical_steps=[],
        objectives=[Objective(topic=topic, expertise=0.)
                    for topic in objectives],
        findings=[],
        resources=[],
        llm_logs=[],
        narratives=[],
    )
    uvicorn.run(app, host=host, port=port)


if __name__ == '__main__':
    dotenv.load_dotenv()
    typer.run(main)
