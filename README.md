# 🤖📦 BlockAGI

BlockAGI is an open-source research agent built with Python3, utilizing the capabilities of [LangChain](https://github.com/hwchase17/langchain) and [OpenAI](https://openai.com/). BlockAGI conducts iterative, domain-specific research, primarily focused on cryptocurrency but customizable to other domains. It outputs detailed narrative reports to showcase its findings. The progress of the AI agent's work is presented interactively through a user-friendly web interface, allowing users to watch the progress in real-time.

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

## License

BlockAGI is open-source software licensed under the Apache License 2.0. This license allows use, modification, and distribution of the software. For complete details, please see the [LICENSE](LICENSE) and [NOTICE](NOTICE) files in this repository.

## Acknowledgements

We would like to express our gratitude to the following projects and communities for their inspiring work and valuable contributions:
- [LangChain](https://github.com/hwchase17/langchain)
- [OpenAI](https://openai.com/)
- [BabyAGI](https://github.com/yoheinakajima/babyagi)
- [AutoGPT](https://github.com/Significant-Gravitas/Auto-GPT)