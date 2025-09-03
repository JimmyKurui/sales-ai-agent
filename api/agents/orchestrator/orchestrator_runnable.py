from langchain_core.runnables import Runnable, RunnableConfig
from langchain_core.prompts import ChatPromptTemplate
from langchain_tavily import TavilySearch
from langchain_groq import ChatGroq
from api.models.agent import AgentRequest, State
from datetime import datetime



llm = ChatGroq(model="deepseek-r1-distill-llama-70b", temperature=0.5)

assistant_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are Gamma, an outbound task agent operating in the Sales Development Representative pipeline assisting independent sales consultants to close deals with high qualitfying prospects"
            "You aim to speed up prospecting, follow up to bring in qualified leads and other manual intensive tasks that take up time and effort of a sales representative."
            "Use the provided tools to query social media posts, business information, analyze psyche user profiles and other information to assist the user's queries. "
            " When searching, be persistent. Expand your query bounds if the first search returns no results. "
            " If a search comes up empty, expand your search before giving up."
            "\n\nCurrent user:\n<User>\n{user_info}\n</User>"
            "\nCurrent time: {time}.",
        ),
        ("placeholder", "{messages}"),
    ]
).partial(time=datetime.now)

tools = [
    TavilySearch(max_results=3),
]
orchestrator_runnable = assistant_prompt | llm.bind_tools(tools)