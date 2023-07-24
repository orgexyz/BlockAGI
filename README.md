[![GitHub Repo stars](https://img.shields.io/github/stars/blockpipe/blockagi?style=social)](https://github.com/blockpipe/blockagi/stargazers)
[![Twitter Follow](https://img.shields.io/twitter/follow/BlockAGI?style=social)](https://twitter.com/BlockAGI)

<img width="600" alt="banner" src="https://github.com/blockpipe/BlockAGI/assets/891585/4ea315e2-b496-4cfb-a81a-560a1763bf15">

**BlockAGI** is an open-source research agent built with Python3, utilizing the capabilities of [LangChain](https://github.com/hwchase17/langchain) and [OpenAI](https://openai.com/). BlockAGI conducts iterative, domain-specific research, primarily focused on cryptocurrency but customizable to other domains. It outputs detailed narrative reports to showcase its findings. The progress of the AI agent's work is presented interactively through a user-friendly web interface, allowing users to watch the progress in real-time.

> 🤖 Initially designed to answer crypto research topics (hence the "Block" in BlockAGI), it has proven useful for a wide variety of other use cases.

## 🔎 Quick Preview

![blockagi-preview-2](https://github.com/blockpipe/BlockAGI/assets/891585/bfd05611-9017-4d1f-844c-e6feae737973)

## 🎯 Features

- **📚 Automated Research**: Just provide the topics, and let BlockAGI do the research.
- **🔍 Comprehensive**: BlockAGI can search, gather, refine, and evaluate information on its own.
- **🔄 Live Data**: BlockAGI can access real-time data from the internet or your own database.
- **🌐 WebUI**: Equipped with user-friendly interface, all in one [`tsx`](/ui/app/page.tsx) file.
- **💯 100% Hackable**: The code, based on LangChain, is concise and easy to modify to suit your needs.
- **🔐 Privacy Focused**: Your report stays with you and the LLM provider you trust.
- **🚀 Inspired by the Best**: BlockAGI builds upon the work of [BabyAGI](https://github.com/yoheinakajima/babyagi) and [AutoGPT](https://github.com/Significant-Gravitas/Auto-GPT) to create a self-improving agent.


## 💡 Differences from AutoGPT

- **⚡ Efficiency**: BlockAGI has been tested to work well with `gpt-3.5-turbo-16k`, which is substantially cheaper than `gpt-4` on most research tasks.
- **🖥️ Interactive Web UI**: BlockAGI features a Web UI that displays the agent's decision-making process, execution progress, and the latest research results. This allows for a more interactive and user-friendly experience.
- **🎯 Focused Functionality**: BlockAGI is designed with a single goal in mind - to assist users in their research topics. It's not about doing everything, but doing one thing really well.
- **🔧 Simplified Setup**: BlockAGI does not require file reading/writing, so there's no need for Docker/sandboxing. This makes the setup process simpler and more straightforward.
- **📦 No External Datastore**: BlockAGI does not require an external vector datastore to work, reducing the complexity and resource requirements.

## 🛠️ Tech Stack

- Backend: [Python](https://www.python.org/downloads/) and [LangChain](https://python.langchain.com/)
- Frontend: [Next.js](https://nextjs.org/) and [Tailwind](https://tailwindcss.com/)

## 🤝 Sponsors and Contributors

We currently don't take any monetary donations! However, every issue filed and PR are extremely important to us. Here is the roster of contributors and supporters of the project.

<a href="https://blockpipe.io"><img width="200" alt="blockpipe" src="https://github.com/blockpipe/BlockAGI/assets/891585/c595fd73-4a7e-4401-8312-1d7ea79b1bf4"></a>

<br />

<a href="https://github.com/smiled0g"><img src="https://avatars.githubusercontent.com/smiled0g?v=4" width="50px" alt="smiled0g" /></a>&nbsp;&nbsp;<a href="https://github.com/sorawit"><img src="https://avatars.githubusercontent.com/sorawit?v=4" width="50px" alt="sorawit" /></a>&nbsp;&nbsp;<a href="https://github.com/endolith"><img src="https://avatars.githubusercontent.com/endolith?v=4" width="50px" alt="endolith" /></a>&nbsp;&nbsp;

## 📚 Documentation

- [Installation and Basic Usage](#-Installation)
- [Parameters and Their Recommended Value](/docs/PARAMETERS.md)
- [BlockAGI's Architecture](/docs/ARCHITECTURE.md)
- [Design Choices](/docs/DESIGN_CHOICES.md)
- [Building Custom Tools](/docs/BUILDING_TOOLS.md)
- [Hacking Your Own Research Assitant (Advanced)](/docs/ADVANCED_HACKING.md)
- [Contributing to BlockAGI](/CONTRIBUTING.md)

## 🔋 Installation

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

## 🎮 Basic Usage

To start using BlockAGI, please follow these steps:

1. Copy the `.env.example` file and rename it to `.env`.
2. Open the `.env` file and add your OpenAI API key. You can also modify other configurations as needed, such as the research domain or any additional settings.
3. Run the following command to start BlockAGI:

   ```
   poetry run python main.py
   ```

   This will initiate BlockAGI and also spin up a web application, allowing you to monitor the progress and interact with the research agent.

4. Watch the progress on BlockAGI via the web interface.

## 📥 Contribution and Feedback

Contributions, feedback, and suggestions are highly encouraged and appreciated! You can contribute to BlockAGI in the following ways:

- Fork the repository and make modifications in your own branch. Then, submit a pull request ([PR](https://github.com/blockpipe/BlockAGI/pulls)) with your changes.
- Submit issues ([GitHub Issues](https://github.com/blockpipe/BlockAGI/issues)) to report bugs, suggest new features, or ask questions.
- Join our [Discord](https://discord.gg/K3TWumAtZV) community and share your experiences, ideas, and improvements. We believe that collaborative development is essential for the growth of BlockAGI.

For BlockAGI code structure and contribution ideas, see [CONTRIBUTING.md](CONTRIBUTING.md).

## 📖 Citation

If you wish to cite BlockAGI in your research, we encourage the use of [CITATION.cff](CITATION.cff) provided for appropriate citation formatting. For more details on the citation file format, please visit the [Citation File Format website](https://citation-file-format.github.io).

## 📜 License

BlockAGI is open-source software licensed under the Apache License 2.0. This license allows use, modification, and distribution of the software. For complete details, please see the [LICENSE](LICENSE) and [NOTICE](NOTICE) files in this repository.

## 🙏 Acknowledgements

We would like to express our gratitude to the following projects and communities for their inspiring work and valuable contributions:

- [LangChain](https://github.com/hwchase17/langchain)
- [OpenAI](https://openai.com/)
- [BabyAGI](https://github.com/yoheinakajima/babyagi)
- [AutoGPT](https://github.com/Significant-Gravitas/Auto-GPT)
