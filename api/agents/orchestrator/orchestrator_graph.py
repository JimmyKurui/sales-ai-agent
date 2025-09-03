from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph, START
from langgraph.prebuilt import tools_condition
from api.models.agent import State, AgentRunnable
from api.agents.utils import create_tool_node_with_fallback
from .orchestrator_runnable import tools, orchestrator_runnable

def create_orchestrator_agent(state: State = State) -> StateGraph:
    builder = StateGraph(state)
    builder.add_node("assistant", AgentRunnable(orchestrator_runnable))
    builder.add_node("tools", create_tool_node_with_fallback(tools))
    builder.add_edge(START, "assistant")
    builder.add_conditional_edges("assistant", tools_condition)
    builder.add_edge("tools", "assistant")

    memory = InMemorySaver()
    orchestrator_graph = builder.compile(
        checkpointer=memory,
    )
    return orchestrator_graph