from documents.models import Document
from langchain_core.tools import Tool
from django.db.models import Q

def make_list_documents_tool(config):
    def _list_documents(limit: int = 5):
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
        description="List up to 25 of the user's most recent documents."
    )


def make_get_document_tool(config):
    def _get_document(document_id: int):
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
        description="Get a document's full details using its ID."
    )


def make_create_document_tool(config):
    def _create_document(title: str, content: str):
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
        description="Create a new document with a title and content for the current user."
    )


def make_update_document_tool(config):
    def _update_document(document_id: int, title: str = None, content: str = None):
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
            "created_at": doc.created_at
        }

    return Tool.from_function(
        name="update_document",
        func=_update_document,
        description="Update a document's title or content for the current user."
    )


def make_delete_document_tool(config):
    def _delete_document(document_id: int):
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
        description="Delete a document by ID for the current user."
    )


def make_search_documents_tool(config):
    def _search_documents(query: str, limit: int = 5):
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
        description="Search a user's documents by text in title or content. Max 25 results."
    )

