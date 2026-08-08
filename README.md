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

<img width="656" height="340" alt="Agent Routing - Query 2" src="https://github.com/user-attachments/assets/09fa381b-2947-4ac0-a5a4-858b9c2d157b" />


### Screenshot 2

<img width="1356" height="782" alt="Human-in-the-loop - Query 4" src="https://github.com/user-attachments/assets/c673e71a-4c64-4275-9b0a-ce59e9424e91" />

### Screenshot 3

<img width="1371" height="796" alt="Query-1" src="https://github.com/user-attachments/assets/cb368727-44f1-46cd-a33c-a5feb4488da4" />


### Screenshot 4

<img width="1374" height="411" alt="Query-3-Part 1" src="https://github.com/user-attachments/assets/73c30f15-701e-4d6f-ad91-c9a4f6d0740e" />
<img width="1371" height="518" alt="Query-3-Part 2" src="https://github.com/user-attachments/assets/4703b710-b946-44ae-bb29-05450aa55b1b" />


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


