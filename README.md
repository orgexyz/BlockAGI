# 🤖📦 BlockAGI

BlockAGI is an open-source research agent built with [Python](https://www.python.org/), utilizing the capabilities of [LangChain](https://github.com/hwchase17/langchain) and [OpenAI](https://openai.com/). Taking inspiration from [BabyAGI](https://github.com/yoheinakajima/babyagi) and [AutoGPT](https://github.com/Significant-Gravitas/Auto-GPT), BlockAGI conducts iterative, domain-specific research, primarily focused on cryptocurrency but customizable to other domains. It outputs detailed narrative reports to showcase its findings. The progress of the AI agent's work is presented interactively through a user-friendly web interface, allowing users to watch the progress in real-time.

## Installation

```sh
poetry install
poetry run playwright install
```

## Running

Copy `.env.example` to `.env` and edit `OPENAI_API_KEY` and run `main.py` with poetry.

```sh
cp .env.example .env
# edit OPENAI_API_KEY in .env

poetry run python main.py
```
