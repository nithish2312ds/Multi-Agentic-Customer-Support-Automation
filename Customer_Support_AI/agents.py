from langchain_ollama import ChatOllama
from memory import recall_previous_issue
from rag import retrieve_context

# Ollama LLM
llm = ChatOllama(
    model="qwen2.5:3b",
    temperature=0
)


# -----------------------------
# Intent Classification
# -----------------------------
def classify_intent(state):

    prompt = f"""
You are a customer support intent classifier.

Classify the customer query into EXACTLY one of these categories:
- Sales
- Technical
- Billing
- Account
- Memory

Rules:
- If the customer is asking about their previous query, issue, problem, or conversation history -> Memory
- If the customer asks about pricing, plans, subscriptions, or product information -> Sales
- If the customer asks about errors, crashes, login problems, installation, or configuration -> Technical
- If the customer asks about invoices, payments, refunds, or billing issues -> Billing
- If the customer asks about password reset, profile updates, account activation or deactivation -> Account

Query:
{state["query"]}

Return ONLY the category name. No explanation. No punctuation.
"""

    result = llm.invoke(prompt)
    issue_type = result.content.strip()

    # Keyword override — safety net in case LLM misclassifies
    memory_triggers = [
        "previous", "last issue", "before",
        "history", "earlier", "last time",
        "past issue", "what did i", "what was my"
    ]
    if any(trigger in state["query"].lower() for trigger in memory_triggers):
        issue_type = "Memory"

    state["issue_type"] = issue_type
    return state


# -----------------------------
# Retrieve Context
# -----------------------------
def retrieve_context_node(state):

    doc = retrieve_context(state["query"])

    state["retrieved_context"] = doc["content"]
    state["source_document"] = doc["source"]

    return state


# -----------------------------
# Sales Agent
# -----------------------------
def sales_agent(state):

    state["department"] = "Sales"

    state["draft_response"] = f"""
ABC Technologies Support

Department: Sales

Response:
Sales Department Response

Source: {state["source_document"]}

{state["retrieved_context"]}

Thank you for contacting us.
"""

    return state


# -----------------------------
# Technical Agent
# -----------------------------
def technical_agent(state):

    state["department"] = "Technical Support"

    prompt = f"""
You are a Technical Support Engineer at ABC Technologies.

Customer Query:
{state["query"]}

Retrieved Context:
{state["retrieved_context"]}

Answer the customer professionally and helpfully.
Do NOT use any placeholders like [Your Name] or [Your Contact Information].
Use this exact sign-off at the end:

Best regards,
ABC Technologies Technical Support Team
Email: support@abctechnologies.com
Phone: +1-800-111-2222
"""

    result = llm.invoke(prompt)
    state["draft_response"] = result.content

    return state


# -----------------------------
# Billing Agent
# -----------------------------
def billing_agent(state):

    state["department"] = "Billing"

    prompt = f"""
You are a Billing Support Specialist at ABC Technologies.

Customer Query:
{state["query"]}

Retrieved Context:
{state["retrieved_context"]}

Answer the customer professionally and helpfully.
Do NOT use any placeholders like [Your Name] or [Your Contact Information].
Use this exact sign-off at the end:

Best regards,
ABC Technologies Billing Support Team
Email: billing@abctechnologies.com
Phone: +1-800-222-3333
"""

    result = llm.invoke(prompt)
    state["draft_response"] = result.content

    return state


# -----------------------------
# Account Agent
# -----------------------------
def account_agent(state):

    state["department"] = "Account"

    prompt = f"""
You are an Account Support Specialist at ABC Technologies.

Customer Query:
{state["query"]}

Retrieved Context:
{state["retrieved_context"]}

Answer the customer professionally and helpfully.
Do NOT use any placeholders like [Your Name] or [Your Contact Information].
Use this exact sign-off at the end:

Best regards,
ABC Technologies Account Support Team
Email: accounts@abctechnologies.com
Phone: +1-800-333-4444
"""

    result = llm.invoke(prompt)
    state["draft_response"] = result.content

    return state


# -----------------------------
# Memory Agent
# -----------------------------
def memory_agent(state):

    previous_issue = recall_previous_issue(state["customer_id"])

    if previous_issue:
        state["final_response"] = (
            f"Your previous support issue was: {previous_issue}"
        )
    else:
        state["final_response"] = (
            "No previous support history was found for your account."
        )

    return state


# -----------------------------
# Human Approval Check
# -----------------------------
def approval_check(state):

    query = state["query"].lower()

    risky_keywords = [
        "refund",
        "cancel subscription",
        "close account",
        "account closure",
        "compensation",
        "management"
    ]

    state["approval_required"] = any(
        keyword in query for keyword in risky_keywords
    )

    return state


# -----------------------------
# Human Review
# -----------------------------
def human_review(state):

    print("\n==============================")
    print("HUMAN APPROVAL REQUIRED")
    print("==============================")
    print("\nDraft Response:\n")
    print(state["draft_response"])

    approval = input("\nApprove response? (yes/no): ")
    state["approval_status"] = approval

    return state


# -----------------------------
# Supervisor Agent
# -----------------------------
def supervisor_agent(state):

    print("\n==============================")
    print("SUPERVISOR: Validating response...")
    print("==============================")

    prompt = f"""
You are a Quality Assurance Supervisor at ABC Technologies.

Your job is to review a draft customer support response and improve it before it is sent to the customer.

Customer Query:
{state["query"]}

Department: {state.get("department", "Support")}

Draft Response:
{state["draft_response"]}

Review the draft response and check ALL of the following:
1. Is the response polite and professional in tone?
2. Does it directly and fully address the customer query?
3. Are there any placeholder texts like [Your Name] or [Your Contact Information]? If yes, remove or replace them with real details.
4. Is the response clear, concise, and easy to understand?
5. Does it have a proper greeting and a complete sign-off?

If the draft is already good, return it exactly as-is.
If it needs any improvement, return the improved version.

Return ONLY the final response text. No commentary, no notes, no labels, no explanations.
"""

    result = llm.invoke(prompt)
    state["final_response"] = result.content.strip()

    print("SUPERVISOR: Response validated and approved.")

    return state


# -----------------------------
# Routing Functions
# -----------------------------
def route_query(state):

    issue = state["issue_type"]

    mapping = {
        "Sales": "sales",
        "Technical": "technical",
        "Billing": "billing",
        "Account": "account",
        "Memory": "memory"
    }

    return mapping.get(issue, "technical")


def route_approval(state):

    if state["approval_required"]:
        return "human"

    return "supervisor"