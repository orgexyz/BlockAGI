# 👋 Contributing to BlockAGI

Welcome to the BlockAGI contribution guide! This document will provide a rough code overview and highlight the areas where you can contribute. Any and all contributions are welcome, whether you're improving existing features or introducing new ones.

## 🌱 Contributing Aspects

There are several areas in BlockAGI where your contributions would be highly valued:

1. **Bug Fixes, Typos, and Documentation**: Continual improvement of our codebase and documentation is vital. This can range from fixing bugs and correcting typos to enhancing our existing documentation for improved clarity and comprehensiveness.

2. **Improve OpenAI Prompts**: OpenAI prompts play a critical role in our system. Enhancements to these prompts, such as making them more accurate or efficient, could significantly boost the overall performance of BlockAGI.

3. **Add More Functionalities**: You could further extend the capabilities of BlockAGI by adding new tools or features, thereby improving the system's functionality and performance.

4. **Produce Benchmarks**: Production of benchmarks would be an invaluable contribution, as it helps in gauging the efficiency and effectiveness of our system, providing insights for potential improvements.

5. **Provide Testimony**: Your feedback is important to us. We're gathering testimonies and feedback for our initiative called `awesome-blockagi`. Sharing your experiences would contribute greatly to this initiative.

## 💡 Feature Ideas

If you're not sure where to start, here are a few initial ideas you can consider working on:

1. **Make BlockAGI Stop When Expertise is Sufficient**: Developing a mechanism that makes BlockAGI stop when it has gained enough expertise could enhance efficiency and performance.

2. **Streaming Over WebSocket**: Implementing WebSocket streaming could significantly improve real-time communication in the system.

3. **Pause/Resume Agents Using Web Interface**: A feature that allows users to pause and resume agents directly through the web interface could improve user interaction and system control.

4. **Edit Parameters/Program Environments on the Web Interface**: A feature to edit parameters or program environments directly on the web interface could provide users with more control and flexibility over the system.

## 📥 BlockAGI Code Structure Overview

BlockAGI is primarily divided into two main parts: the frontend and the backend.

### Frontend

The frontend is an essential aspect of BlockAGI, focusing on user interaction and visual output. If you're interested in these areas, this is where you can contribute significantly. The frontend code is written in TypeScript, leveraging the React framework for its development. The primary directory for the frontend code is `/ui`, with the core file being `/ui/app/page.tsx`.

### Backend

The backend of BlockAGI is equally important, making extensive use of the Langchain framework. It exposes its functionalities to the frontend via the FastAPI framework. Each step in the backend is implemented as a chain object in Langchain, creating a robust and flexible backend structure.
