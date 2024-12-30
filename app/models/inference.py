from langchain_openai import ChatOpenAI
from .helper.agent import Agent
from langchain_core.messages import HumanMessage
from .tools import query_tool
from .tools import upsert_tool
from .tools import search_tool

class Inference:

    def query_workflow(self, user_query):
        model = ChatOpenAI(model="gpt-4o-mini")  # Updated to GPT-4o-mini
        abot = Agent(model, query_tool, upsert_tool, search_tool)

        messages = [HumanMessage(content=user_query)]
        result = abot.graph.invoke({"messages": messages})
        return result['messages'][-1].content

inference_obj = Inference()