from langgraph.prebuilt import create_react_agent
from ai.llms import get_groq_model
from ai.tools.documents import (
    make_list_documents_tool,
    make_get_document_tool,
    make_create_document_tool,
    make_update_document_tool,
    make_delete_document_tool,
    make_search_documents_tool
)
from ai.tools.movie_discovery import (
    make_search_movies_tool,
    make_movie_detail_tool
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
        name="document_agent",
        model=model,
        tools=document_tools,
        prompt=(
            "You are a helpful assistant responsible for managing user documents. "
            "You must use the tools provided to list, fetch, create, update, or delete documents. "
            "NEVER guess, fabricate, or assume changes were made — always call a tool when the user asks for document actions. "
            "If the user wants to modify, fix, rename, correct, or revise a document, you MUST use the update_document tool. "
            "Respond only after successfully calling the tool."),
        checkpointer=checkpointer
    )
    return agent

def get_movie_discovery_agent(config, checkpointer=None):
    model = get_groq_model()

    # Dynamically inject config into each tool
    movie_tools = [
        make_search_movies_tool(config),
        make_movie_detail_tool(config)
    ]

    agent = create_react_agent(
        name="movie_discovery_agent",
        model=model,
        tools=movie_tools,
        prompt=(
            "You are a helpful assistant that assists users in discovering and learning about movies. "
            "You may search for movies and retrieve detailed information using your tools. "
            "Always use tools to fetch or suggest movie content; never guess movie details."),
        checkpointer=checkpointer
    )
    return agent
