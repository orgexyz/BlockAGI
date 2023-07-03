# 🏗️ BlockAGI Architecture

BlockAGI is comprised of multiple components, each with specific purposes which we'll outline below.

## 🧠 Python Engine

The Python Engine is the brain of BlockAGI, powered by LangChain with a few modifications in its convention. The Engine utilizes a short-term memory called Resource Pool, which is shared across multiple tools and the agent itself to keep track of information.

## 🖥️ Web UI

Another key component that makes BlockAGI a powerful and practical tool is its WebUI. Currently, the sole purpose of the WebUI is to display the current status and results from BlockAGI's iterations. This makes it substantially easier for the users to inspect the agent's behaviors, including all its decisions, tools utilized, and more.

## 🔄 How BlockAGI Works

BlockAGI works in a series of steps 🅿🆁🆄🅽🅴, each with specific inputs and outputs. The steps are as follows:

### Step 1) 🅿 Plan

The Plan step takes the user's objectives and its own evaluation (findings) from the previous iteration and produces tasks to be executed. Depending on the expertise level of each objective, the agent may choose to utilize different tools to scope for broader/narrower researches.

### Step 2) 🆁 Research

The Research step executes tasks from the Plan step and passes on the results. Normally this step doesn't utilize LLM unless the tools require it.

### Step 3) 🆄 Update Resources

This step updates the resource pools (the short-term memory), which tools can add new links and set websites visited. This step normally happens after tools are executed, so it's not part of the "chain" of execution.

### Step 4) 🅽 Narrate

The Narrate step

takes the research results and writes a comprehensive report. Due to the context limit of LLM models, the research results are packed into chunks. Each chunk then gets passed into LLM alongside the latest version of the narrative, in order to produce an improved version. Once all results are taken into account, this step then returns a markdown of the research piece.

### Step 5) 🅴 Evaluate

The Evaluate step allows the agent to self-evaluate how well it understands the objecting topics and come up with a few things: the agent's expertise in each of its given objectives, generated intermediate objectives that help it breakdown the main objectives into smaller research goals, and a remark to its next iteration on what to improve and what to keep doing.

## 📚 Schema Reference

Here are the main classes used in BlockAGI:

```python
class Objective:
    topic: str
    expertise: float

class Resource:
    url: str
    description: Optional[str]
    visited: Optional[bool]
    content: Optional[str] = None

class ResearchTask:
    tool: str
    args: Dict[str, Any]
    reasoning: str

class ResearchResult(ResearchTask):
    result: Any
    citation: Optional[str] = None

class Narrative:
    markdown: str

class Findings:
    narrative: str
    remark: str
    generated_objectives: List[Objective]
```

This architecture allows BlockAGI to be flexible and adaptable, making it a powerful tool for a wide range of research tasks.
