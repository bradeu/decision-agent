from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator
from langchain_core.messages import AnyMessage, SystemMessage, ToolMessage
from dotenv import load_dotenv
import json

# import logging

# logging.basicConfig(
#     level=logging.DEBUG,
#     format='%(asctime)s - %(levelname)s - %(message)s'
# )

_ = load_dotenv()

class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]

class Agent:
    def __init__(self, model, tools):
        graph = StateGraph(AgentState)

        graph.add_node("breakdown_agent", self.call_openai_breakdown_tasks)
        graph.add_node("qualification_agent", self.call_openai_qualification)
        graph.add_node("decision_agent", self.call_openai_decision)
        graph.add_node("take_action", self.take_action)

        graph.add_conditional_edges(
            "breakdown_agent",
            self.exists_action,
            {True: "action", False: "decision_agent"}
        )
        graph.add_edge("action", "qualification_agent")
        graph.add_conditional_edges(
            "qualification_agent",
            self.exists_action,
            {True: "action", False: "breakdown_agent"}
        )
        graph.add_edge("decision_agent", END)

        graph.set_entry_point("breakdown_agent")
        self.graph = graph.compile()
        self.tools = {t.name: t for t in tools}
        self.model = model.bind_tools(tools)


    def call_openai_breakdown_tasks(self, state: AgentState):
        messages = state['messages']

        system_query = """You are a breakdown sub-agent, your task is to break down the query into multiple executable steps based on the available tools. \
            You are allowed to make multiple calls (either together or in sequence). \
            Only look up information when you are sure of what you want. \
            If you need to look up some information before asking a follow up question, you are allowed to do that!"""

        messages = [SystemMessage(content=system_query)] + messages
        message = self.model.invoke(messages)
        new_state = {'messages': [message]}
        return new_state
    
    def call_openai_qualification(self, state: AgentState):
        initial_message = state["messages"][0]
        messages = state['messages']

        system_query = f"You are a qualification sub-agent, your task is to make sure that the informations provided covered fully this query: {initial_message}."

        messages = [SystemMessage(content=system_query)] + messages
        message = self.model.invoke(messages)
        new_state = {'messages': [message]}
        return new_state

    def call_openai_decision(self, state: AgentState):
        initial_message = state["messages"][0]
        messages = state['messages']

        system_query = f"You are a decision sub-agent, your task is to decide which booking is the best based on this query: {initial_message}."

        messages = [SystemMessage(content=system_query)] + messages
        message = self.model.invoke(messages)
        new_state = {'messages': [message]}
        return new_state

    def exists_action(self, state: AgentState):
        result = state['messages'][-1]
        return len(result.tool_calls) > 0

    def take_action(self, state: AgentState):
        tool_calls = state['messages'][-1].tool_calls
        results = []
        for t in tool_calls:
            print(f"Calling: {t}")
            if not t['name'] in self.tools:
                print("\n ....bad tool name....")
                result = "bad tool name, retry"
            else:
                result = self.tools[t['name']].invoke(t['args'])
            results.append(ToolMessage(tool_call_id=t['id'], name=t['name'], content=str(result)))
        print("To the filter model!")
        return {'messages': results}