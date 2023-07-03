# 🎨 BlockAGI Design Choices & Inspirations

BlockAGI is built with a set of distinct design choices that set it apart from other tools. These choices prioritize usability, believing that a good user experience is equally, if not more, important than the underlying technology.

## 🖥️ User-Centric Design

BlockAGI is designed with the user in mind. The WebUI is not just a secondary feature, but a core part of the system. It works hand-in-hand with the Python engine to create a good user experience, presenting the right information to the user in the right context.

## 📚 No External Datastore

BlockAGI does not use any external VectorDatastore. This is because most of the resources found within a BlockAGI iteration are immediately put to use in narrating the research piece. Adding another layer of long-term memory datastore did not yield additional accuracies or performance benefits.

## 🔄 ReAct Inspired

BlockAGI's iterative process is inspired by the ReAct framework (https://arxiv.org/abs/2210.03629). In every iteration, BlockAGI goes through a self-evaluation which guides its own objectives in the next iteration as well as generating a remark to improve itself in the next planning stage.
