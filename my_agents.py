from agents import Agent, ModelSettings
from agents.model_settings import ToolChoice
from my_tools.my_tools import web_search_tool, extract_content, user_info, dynamic_instructions
from my_config.gemini_config import llm_model


# -----------------------------
# Web Search Agent
# -----------------------------
web_search_agent = Agent(
    name="Web Search Agent",
    tools=[web_search_tool, extract_content, user_info],
    instructions="""
You are a deep web search agent.
Your role is to perform accurate and comprehensive searches across the web.

Guidelines:
1. Take the user’s query and run a web search.
2. Parameters:
   - search_depth: "basic" (quick) or "advanced" (multi-source).
   - max_results: default 5, maximum 10.
3. Return results in a clear, structured list:
   - Title
   - Source (URL)
   - Short, precise summary
4. If results are limited, note this transparently.
5. Never invent or hallucinate sources.
6. Use all given tools and hand off if required.
""",
    model=llm_model,
)


# -----------------------------
# Reflection Agent
# -----------------------------
reflection_agent = Agent(
    name="Reflection Agent",
    instructions="""
You are a reflection agent.
Your role is to analyze, critique, and refine outputs from other agents.

Guidelines:
1. Review responses for accuracy, clarity, completeness, and relevance.
2. Identify weaknesses (missing details, vague explanations, hallucinations, formatting issues).
3. Suggest improvements while preserving meaning.
4. If the response is already strong, confirm it and provide brief validation.
""",
    model=llm_model,
)


# -----------------------------
# Citations Agent
# -----------------------------
citations_agent = Agent(
    name="Citations Agent",
    instructions="""
You are a citations agent.
Your role is to verify sources and add proper citations to responses.

Guidelines:
1. Review content and identify claims, facts, or data that need sources.
2. Attach citations from provided URLs or references.
3. If no valid source is available, mark it as [source not found].
4. Use a consistent citation style (numbered [1], [2], [3]).
5. Place citations directly after relevant statements.
6. Provide a References list at the end of the response.
""",
    model=llm_model,
)


# -----------------------------
# Orchestrator Agent
# -----------------------------
orchestrator_agent = Agent(
    name="Orchestrator Agent",
    instructions=dynamic_instructions,
    tools=[
        web_search_agent.as_tool(
            tool_name="web_search_agent",
            tool_description="Performs deep and accurate web searches."
        ),
        citations_agent.as_tool(
            tool_name="citations_agent",
            tool_description="Adds citations and reference tracking to responses."
        ),
        reflection_agent.as_tool(
            tool_name="reflection_agent",
            tool_description="Reviews and refines outputs for clarity and accuracy."
        ),
    ],
    model_settings=ModelSettings(
        temperature=0.9,
        tool_choice="required"
    ),
    model=llm_model,
)


# -----------------------------
# Planner Agent
# -----------------------------
planner_agent = Agent(
    name="Planner Agent",
    instructions="""
You are a planner agent.
Your role is to:
1. Break down complex research questions into smaller, manageable parts.
2. Pass the structured tasks to the orchestrator agent.
""",
    handoffs=[orchestrator_agent],
    handoff_description="Break down complex research questions into smaller manageable parts.",
    model=llm_model,
)


# -----------------------------
# Conflict Detection Agent
# -----------------------------
conflict_detection_agent = Agent(
    name="Conflict Detection Agent",
    instructions="""
You are a conflict detection agent.
Your role is to:
1. Detect conflicting information in responses.
2. Clearly highlight differences, e.g.:
   - Source A says X
   - Source B says Y
3. Warn the user when there is disagreement between sources.
""",
    handoffs=[orchestrator_agent],
    handoff_description="Highlight conflicting information across sources.",
    model=llm_model,
)


# -----------------------------
# Requirement Gathering Agent
# -----------------------------
requirement_gathering_agent = Agent(
    name="Requirement Gathering Agent",
    instructions="""
You are a requirement gathering agent.
Your role is to:
1. Understand the user’s main query and context.
2. Ask clarifying questions if needed.
3. Gather all requirements before proceeding.
4. Pass the finalized requirements to the planner_agent or conflict_detection_agent.
""",
    handoff_description="Gather requirements for fulfilling the user query.",
    handoffs=[planner_agent, conflict_detection_agent],
    model=llm_model,
)
