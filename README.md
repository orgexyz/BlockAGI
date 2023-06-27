# 🤖📦 BlockAGI

BlockAGI is an open-source research agent built with Python3, utilizing the capabilities of [LangChain](https://github.com/hwchase17/langchain) and [OpenAI](https://openai.com/). BlockAGI conducts iterative, domain-specific research, primarily focused on cryptocurrency but customizable to other domains. It outputs detailed narrative reports to showcase its findings. The progress of the AI agent's work is presented interactively through a user-friendly web interface, allowing users to watch the progress in real-time.

## Installation

To get started with BlockAGI, please follow these steps:
1. Install [Poetry](https://python-poetry.org/), a dependency management tool for Python.
2. Clone the BlockAGI repository to your local machine.
3. Navigate to the project directory and run the following command to install the required dependencies:
   ```bash
   poetry install
   ```

4. Next, install the [Playwright](https://github.com/microsoft/playwright) dependencies by running the following command:
   ```bash
   poetry run playwright install
   ```

## Usage

To start using BlockAGI, please follow these steps:
1. Copy the `.env.example` file and rename it to `.env`.
2. Open the `.env` file and add your OpenAI API key. You can also modify other configurations as needed, such as the research domain or any additional settings.
3. Run the following command to start BlockAGI:
   ```
   poetry run python main.py
   ```

   This will initiate BlockAGI and also spin up a web application, allowing you to monitor the progress and interact with the research agent.

4. Watch the progress on BlockAGI via the web interface.

## License

BlockAGI is open-source software licensed under the Apache License 2.0. This license allows use, modification, and distribution of the software. For complete details, please see the [LICENSE](LICENSE) and [NOTICE](NOTICE) files in this repository.

## Acknowledgements

We would like to express our gratitude to the following projects and communities for their inspiring work and valuable contributions:
- [LangChain](https://github.com/hwchase17/langchain)
- [OpenAI](https://openai.com/)
- [BabyAGI](https://github.com/yoheinakajima/babyagi)
- [AutoGPT](https://github.com/Significant-Gravitas/Auto-GPT)