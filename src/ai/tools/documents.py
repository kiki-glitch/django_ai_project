from documents.models import Document
from langchain_core.tools import Tool
from django.db.models import Q
from typing import Any
from pydantic import field_validator, BaseModel, Field

# Define schema using Pydantic
class ListDocumentsInput(BaseModel):
    limit: int = Field(default=5, description="Number of documents to return (max 25)")

class SearchDocumentsInput(BaseModel):
    query: str = Field(..., description="Keyword to search for in title or content")
    limit: int = Field(default=5, description="Number of results to return (max 25)")

class GetDocumentInput(BaseModel):
    document_id: int = Field(..., description="ID of the document to retrieve")

class CreateDocumentInput(BaseModel):
    title: str = Field(..., description="Title of the new document")
    content: str = Field(..., description="Content of the new document as a string")

class UpdateDocumentInput(BaseModel):
    document_id: int = Field(..., description="ID of the document to update")
    title: str = Field(default=None, description="New title (optional)")
    content: str = Field(default=None, description="New content (optional)")

class DeleteDocumentInput(BaseModel):
    document_id: int = Field(..., description="ID of the document to delete")


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

        docs = qs[:limit]
        if not docs:
            return "No documents found."
        
        # return [
        #     {"id": doc.id, "title": doc.title}
        #     for doc in qs[:limit]
        # ]
        # Return as formatted string instead of list of dicts
        doc_list = "\n".join([f"ID {doc.id}: {doc.title}" for doc in docs])
        return f"Your recent documents:\n{doc_list}"

    return Tool.from_function(
        name="list_documents",
        func=_list_documents,
        description="List upto 25 documents for the current user, ordered by most recent first. Use this tool whenever the user asks for recent, all, or latest documents..",
        args_schema=ListDocumentsInput
    )

def make_search_documents_tool(config):
    def _search_documents(query: str, limit: int = 5):
        """
        Search documents using a keyword.

        Parameters:
        - query (str): The search string to filter documents.
        - limit (int, optional): Maximum number of results to return. Defaults to 5.
        """

        print("✅ [Tool] search_documents was called")
        if limit > 25:
            limit = 25

        user_id = config.get('configurable', {}).get('user_id')

        qs = Document.objects.filter(
            Q(owner_id=user_id),
            Q(active=True),
            Q(title__icontains=query) | Q(content__icontains=query)
        ).order_by("-created_at")

        docs = qs[:limit]
        if not docs:
            return "No documents found matching the query."
        
        doc_list = "\n".join([f"ID {doc.id}: {doc.title}" for doc in docs])
        return f"Found {len(docs)} documents matching '{query}':\n{doc_list}"

    return Tool.from_function(
        name="search_documents",
        func=_search_documents,
        description="Search the user’s documents by keyword in title or content. Use when the user wants to find specific documents based on text.",
        args_schema=SearchDocumentsInput
    )

def make_get_document_tool(config):
    def _get_document(document_id: int):
        print("✅ [Tool] get_documents was called")
        user_id = config.get('configurable', {}).get('user_id')

        try:
            doc = Document.objects.get(id=document_id, owner_id=user_id, active=True)
            # Return formatted string instead of dict
            return f"Document ID {doc.id}: {doc.title}\n\nContent:\n{doc.content}"
        except Document.DoesNotExist:
            raise Exception("Document not found or access denied.")


    return Tool.from_function(
        name="get_document",
        func=_get_document,
        description="Retrieve a specific document’s full details (title, content, date) by its ID. Use when the user asks to open or view a document.",
        args_schema=GetDocumentInput
    )

def make_create_document_tool(config):
    def _create_document(title: str, content: str):

        print(f"[Tool] create_document called with title='{title}', content type={type(content)}")
        user_id = config.get("configurable", {}).get("user_id")
        if not user_id:
            raise Exception("Missing user_id in config")
        doc = Document.objects.create(
            owner_id=user_id, 
            title=title, 
            content=content, 
            active=True)
        return f"Document '{doc.title}' created successfully with ID {doc.id}"

    
    return Tool.from_function(
        name="create_document",
        func=_create_document,
        description="Create a new document for the user by providing a title and content. Use when the user asks to write, draft, or save a new document.",
        args_schema=CreateDocumentInput
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

        return f"Document ID {doc.id} ('{doc.title}') updated successfully."

    return Tool.from_function(
        name="update_document",
        func=_update_document,
        description="Update an existing document’s title or content. Use when the user asks to rename, fix, revise, modify, or correct a document.",
        args_schema=UpdateDocumentInput
    )

def make_delete_document_tool(config):
    def _delete_document(document_id: int):
        print("✅ [Tool] delete_document was called")
        user_id = config.get('configurable', {}).get('user_id')

        try:
            doc = Document.objects.get(id=document_id, owner_id=user_id, active=True)
            doc.delete()
            return f"Document ID {document_id} deleted successfully."
        except Document.DoesNotExist:
            raise Exception("Document not found or access denied.")

    return Tool.from_function(
        name="delete_document",
        func=_delete_document,
        description="Delete a document from the user’s list by specifying its ID. Use when the user wants to remove or erase a document.",
        args_schema=DeleteDocumentInput
    )



