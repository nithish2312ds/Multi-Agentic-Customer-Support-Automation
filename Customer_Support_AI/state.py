from typing import TypedDict

class SupportState(TypedDict):
    customer_id: str
    query: str
    issue_type: str
    department: str
    retrieved_context: str
    approval_required: bool
    approval_status: str
    source_document: str
    draft_response: str
    final_response: str
