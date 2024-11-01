from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

class LLMConfig:
    @staticmethod
    def setup_llm():
        load_dotenv()
        
        model_name = os.getenv('MODEL_NAME', 'gpt-4')
        temperature = float(os.getenv('TEMPERATURE', '0.7'))
        
        if 'claude' in model_name.lower():
            return ChatAnthropic(
                anthropic_api_key=os.getenv('ANTHROPIC_API_KEY'),
                model=model_name,
                temperature=temperature
            )
        else:
            return ChatOpenAI(
                openai_api_key=os.getenv('OPENAI_API_KEY'),
                temperature=temperature,
                model_name=model_name
            )