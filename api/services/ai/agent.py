from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool
from tools import get_tweets
from helpers.ai_builder import AIBuilder

# Use builder here first then agent
agent = create_react_agent(
    # model = _set_model("gpt-4o-mini"),
    tools=[get_tweets],
    version="v1",
    debug=True,
)

# agent.run(
#     input="Fetch the latest tweets about AI advancements.",)
# )