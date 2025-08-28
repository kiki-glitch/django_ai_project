from langchain_openai import ChatOpenAI
from langgraph_supervisor import create_supervisor
from ai import agents
from ai.llms import get_groq_model
import uuid

def get_supervisor(config=None, checkpointer=None):

    if config is None:
        config = {
            "configurable": {
                "user_id": "3",  # You can inject a real user ID here
                "thread_id": str(uuid.uuid4())
            }
        }
    try:
        model = get_groq_model()
        document_agent = agents.get_document_agent(config=config, checkpointer=checkpointer)
        movie_discovery_agent = agents.get_movie_discovery_agent(config=config, checkpointer=checkpointer)

        return create_supervisor(
            agents=[document_agent, movie_discovery_agent],
            model=model,
            prompt=(
                "You are a supervisor that routes user requests to the appropriate specialized agent.\n\n"
                "Available agents:\n"
                "• document_agent - handles ALL document operations (list, create, read, update, delete, search)\n"
                "• movie_discovery_agent - handles movie searches and information retrieval\n\n"
                
                "ROUTING DECISIONS:\n"
                "• Document requests ('list my documents', 'create document', 'update document') → document_agent\n"
                "• Movie requests ('search movies', 'movie details') → movie_discovery_agent\n"
                "• Movie + Document requests ('create document about movie X') → coordinate both agents\n\n"
                
                "CRITICAL RULES:\n"
                "1. You do NOT have access to any tools yourself\n"
                "2. You MUST route all requests to the appropriate agent\n"
                "3. NEVER attempt to call list_documents, create_document, or any other tool directly\n"
                "4. Your only job is to decide which agent should handle the request\n"
                "5. For multi-step workflows, coordinate between agents in sequence\n\n"
                
                "Always respond by routing to an agent - never try to answer directly or call tools."
            ),
            include_agent_name="inline",  # ✅ Helps understand which agent responded
            add_handoff_messages=True  # ✅ Helps with debugging transitions
        ).compile(name="main_supervisor",checkpointer=checkpointer)

    except Exception as e:
        print(f"Error creating supervisor: {e}")
        raise