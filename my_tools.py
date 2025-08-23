from agents import Agent, function_tool, ItemHelpers, RunContextWrapper
from tavily import AsyncTavilyClient, TavilyClient
from dataclasses import dataclass
from my_config.gemini_config import llm_model
import os
import asyncio

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

@dataclass
class UserContext:
    name: str
    city:str
    topic: str | None = None

@function_tool()

async def user_info(ctx: RunContextWrapper[UserContext]):
    """personalized information"""


    return (f"You are helping {ctx.context.name} from {ctx.context.city} who likes {ctx.context.topic}. Personalise examples accordingly.")

def dynamic_instructions(
    ctx: RunContextWrapper[UserContext], agent: Agent[UserContext]) -> str:
        """You are a helpful research assistant.Use context to call person.
        Use the web_search_tool to get the latest information on the query and than extract content
         using extract_content tool.Also use context for personalization.Finaly sumarize answer in bullet points.Donot ask user for more information."""
                      
        return f"The user's name is {ctx.context.name}. Help them with their questions." 


@function_tool()
async def web_search_tool(query: str, search_depth: str = "advanced", max_results: int = 5) -> str:
    """

    Perform a web search using Tavily API.

    Args:
        query (str): The search query.
        search_depth (str): "basic" (faster) or "advanced" (more comprehensive).
        max_results (int): Number of results to return (max 10).

    Returns:
        list: A list of search results with titles, URLs, and snippets.
    """
    try:
        response = await asyncio.to_thread(
        tavily_client.search,
        query=query,
        search_depth=search_depth,
        max_results=max_results
        )
        
        return response
    except Exception as e:
        print(f"Error performing web search: {e}")
        return {"error": str(e), "results": []}

@function_tool()
def extract_content(urls:list)-> dict:
    """
    Perform a web extract using Tavily API.

    Args:urls:read urls and extract content.

    Returns:
        dict:give the content of that urls.
    """
    try:
        response = tavily_client.extract(urls)
        
        return response
    except Exception as e:
        print(f"Error performing web scrap: {e}")
        return {"error": str(e), "results": []}
