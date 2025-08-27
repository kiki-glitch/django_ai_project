from documents.models import Document
from langchain_core.tools import Tool
from django.db.models import Q
from langchain_core.pydantic_v1 import BaseModel, Field

# Define schema using Pydantic
class ListDocumentsInput(BaseModel):
    limit: int = Field(default=5, description="Number of documents to return (max 25)")

def make_list_documents_tool(config):
    
    def _list_documents(limit: int = 5):
        """
        List the most recent LIMIT documents for the current user with maximum of 25.

        Arguments:
        limit: number of results
        """
        print("✅ [Tool] list_documents was called")
        if limit > 25:
            limit = 25

        user_id = config.get('configurable', {}).get('user_id')
        qs = Document.objects.filter(owner_id=user_id, active=True).order_by("-created_at")

        
        return [
            {"id": doc.id, "title": doc.title}
            for doc in qs[:limit]
        ]

    return Tool.from_function(
        name="list_documents",
        func=_list_documents,
        description="List up to 25 of the user's most recent documents.",
        args_schema=ListDocumentsInput
    )


def make_get_document_tool(config):
    def _get_document(document_id: int):
        print("✅ [Tool] get_documents was called")
        user_id = config.get('configurable', {}).get('user_id')

        try:
            doc = Document.objects.get(id=document_id, owner_id=user_id, active=True)
        except Document.DoesNotExist:
            raise Exception("Document not found or access denied.")

        return {
            "id": doc.id,
            "title": doc.title,
            "content": doc.content,
            "created_at": doc.created_at
        }

    return Tool.from_function(
        name="get_document",
        func=_get_document,
        description="Retrieve a specific document’s full details (title, content, date) by its ID. Use when the user asks to open or view a document."
    )


def make_create_document_tool(config):
    def _create_document(title: str, content: str):
        print("✅ [Tool] create_documents was called")
        user_id = config.get("configurable", {}).get("user_id")
        if not user_id:
            raise Exception("Missing user_id in config")
        doc = Document.objects.create(
            owner_id=user_id, 
            title=title, 
            content=content, 
            active=True)

        return {
            "id": doc.id,
            "title": doc.title,
            "content": doc.content,
            "created_at": doc.created_at
        }

    return Tool.from_function(
        name="create_document",
        func=_create_document,
        description="Create a new document for the user by providing a title and content. Use when the user asks to write, draft, or save a new document."
    )


def make_update_document_tool(config):
    def _update_document(document_id: int, title: str = None, content: str = None):
        print("✅ [Tool] update_documents was called")
        user_id = config.get('configurable', {}).get('user_id')

        try:
            doc = Document.objects.get(id=document_id, owner_id=user_id, active=True)
        except Document.DoesNotExist:
            raise Exception("Document not found or access denied.")

        if title:
            doc.title = title
        if content:
            doc.content = content
        if title or content:
            doc.save()

        return {
            "id": doc.id,
            "title": doc.title,
            "content": doc.content,
            "created_at": doc.created_at,
            "updated_at": doc.updated_at,
            "message": f"Document '{doc.title}' updated successfully."
        }

    return Tool.from_function(
        name="update_document",
        func=_update_document,
        description="Update an existing document’s title or content. Use when the user asks to rename, fix, revise, modify, or correct a document."
    )


def make_delete_document_tool(config):
    def _delete_document(document_id: int):
        print("✅ [Tool] delete_document was called")
        user_id = config.get('configurable', {}).get('user_id')

        try:
            doc = Document.objects.get(id=document_id, owner_id=user_id, active=True)
            doc.delete()
        except Document.DoesNotExist:
            raise Exception("Document not found or access denied.")

        return {"message": "Document deleted successfully."}

    return Tool.from_function(
        name="delete_document",
        func=_delete_document,
        description="Delete a document from the user’s list by specifying its ID. Use when the user wants to remove or erase a document."
    )


def make_search_documents_tool(config):
    def _search_documents(query: str, limit: int = 5):
        print("✅ [Tool] search_documents was called")
        if limit > 25:
            limit = 25

        user_id = config.get('configurable', {}).get('user_id')

        qs = Document.objects.filter(
            Q(owner_id=user_id),
            Q(active=True),
            Q(title__icontains=query) | Q(content__icontains=query)
        ).order_by("-created_at")

        return [
            {"id": doc.id, "title": doc.title}
            for doc in qs[:limit]
        ]

    return Tool.from_function(
        name="search_documents",
        func=_search_documents,
        description="Search the user’s documents by keyword in title or content. Use when the user wants to find specific documents based on text."
    )

