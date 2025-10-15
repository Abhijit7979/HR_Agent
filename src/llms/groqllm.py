from dotenv import load_dotenv
import os 
from langchain_groq import ChatGroq
from langchain.chat_models import init_chat_model


class Groqllm():

    def __init__(self):
        load_dotenv()

    def get_llm(self):
        try: 
            os.environ["OPENAI_API_KEY"] = self.groq_api_key=os.getenv("OPENAI_API_KEY")
            llm=init_chat_model("openai:gpt-5",api_key=self.groq_api_key)
            # llm= ChatGroq(api_key=self.groq_api_key, model="openai/gpt-oss-20b")
            return llm
        except Exception as e:
            raise ValueError(f"Error initializing Groq LLM: {e}")