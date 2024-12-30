from langchain_core.tools import tool
from langchain_core.messages import ToolMessage
import uuid

@tool
def search_tool(queries: list) -> ToolMessage:
    """This is a search tool"""

    tool_call_id = f"tool_call_{uuid.uuid4()}"
    return ToolMessage(name=search_tool.name, content={"results": queries}, tool_call_id=tool_call_id)