from documents.models import Document
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool

@tool
def list_documents(config:RunnableConfig):
    """
    Get user's documents
    """
    print(config)
    metadata = config.get('metadata') or config.get('configurable')
    user_id = metadata.get('user_id')
    qs = Document.objects.filter(owner_id=user_id ,active=True)
    response_data = []
    for obj in qs:
        response_data.append(
            {
                "id":obj.id,
                "title":obj.title
            }
        )
    return response_data


@tool
def get_document(document_id:int, config:RunnableConfig):
    """
    Get details of a document of current user
    """
    metadata = config.get('metadata') or config.get('configurable')
    user_id = metadata.get('user_id')
    if user_id is None:
        raise Exception("Invalid request for user.")
    try:
        qs = Document.objects.get(owner_id=user_id,id=document_id, active=True)
    except Document.DoesNotExist:
        raise Exception("Document not found, try again")
    except:
        raise Exception("Invalid request for a document detail, try again")
    response_data = {
        "id": qs.id,
        "title": qs.title
    }
    return response_data

