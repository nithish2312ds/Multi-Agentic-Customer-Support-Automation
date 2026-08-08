from langgraph.graph import StateGraph, START, END

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from state import SupportState
from memory import init_db, save_memory
from agents import (
    classify_intent,
    retrieve_context_node,
    sales_agent,
    technical_agent,
    billing_agent,
    account_agent,
    memory_agent,
    approval_check,
    human_review,
    supervisor_agent,
    route_query,
    route_approval
)

console = Console()

# -----------------------------------
# Initialize Database
# -----------------------------------
init_db()

# -----------------------------------
# Build Graph
# -----------------------------------
builder = StateGraph(SupportState)

builder.add_node("classifier", classify_intent)
builder.add_node("retrieve", retrieve_context_node)

builder.add_node("sales", sales_agent)
builder.add_node("technical", technical_agent)
builder.add_node("billing", billing_agent)
builder.add_node("account", account_agent)

builder.add_node("memory", memory_agent)

builder.add_node("approval", approval_check)
builder.add_node("human", human_review)

builder.add_node("supervisor", supervisor_agent)

builder.add_node("save", save_memory)

# -----------------------------------
# Graph Flow
# -----------------------------------
builder.add_edge(START, "classifier")

builder.add_conditional_edges(
    "classifier",
    route_query,
    {
        "sales": "retrieve",
        "technical": "retrieve",
        "billing": "retrieve",
        "account": "retrieve",
        "memory": "memory"
    }
)

builder.add_conditional_edges(
    "retrieve",
    lambda state: state["issue_type"].lower(),
    {
        "sales": "sales",
        "technical": "technical",
        "billing": "billing",
        "account": "account"
    }
)

builder.add_edge("sales", "approval")
builder.add_edge("technical", "approval")
builder.add_edge("billing", "approval")
builder.add_edge("account", "approval")

builder.add_conditional_edges(
    "approval",
    route_approval,
    {
        "human": "human",
        "supervisor": "supervisor"
    }
)

builder.add_edge("human", "supervisor")

builder.add_edge("supervisor", "save")

builder.add_edge("save", END)

builder.add_edge("memory", END)

graph = builder.compile()


# -----------------------------------
# Rich Display Helper
# -----------------------------------
def show_workflow(result):

    table = Table(title="Workflow Summary")

    table.add_column("Field", style="cyan")
    table.add_column("Value", style="green")

    table.add_row(
        "Intent",
        str(result.get("issue_type", ""))
    )

    table.add_row(
        "Department",
        str(result.get("department", ""))
    )

    table.add_row(
        "Approval Required",
        str(result.get("approval_required", False))
    )

    table.add_row(
        "Approval Status",
        str(result.get("approval_status", "N/A"))
    )

    console.print(table)


# -----------------------------------
# Main Loop
# -----------------------------------
console.print(
    Panel.fit(
        "AI-Powered Customer Support Automation System",
        title="LangGraph Project",
        border_style="green"
    )
)

while True:

    query = console.input(
        "\n[bold cyan]Customer Query[/bold cyan] (type 'exit' to quit): "
    )

    if query.lower() == "exit":
        break

    result = graph.invoke(
        {
            "customer_id": "David",
            "query": query
        }
    )

    show_workflow(result)

    if result.get("retrieved_context"):
        console.print(
            Panel(
                result["retrieved_context"],
                title="Retrieved Context (RAG)",
                border_style="blue"
            )
        )

    console.print(
        Panel(
            result.get(
                "final_response",
                "No response generated."
            ),
            title="Final Response",
            border_style="green"
        )
    )