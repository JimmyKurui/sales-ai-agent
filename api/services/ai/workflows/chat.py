from langgraph.graph import START, END, StateGraph
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.constants import Send
from pydantic import BaseModel
from typing import TypedDict
from helpers.ai_builder import AIBuilder
from tools.twitter import get_tweets
    
llm = AIBuilder(model_name="meta-llama/llama-3.3-70b-instruct:free", role="default")     
print(llm)

class ClarifiedMessage(BaseModel):
    intent: str
    message: str
    action: str
    
supervisor = llm.with_structured_output(ClarifiedMessage)


class SocialsInsights(TypedDict):
    platform: str
    insights: str
    
class BioData(TypedDict):
    name: str
    age: int
    location: str
    interests: list[str]
    values: list[str]
    average_income: float
    
class State(BaseModel):
    message: ClarifiedMessage
    socials_insights: list[SocialsInsights]
    all_insights: str
    personality: str
    sentiment: str
    pain_points: str
    past_actions: str
    
    
# Nodes
def prospecter(input: str) -> State:
    """ Orchestrates the flow based on the user's message to qualify a lead. """
    message: dict = supervisor.invoke([
      SystemMessage(content="""You are an AI prospecting sales assistant that clarifies user messages to determine their intent and required action regarding a particular human or company subject. 
            This clarity is highly optimized and suitable for for other agents downstream to process for accurate and relevant results."""),
    ])
    # supervisor.invoke([SystemMessage(content=f"Based on this clarified message got from a user that gives the intent, desired action and message: {clarified_message}. \n\nDetermine the next action to take based on the intent and message. If the intent is to fetch social media insights, proceed to the respective social media nodes. If the intent is to end the conversation, return an empty state.")])
    return {"messsage": message}

def twitter(state: State) -> State:
    """ Fetches insights from Twitter based on the user's message. """
    insights = get_tweets()
    return {"socials_insights": [{"platform": "twitter", "insights": insights}]}

def evaluator(state: State) -> State:
    """ Evaluates the insights and determines the next action. """
    # Here you would implement logic to evaluate the insights and decide on the next action
    llm.invoke([
        SystemMessage(content="Evaluate the insights from the social media platforms and determine the next action based on the insights gathered. If the insights are sufficient, end the conversation. If more information is needed, clarify the next steps."),
        HumanMessage(content=state.socials_insights)
    ])
    return state
    
# Chaining the nodes 
chat_builder = StateGraph(State)

chat_builder.add_node("prospecter", prospecter)
chat_builder.add_node("twitter", twitter)
# chat_builder.add_node("linkedin", linkedin)
# chat_builder.add_node("facebook", facebook)
# chat_builder.add_node("article", article)
chat_builder.add_node("evaluator", evaluator)

chat_builder.add_edge(START, "prospecter")
chat_builder.add_conditional_edge("prospecter", "twitter", lambda x: x.get("platform") == "twitter")
# chat_builder.add_conditional_edge("prospecter", "linkedin", lambda x: x.get("platform") == "linkedin")
# chat_builder.add_conditional_edge("prospecter", "facebook", lambda x: x.get("platform") == "facebook")
chat_builder.add_edge("twitter", "evaluator")
# chat_builder.add_edge("linkedin", "synthesizer")
# chat_builder.add_edge("facebook", "synthesizer")
chat_builder.add_conditional_edge("evaluator", END, lambda x: x.get("action") == "end")
