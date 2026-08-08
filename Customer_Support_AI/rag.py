import os

documents = []

for filename in sorted(os.listdir("docs")):  # sorted for consistency
    path = os.path.join("docs", filename)
    with open(path, "r", encoding="utf-8") as f:
        documents.append({
            "source": filename.lower(),  # just filename, easier to match
            "content": f.read()
        })


def get_doc(keyword):
    for doc in documents:
        if keyword in doc["source"]:
            return doc
    return None


def retrieve_context(query):
    query = query.lower()

    # Sales / Pricing
    if any(w in query for w in ["price", "pricing", "plan", "subscription", "cost", "upgrade"]):
        return get_doc("pricing") or documents[0]

    # Technical
    elif any(w in query for w in ["crash", "upload", "error", "install", "login", "configuration", "bug", "issue", "slow"]):
        return get_doc("technical") or documents[0]

    # Billing
    elif any(w in query for w in ["refund", "invoice", "payment", "billing", "charge", "cancel"]):
        return get_doc("policy") or documents[0]

    # Account
    elif any(w in query for w in ["password", "reset", "profile", "account", "activation", "deactivation"]):
        return get_doc("faq") or documents[0]

    # Memory queries — return empty, no RAG needed
    elif any(w in query for w in ["previous", "last issue", "history", "earlier", "past issue", "before"]):
        return {"source": "none", "content": ""}

    # Safe fallback
    else:
        return {"source": "none", "content": "No relevant document found."}