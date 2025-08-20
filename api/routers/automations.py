from api.services.ai.helpers.ai_builder import AIBuilder
from api.services.ai.models.chat_model import InputMessage
from langchain_core.messages import SystemMessage, HumanMessage
from fastapi import APIRouter, Body
from datetime import datetime, timezone

router = APIRouter(prefix="/ai", tags=["api"])

@router.post("/chat/")
def chat(data: dict = Body(...)) -> str:
    print(f"Received data: {data}")
    """
    Handles a chat request by sending the user's message to the AI model and returning the AI's response.

    Parameters:
        input (str): The user's input message.

    Returns:
        str: The AI-generated response to the user's message.
    """
    llm = AIBuilder(model_name="gemma2-9b-it", role="default").model
    print(llm)
    response = llm.invoke([
        SystemMessage(content="You are Gamma, a helpful sales ai agent that supports sales development representatives. Your primary focus is to efficiently prospect clients and qualify leads at a high standard. secondly to perform the complementary outbound tasks that are required to qualify a lead. You are helpful, professional and tactical in assisting with the sales process. If the question is more specific and you do not know the answer, simply state you do not know. The user message has been attached within this marks === {input} ==="),
        HumanMessage(content=data["message"])
    ])
    
    timestamp = datetime.now(timezone.utc)
    with open("chat_log.txt", "a") as log_file:
        log_file.write(f"{timestamp}, User: {data["message"]}\n")
        log_file.write(f"{timestamp}, AI: {response}\n")
    return response.content