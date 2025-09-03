from agents import Agent, function_tool, ItemHelpers, RunContextWrapper
from tavily import AsyncTavilyClient, TavilyClient
from dataclasses import dataclass
from my_config.gemini_config import llm_model
import os
import asyncio
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)

# Load API Key
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

# -----------------------------
# Context Model
# -----------------------------
@dataclass
class UserContext:
    name: str
    city: str
    topic: str | None = None


# -----------------------------
# Tools
# -----------------------------
@function_tool()
async def user_info(ctx: RunContextWrapper[UserContext]) -> str:
    """
    Provide personalized context about the user.

    Args:
        ctx (RunContextWrapper[UserContext]): Contains user context (name, city, topic).

    Returns:
        str: A formatted sentence describing the user.
    """
    return (
        f"You are helping {ctx.context.name} from {ctx.context.city} "
        f"who likes {ctx.context.topic or 'various topics'}. "
        "Personalize examples accordingly."
    )


def dynamic_instructions(ctx: RunContextWrapper[UserContext], agent: Agent[UserContext]) -> str:
    """
    Generate dynamic instructions for the orchestrator agent.

    Guidelines:
    1. Use context (name, city, topic) to personalize answers.
    2. Use web_search_tool to get the latest information.
    3. Use extract_content to expand on URLs when needed.
    4. Summarize findings in bullet points.
    5. Always include citations from citations_agent.
    6. Do not ask the user for more information — work with what’s available.

    Args:
        ctx (RunContextWrapper[UserContext]): User context.
        agent (Agent[UserContext]): The agent requesting instructions.

    Returns:
        str: Personalized instruction string for the agent.
    """
    return (
        f"The user's name is {ctx.context.name}. "
        f"They are from {ctx.context.city} and interested in {ctx.context.topic or 'general topics'}. "
        "Help them with their questions following the guidelines."
    )


@function_tool()
async def web_search_tool(query: str, search_depth: str = "advanced", max_results: int = 5) -> dict:
    """
    Perform a web search using the Tavily API.

    Args:
        query (str): The search query.
        search_depth (str): "basic" (faster) or "advanced" (more comprehensive).
        max_results (int): Number of results to return (default 5, max 10).

    Returns:
        dict: Search results with titles, URLs, and snippets.
    """
    try:
        response = await asyncio.to_thread(
            tavily_client.search,
            query=query,
            search_depth=search_depth,
            max_results=max_results
        )
        return {"success": True, "results": response}
    except Exception as e:
        logging.error(f"Error performing web search: {e}")
        return {"success": False, "error": str(e), "results": []}


@function_tool()
def extract_content(urls: list[str]) -> dict:
    """
    Extract content from a list of URLs using the Tavily API.

    Args:
        urls (list[str]): List of URLs to extract content from.

    Returns:
        dict: Extracted content for each URL.
    """
    try:
        response = tavily_client.extract(urls)
        return {"success": True, "data": response}
    except Exception as e:
        logging.error(f"Error extracting content: {e}")
        return {"success": False, "error": str(e), "data": {}}
