from langchain_openai import ChatOpenAI
from .agent import Agent
from langchain_core.messages import HumanMessage
from .tools import query_tool
from .tools import upsert_tool
from .tools import search_tool

class Inference:

    def __init__(self):
        self.tools = [query_tool, upsert_tool, search_tool]
        self.model_breakdown = ChatOpenAI(model="gpt-4o-mini")  # Updated to GPT-4o-mini
        self.model_qualification = ChatOpenAI(model="gpt-4o-mini")  # Updated to GPT-4o-mini
        self.model_decision = ChatOpenAI(model="gpt-4o-mini")  # Updated to GPT-4o-mini

    def query_workflow(self, user_query):
        abot = Agent(self.model_breakdown, self.model_qualification, self.model_decision, self.tools)

        messages = [HumanMessage(content=user_query)]
        result = abot.graph.invoke({"messages": messages})
        return result['messages'][-1].content
    
    def query_update(self, user_updated_query):
        pass

inference_obj = Inference()