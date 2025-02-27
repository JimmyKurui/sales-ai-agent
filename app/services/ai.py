import os
from ..config import Config
from ..models.message import Message
from typing import List, Dict
from langchain_ibm import WatsonxLLM
from langchain.chains import ConversationChain, LLMChain
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_message_histories import MongoDBChatMessageHistory 
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage, AIMessage


class AIService:
    def __init__(self):
        self.parameters = {
            "decoding_method": "sample",
            "max_new_tokens": 200,
            "min_new_tokens": 1,
            "temperature": 0.5,
            "top_k": 50,
            "top_p": 1,
        }
        self.llm = WatsonxLLM(
            model_id="ibm/granite-13b-instruct-v2",
            url="https://us-south.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29",
            project_id="e489eb04-9153-402e-be16-6743231fafe9",
            params=self.parameters,
        )
        self.conversation_chain = ConversationChain(llm=self.llm)
    
        # Sales agent prompt template
        self.sales_prompt = PromptTemplate(
            input_variables=["chat_history", "human_input"],
            template="""You are an AI sales assistant. Be helpful but concise. 
            Focus on understanding customer needs and providing relevant information.

            Previous conversation:
            {chat_history}

            Customer: {human_input}
            AI Sales Assistant:"""
        )
        
        # Initialize conversation memory with MongoDB
        # self.message_history = MongoDBChatMessageHistory(
        #     connection_string=os.getenv('MONGODB_URI', 'mongodb://localhost:27017/sales_agent'),
        #     session_id="default",  # Will be updated per conversation
        #     database_name="sales_agent",
        #     collection_name="chat_histories"
        # )
        
        # Set up conversation memory
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            chat_memory=self.message_history
        )
        
        # Initialize the chain
        self.chain = LLMChain(
            llm=self.llm,
            prompt=self.sales_prompt,
            memory=self.memory,
            verbose=True
        )

    def get_conversation_history(self, messages: List[Dict]) -> str:
        """Format messages into conversation history"""
        history = []
        for msg in messages:
            prefix = "Customer: " if msg['sender_type'] == 'client' else "AI: "
            history.append(f"{prefix}{msg['content']}")
        return "\n".join(history)
    
    # simple without db
    def process_message(self, message: str, conversation_id: str) -> dict:
        """
        Process a customer message and return AI response with context
        """
        try:
            self.message_history.session_id = conversation_id
            
            response = self.chain.predict(human_input=message)
            
            insights = self._extract_sales_insights(message, response)
            
            return {
                'response': response,
                'insights': insights,
                'conversation_id': conversation_id
            }
            
        except Exception as e:
            print(f"Error processing message: {e}")
            return {
                'response': "I apologize, but I'm having trouble processing your request. Let me connect you with a human sales representative.",
                'insights': {'error': str(e)},
                'conversation_id': conversation_id
            }
            
    def process_message(self, email: str, message: str, conversation_id: int) -> dict:
        """Process a customer message and return AI response"""
        try:
            # Get conversation history from messages collection
            previous_messages = Message.get_conversation(conversation_id)
            chat_history = self.get_conversation_history(previous_messages)
            
            # Get response from chain
            response = self.chain.predict(
                human_input=message,
                chat_history=chat_history
            )
            
            # Create new message
            ai_message = Message.create(
                email=email,
                content=response,
                sender_type='ai_agent'
            )
            
            return {
                'status': 'success',
                'message': ai_message
            }
            
        except Exception as e:
            print(f"Error processing message: {e}")
            return {
                'status': 'error',
                'message': "I apologize, but I'm having trouble processing your request. Let me connect you with a human sales representative."
            }

    def _extract_sales_insights(self, customer_message: str, ai_response: str) -> dict:
        """
        Extract basic sales insights from the conversation
        """
        insights = {
            'message_length': len(customer_message),
            'contains_question': '?' in customer_message,
            'response_length': len(ai_response)
        }
        return insights

