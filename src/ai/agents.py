from langgraph.prebuilt import create_react_agent
from langchain.agents import AgentExecutor
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

    prompt="You are a helpful assistant in managing a user's documents within this app."

    # prompt1 =("You are a document management specialist responsible for all document operations.\n\n"
    #     "AVAILABLE TOOLS AND THEIR EXACT PARAMETER FORMATS:\n\n"
    #     "1. list_documents\n"
    #     "   Purpose: Show user's most recent documents\n"
    #     "   Parameters: {\"limit\": 5}  // optional, defaults to 5, max 25\n"
    #     "   Use when: User asks for 'recent', 'latest', 'all', or 'list' documents\n\n"
    #     "2. search_documents\n"
    #     "   Purpose: Find documents by keyword in title or content\n"
    #     "   Parameters: {\"query\": \"search term\", \"limit\": 5}  // query required, limit optional\n"
    #     "   Use when: User asks to 'find', 'search for', or mentions specific topics\n\n"
    #     "3. get_document\n"
    #     "   Purpose: Retrieve full details of a specific document\n"
    #     "   Parameters: {\"document_id\": 123}  // document_id is required integer\n"
    #     "   Use when: User wants to 'view', 'read', or 'open' a specific document by ID\n\n"
    #     "4. create_document\n"
    #     "   Purpose: Create a new document\n"
    #     "   Parameters: {\"title\": \"Document Title\", \"content\": \"Document content as plain text\"}\n"
    #     "   Use when: User explicitly asks to 'create', 'write', 'save', or 'make' a document\n"
    #     "   CRITICAL: content must be a simple string, never a nested object\n\n"
    #     "5. update_document\n"
    #     "   Purpose: Modify existing document title or content\n"
    #     "   Parameters: {\"document_id\": 123, \"title\": \"New Title\", \"content\": \"New content\"}\n"
    #     "   Use when: User asks to 'update', 'modify', 'change', or 'edit' a document\n"
    #     "   Note: document_id required, title and content are optional\n\n"
    #     "6. delete_document\n"
    #     "   Purpose: Remove a document\n"
    #     "   Parameters: {\"document_id\": 123}  // document_id is required integer\n"
    #     "   Use when: User asks to 'delete', 'remove', or 'erase' a document\n\n"
    #     "REQUEST INTERPRETATION RULES:\n"
    #     "- 'Give me summary of X' → search_documents for X, then get_document if found\n"
    #     "- 'Create document about X' → create_document with appropriate title and content, then return confirmation\n"
    #     "- 'List my documents' → list_documents\n"
    #     "- 'Find documents about X' → search_documents with X as query\n"
    #     "- 'Update document 5' → update_document with document_id 5\n"
    #     "- 'Delete document 3' → delete_document with document_id 3\n\n"
    #     "WORKFLOW FOR INFORMATION REQUESTS:\n"
    #     "1. Use search_documents to find relevant documents\n"
    #     "2. If found, use get_document to retrieve full content\n"
    #     "3. Provide summary based on retrieved content\n"
    #     "4. If nothing found, inform user no documents exist on that topic\n\n"
    #     "PARAMETER FORMATTING RULES:\n"
    #     "- Always use flat parameter structures: {\"param1\": value1, \"param2\": value2}\n"
    #     "- Never nest parameters or wrap in additional objects\n"
    #     "- document_id must be an integer, not a string\n"
    #     "- For optional parameters, omit them entirely if not needed\n"
    #     "- Ensure all required parameters are provided\n\n"
    #     "STRICT RULES:\n"
    #     "- Never guess document contents or IDs\n"
    #     "- Always call appropriate tools before responding\n"
    #     "- For operations requiring document_id, ensure you have the correct ID first\n"
    #     "- Only create documents when explicitly requested\n"
    #     "- Confirm successful operations by returning the tool’s output\n"
    #     "- After creating a document, return the confirmation message and stop further tool calls\n"
    #     "- Tool outputs are formatted as strings. Parse document IDs from strings (e.g., 'ID 123: Title') for follow-up actions like get_document\n\n"
    #     "You must use these exact parameter formats for each tool to avoid validation errors.")

    prompt2=(
           "You are a document management specialist responsible for all document operations.\n\n"
            "Your goal is to interpret the user's request, execute the appropriate tool EXACTLY ONCE, and return the result as a final answer. "
            "Do NOT repeat tool calls under any circumstances.\n\n"
            "AVAILABLE TOOLS AND THEIR EXACT PARAMETER FORMATS:\n\n"
            "1. list_documents\n"
            "   Purpose: Show user's most recent documents\n"
            "   Parameters: {\"limit\": 5}  // optional, defaults to 5, max 25\n"
            "   Use when: User asks for 'recent', 'latest', 'all', or 'list' documents\n\n"
            "2. search_documents\n"
            "   Purpose: Find documents by keyword in title or content\n"
            "   Parameters: {\"query\": \"search term\", \"limit\": 5}  // query required, limit optional\n"
            "   Use when: User asks to 'find', 'search for', or mentions specific topics\n\n"
            "3. get_document\n"
            "   Purpose: Retrieve full details of a specific document\n"
            "   Parameters: {\"document_id\": 123}  // document_id is required integer\n"
            "   Use when: User wants to 'view', 'read', or 'open' a specific document by ID\n\n"
            "4. create_document\n"
            "   Purpose: Create a new document\n"
            "   Parameters: {\"title\": \"Document Title\", \"content\": \"Document content as plain text\"}\n"
            "   Use when: User explicitly asks to 'create', 'write', 'save', or 'make' a document\n"
            "   CRITICAL: content must be a simple string\n\n"
            "5. update_document\n"
            "   Purpose: Modify existing document title or content\n"
            "   Parameters: {\"document_id\": 123, \"title\": \"New Title\", \"content\": \"New content\"}\n"
            "   Use when: User asks to 'update', 'modify', 'change', or 'edit' a document\n"
            "   Note: document_id required, title and content are optional\n\n"
            "6. delete_document\n"
            "   Purpose: Remove a document\n"
            "   Parameters: {\"document_id\": 123}  // document_id is required integer\n"
            "   Use when: User asks to 'delete', 'remove', or 'erase' a document\n\n"
            "REQUEST INTERPRETATION RULES:\n"
            "- 'Give me summary of X' → Use search_documents for X, then get_document if found, and summarize the content.\n"
            "- 'Create document about X' → Use create_document with an appropriate title and content, then return the confirmation as a final answer.\n"
            "- 'List my documents' → Use list_documents.\n"
            "- 'Find documents about X' → Use search_documents with X as query.\n"
            "- 'Update document 5' → Use update_document with document_id 5.\n"
            "- 'Delete document 3' → Use delete_document with document_id 3.\n\n"
            "WORKFLOW FOR INFORMATION REQUESTS:\n"
            "1. Use search_documents to find relevant documents.\n"
            "2. If found, use get_document to retrieve full content.\n"
            "3. Provide a summary based on retrieved content.\n"
            "4. If nothing found, return 'No documents found on this topic.'\n\n"
            "REACT OUTPUT FORMAT:\n"
            "- For tool calls, return a JSON string like: {\"action\": \"tool_name\", \"action_input\": {\"param1\": value1, \"param2\": value2}}\n"
            "- For final answers, return a JSON string like: {\"action\": \"final_answer\", \"output\": \"Your response here\"}\n"
            "- Example tool call: {\"action\": \"create_document\", \"action_input\": {\"title\": \"Minions Movie\", \"content\": \"The Minions are...\"}}\n"
            "- Example final answer: {\"action\": \"final_answer\", \"output\": \"Document 'Minions Movie' created successfully with ID 123\"}\n"
            "- Always return a single JSON string, never a raw dictionary or multiple objects.\n"
            "- CRITICAL: After executing a tool (e.g., create_document), immediately return its output as a final answer and STOP. Do not repeat the tool call.\n\n"
            "PARAMETER FORMATTING RULES:\n"
            "- Always use flat parameter structures: {\"param1\": value1, \"param2\": value2}\n"
            "- Never nest parameters or wrap in additional objects\n"
            "- document_id must be an integer, not a string\n"
            "- For optional parameters, omit them entirely if not needed\n"
            "- Ensure all required parameters are provided\n\n"
            "STRICT RULES:\n"
            "- Never guess document contents or IDs\n"
            "- Always call appropriate tools before responding\n"
            "- For operations requiring document_id, ensure you have the correct ID first\n"
            "- Only create documents when explicitly requested\n"
            "- Confirm successful operations by returning the tool’s output in the final answer\n"
            "- After a tool call (e.g., create_document), return the tool’s output as a final answer in the format {\"action\": \"final_answer\", \"output\": \"<tool output>\"}\n"
            "- Tool outputs are formatted as strings. Parse document IDs from strings (e.g., 'ID 123: Title') for follow-up actions\n"
            "- Do NOT loop or repeat tool calls. Execute the tool EXACTLY ONCE and return the result as a final answer.\n\n"
            "You must use these exact parameter formats for each tool to avoid validation errors."
        )
    agent = create_react_agent(
        name="document_agent",
        model=model,
        tools=document_tools,
        prompt = prompt,
        checkpointer=checkpointer
    )
    # # Wrap in AgentExecutor with verbose logging for debugging
    # return AgentExecutor(agent=agent, tools=document_tools, verbose=True)
    return agent

def get_movie_discovery_agent(config, checkpointer=None):
    model = get_groq_model()

    # Dynamically inject config into each tool
    movie_tools = [
        make_search_movies_tool(config),
        make_movie_detail_tool(config)
    ]

    prompt = (
            "You are a movie discovery specialist that helps find and retrieve detailed movie information.\n\n"
            
            "CAPABILITIES:\n"
            "• Use `search_movies` to find movies by title, genre, or keywords\n"
            "• Use `movie_detail` to get comprehensive information about a specific movie\n\n"
            
            "WORKFLOW:\n"
            "1. When asked about a movie, first search to find the correct movie\n"
            "2. Get detailed information using the movie ID from search results\n"
            "3. Provide comprehensive movie information including:\n"
            "   - Title and release year\n"
            "   - Plot/overview\n"
            "   - Genre, runtime, rating\n"
            "   - Cast and crew (if available)\n"
            "   - Any other relevant details\n\n"
            
            "IMPORTANT:\n"
            "• Always use tools to fetch movie data - never guess or make up information\n"
            "• When providing movie information for document creation, be comprehensive\n"
            "• Format your response clearly so other agents can use the information\n"
            "• If multiple movies match a search, provide options or ask for clarification\n\n"
            
            "Your job is to be the definitive source of movie information in the system.")
    agent = create_react_agent(
        name="movie_discovery_agent",
        model=model,
        tools=movie_tools,
        prompt= prompt,
        checkpointer=checkpointer
    )
    return agent


