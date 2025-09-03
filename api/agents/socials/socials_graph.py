from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import tools_condition
from api.models.agent import SocialsState, AgentRunnable
from api.agents.utils import create_tool_node_with_fallback
from .socials_runnable import (socials_runnable, 
                                    socials_safe_tools,
                                    socials_sensitive_tools, 
                                    sensitive_tool_names)

def create_social_media_agent(state: SocialsState = SocialsState) -> StateGraph:
    builder = StateGraph(state)
    builder.add_node("assistant", AgentRunnable(socials_runnable))
    builder.add_node("safe_tools", create_tool_node_with_fallback(socials_safe_tools))
    builder.add_node(
        "sensitive_tools", create_tool_node_with_fallback(socials_sensitive_tools)
    )
    builder.add_edge(START, "assistant")

    def route_tools(state: SocialsState):
        next_node = tools_condition(state)
        # If no tools are invoked, return to the user
        if next_node == END:
            return END
        ai_message = state["messages"][-1]
        # This assumes single tool calls. To handle parallel tool calling, you'd want to
        # use an ANY condition
        first_tool_call = ai_message.tool_calls[0]
        if first_tool_call["name"] in sensitive_tool_names:
            return "sensitive_tools"
        return "safe_tools"

    builder.add_conditional_edges(
        "assistant", route_tools, ["safe_tools", "sensitive_tools", END]
    )
    builder.add_edge("safe_tools", "assistant")
    builder.add_edge("sensitive_tools", "assistant")

    memory = InMemorySaver()
    socials_graph = builder.compile(
        checkpointer=memory,
        interrupt_before=["sensitive_tools"],
    )
    return socials_graph