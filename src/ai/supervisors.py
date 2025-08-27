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

    model = get_groq_model()

    doc_agent = agents.get_document_agent(config=config, checkpointer=checkpointer)
    movie_agent = agents.get_movie_discovery_agent(config=config, checkpointer=checkpointer)

    return create_supervisor(
        agents=[doc_agent, movie_agent],
        model=model,
        prompt=(
            "You manage a document management assistant and a "
            "movie discovery assistant. Assign work to them."
        ),
        include_agent_name="inline",  # ✅ Helps understand which agent responded
        add_handoff_messages=True  # ✅ Helps with debugging transitions
    ).compile(name="main_supervisor",checkpointer=checkpointer)
