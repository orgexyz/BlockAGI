# 🛠️ BlockAGI Parameters Guide

Parameters can be passed to BlockAGI via environment variables or the `.env` file. This guide will help you understand each parameter and how to choose the right values for your needs.

## 🎯 How to Choose the Right Parameters

### LLM Model (`OPENAI_MODEL`)

While the default setting works well with `gpt-3.5-turbo-16k` most of the time, you can change the model to suit your needs:

- `gpt-3.5-turbo` works as well, but you may need to reduce the context size by limiting the length of the tools' output.
- `gpt-4` works much better, but it is also much more expensive to run.

### Agent Role (`BLOCKAGI_AGENT_ROLE`)

The default is `BLOCKAGI_AGENT_ROLE=BlockAGI, a Crypto Research Assistant`. Choose the role that fits your research objectives overall to yield the best result. Keep it concise and direct.

### Research Objectives (`BLOCKAGI_OBJECTIVE_<#N>`)

Be specific and concise. Avoid using entity names that can be confusing. Adding a domain name would also help point the agent to the right thing you need it to research. Asking specific questions also yields better results. For example, "Apple's new tech announcement in 2023" is better than "Apple's exciting news".

### Number of Iterations (`BLOCKAGI_ITERATION_COUNT`)

Normally, 5-10 iterations should yield a good result, but this may vary from topic to topic.

## 🙏 We Need Your Contributions

This page needs your help in evaluating and experimenting with appropriate parameters for various use cases. Share your findings to help us learn more about what works for you!
