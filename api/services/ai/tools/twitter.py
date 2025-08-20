from langchain_core.tools import tool

@tool
def get_tweets():
        return "Fetched tweets..."