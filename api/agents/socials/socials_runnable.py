from langchain_groq import ChatGroq
from langchain_tavily import TavilySearch
from langchain_core.prompts import ChatPromptTemplate
from datetime import datetime


# moonshotai/kimi-k2-instruct
llm = ChatGroq(model="deepseek-r1-distill-llama-70b", temperature=0.8)

assistant_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a social media agent bot that scans through the internet for knowledge about 1 person through their online presence and interactions."
            "You aim to specifically gather messages and information about a certain {topic} in which the user directly or indirectly participates in. Follow up on these threads to observe more on what the user mentions about the topic"
            "Use the provided tools to query social media posts, business information and news to return messages in their original form or paraphrased from articles"
            "When searching, be persistent. Expand your query bounds if the first search returns no results. "
            " If a search comes up empty, expand your search before giving up."
            "\n\nFollow up from this initial social link and search for other social media. Return only the latest 10 posts you get from each social media \n<User>\n{user_info}\n</User>"
            "\nCurrent time: {time}.",
        ),
        ("placeholder", "{messages}"),
    ]
).partial(time=datetime.now)


# "Read"-only tools (such as retrievers) don't need a user confirmation to use
socials_safe_tools = [
    TavilySearch(max_results=6),
]

socials_sensitive_tools = [
]
sensitive_tool_names = {t.name for t in socials_sensitive_tools}

socials_runnable = assistant_prompt | llm.bind_tools(
    socials_safe_tools + socials_sensitive_tools
)
