import os
from dotenv import load_dotenv
from agents import Agent, AsyncOpenAI, ModelSettings, OpenAIChatCompletionsModel
import requests
#from tavily import AsyncTavilyClient, TavilyClient




load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")
#TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

#tavily_client = TavilyClient(api_key=TAVILY_API_KEY)
# 1. Which LLM Service?
external_client: AsyncOpenAI = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# 2. Which LLM Model?
llm_model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_client
)
