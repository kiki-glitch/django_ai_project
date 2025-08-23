from langgraph.prebuilt import create_react_agent
from ai.llms import get_groq_model
from ai.tools import (
    make_list_documents_tool,
    make_get_document_tool,
    make_create_document_tool,
    make_update_document_tool,
    make_delete_document_tool,
    make_search_documents_tool
)

def get_document_agent(config, checkpointer=None):
    model = get_groq_model()

    # Dynamically inject config into each tool
    document_tools = [
        make_list_documents_tool(config),
        make_get_document_tool(config),
        make_create_document_tool(config),
        make_update_document_tool(config),
        make_delete_document_tool(config),
        make_search_documents_tool(config),
    ]

    agent = create_react_agent(
        model=model,
        tools=document_tools,
        prompt=("You are a helpful assistant for managing user documents. "
            "Only use document tools when the user asks to create, update, delete, or view documents. "
            "Do not create documents on your own unless the user asks explicitly."),
        checkpointer=checkpointer
    )
    return agent
