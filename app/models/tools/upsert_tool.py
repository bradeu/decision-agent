from langchain_core.tools import tool
from langchain_core.messages import ToolMessage
import uuid
from ...db.pinecone import db_helper_obj

@tool
def upsert_tool(text: str) -> ToolMessage:
    """This is an upsert tool"""

    if not isinstance(text, str):
        raise ValueError("Expected 'text' to be a string.")
    
    sentences = db_helper_obj.split_text_into_sentences(text)
    vector = db_helper_obj.embed_sentences_openai(sentences)
    res = db_helper_obj.upsert_method(vector)
    
    tool_call_id = f"tool_call_{uuid.uuid4()}"
    return ToolMessage(name=upsert_tool.name, content={"results": res}, tool_call_id=tool_call_id)


    