from langchain_ibm import WatsonxLLM
from langchain.chains import ConversationChain
from ibm_watsonx_ai import Credentials
from ..config import Config


class AIService:
    def __init__(self):
        self.parameters = parameters = {
            "decoding_method": "sample",
            "max_new_tokens": 100,
            "min_new_tokens": 1,
            "temperature": 0.5,
            "top_k": 50,
            "top_p": 1,
        }
        # self.llm = WatsonxLLM(
        #     model_id="ibm/granite-13b-instruct-v2",
        #     url="https://us-south.ml.cloud.ibm.com",
        #     project_id="PASTE YOUR PROJECT_ID HERE",
        #     params=self.parameters,
        # )
        # self.conversation_chain = ConversationChain(llm=self.llm)

    def generate_response(self, message, context=None):
        response = self.conversation_chain.predict(input=message)
        return response
