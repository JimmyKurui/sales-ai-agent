from langgraph.graph.message import AnyMessage, add_messages
from langchain_core.messages import HumanMessage
from langchain_core.runnables import Runnable, RunnableConfig
from typing import Annotated, TypedDict



class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    user_info: str

class SocialsState(State):
    topic: str
    

class AgentOutput(TypedDict):
    response: str
    
class AgentConfig(TypedDict):
    name: str
    description: str
    version: str
    
class Agent(TypedDict):
    config: AgentConfig
    output: AgentOutput
    
class AgentResponse(TypedDict):
    agent: Agent
    
class AgentRequest(State, total=False):
    messages: list[str]
    

class AgentRunnable:
    def __init__(self, runnable: Runnable):
        self.runnable = runnable

    def __call__(self, state: State, config: RunnableConfig):
        while True:
            # state = State(**{**state.model_dump(), **config.get("configurable")})
            result = self.runnable.invoke(state)
            # If the LLM happens to return an empty response, we will re-prompt it
            # for an actual response.
            if not result.tool_calls and (
                not result.content
                or isinstance(result.content, list)
                and not result.content[0].get("text")
            ):
                state["messages"] += HumanMessage(content="Respond with a real output.")
            else:
                break
        return {"messages": result}