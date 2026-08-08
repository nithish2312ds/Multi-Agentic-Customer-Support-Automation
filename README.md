# Multi-Agent Customer Support Automation

A production-inspired AI customer support system built with [LangGraph](https://github.com/langchain-ai/langgraph), RAG, SQLite conversation memory, specialized agents, and human-in-the-loop approval workflows.

## Overview

This project implements a supervisor-based multi-agent architecture for automating customer support workflows.

Routes customer requests to specialized billing, technical support, and escalation agents.

Uses RAG to ground responses in a local knowledge base.

Uses SQLite for persistent conversation memory.

Includes human-in-the-loop approval gates for sensitive actions.

## Tech Stack

* [Python](https://www.python.org/)
* [LangGraph](https://github.com/langchain-ai/langgraph)
* [RAG](https://python.langchain.com/docs/concepts/retrieval/)
* [SQLite](https://www.sqlite.org/)
* [Qwen](https://huggingface.co/Qwen)
* [LangChain](https://www.langchain.com/)
* LLM
* Human-in-the-Loop

## Screenshots

### Screenshot 1

![Screenshot 1](screenshots/screenshot1.png)

### Screenshot 2

![Screenshot 2](screenshots/screenshot2.png)

### Screenshot 3

![Screenshot 3](screenshots/screenshot3.png)

### Screenshot 4

![Screenshot 4](screenshots/screenshot4.png)

## Workflow

The system follows a supervisor-based multi-agent workflow:

```text
                    Customer Request
                           │
                           ▼
                    ┌──────────────┐
                    │  Supervisor  │
                    │     Agent    │
                    └──────┬───────┘
                           │
          ┌────────────────┼────────────────┐
          ▼                ▼                ▼
    ┌───────────┐    ┌───────────┐    ┌────────────┐
    │  Billing  │    │ Technical │    │ Escalation │
    │   Agent   │    │  Support  │    │   Agent    │
    └───────────┘    └───────────┘    └────────────┘
          │                │                │
          └────────────────┼────────────────┘
                           ▼
                    ┌──────────────┐
                    │     RAG      │
                    │  Knowledge   │
                    │     Base     │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │ Human Review │
                    │  if required │
                    └──────┬───────┘
                           │
                           ▼
                       Response
```

## Steps

1. Download [Qwen 2.5 3B](https://huggingface.co/Qwen/Qwen2.5-3B).

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Run the application:

```bash
python main.py
```

## Architecture

The application uses a supervisor-based architecture where a central supervisor determines which specialized agent should handle each customer request.

### Specialized Agents

* **Billing Agent** — Handles billing and payment-related queries.
* **Technical Support Agent** — Handles technical issues and troubleshooting.
* **Escalation Agent** — Handles requests requiring human intervention.

### RAG

The retrieval-augmented generation pipeline retrieves relevant information from the local knowledge base before generating a response.

This helps reduce hallucinations and keeps responses grounded in the available support documentation.

### Conversation Memory

SQLite is used to maintain persistent conversation state, allowing the system to retain relevant information across interactions.

### Human-in-the-Loop

Sensitive operations can be paused for human approval before the system proceeds.

This provides an additional safety layer for actions that should not be performed autonomously.

## Project Structure

```text
.
├── main.py
├── requirements.txt
├── README.md
├── database/
├── knowledge_base/
├── agents/
├── rag/
└── screenshots/
```

## Future Improvements

* Add additional specialized support agents
* Improve retrieval quality
* Add evaluation and observability
* Add authentication and authorization
* Deploy the application as an API
* Add a web-based customer support interface
* Add automated agent evaluation

## License

This project is for educational and experimental purposes.
