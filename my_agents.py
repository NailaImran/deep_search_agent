from agents import Agent, ModelSettings
from my_tools.my_tools import web_search_tool, extract_content, user_info, dynamic_instructions
from my_config.gemini_config import llm_model



web_search_agent = Agent(
    name="web search agent",
    tools=[web_search_tool, extract_content, user_info],
    instructions="You are web search agent. You have to search user quiery on website to find latest information.Create a Synthesis Agent that takes all research findings and organizes them into clear sections with themes, trends, and key insights rather than just listing facts.",
    model=llm_model)


reflection_agent = Agent(
    name="Reflection agent",
    instructions="You are reflection agent.",
    model=llm_model)


citations_agent = Agent(
    name="citations agent",
    instructions="You are citation agent. You have to add all refrence of your research.Add automatic citation tracking: every claim gets a numbered reference [1], [2], [3] with full source details at the end of the report.",
    model=llm_model)


web_search = web_search_agent.as_tool(
    tool_name="web_search_agent",
    tool_description="You are web search agent. You have to search user quiery on website to find latest information.."
)


reflection = reflection_agent.as_tool(
    tool_name="reflection_agent",
    tool_description="You are reflection agent.Add a Source Checker agent that rates sources as High (.edu, .gov, major news), Medium (Wikipedia, industry sites), or Low (blogs, forums) and warns users about questionable information."
)


citations = citations_agent.as_tool(
    tool_name="citations_agent",
    tool_description="You are citation agent. You have to add all refrence of your research.Add automatic citation tracking: every claim gets a numbered reference [1], [2], [3] with full source details at the end of the report."
)


orchestrator_agent: Agent = Agent(name="orchestrator_agent",
                     instructions="use given all tools web_search, citations and reflection to give deep research and give summary of answer you got.Don't ask user for further details.Use citation from citations. ",
                     tools=[web_search, citations, reflection],
                     model_settings=ModelSettings(temperature=0.9),
                     model=llm_model,
                     
) 

planner_agent: Agent = Agent(name="planner_agent",
                 instructions=" you are requested to break down Complex research questions to smaller, manageable parts, than you need to pass information to orchestrator agent.",
                 handoffs = [orchestrator_agent],
                 handoff_description = "You are planner agent you should break down complex research questions to smaller manageable parts.",
                 model=llm_model)                     

Conflict_Detection_agent: Agent = Agent(name="Conflict_Detection_agent",
                 instructions="When your agents find conflicting information, highlight it clearly: Source A says X, but Source B says Y and let users know there's disagreement.",
                 handoffs = [orchestrator_agent],
                 handoff_description = "When your agents find conflicting information, highlight it clearly: Source A says X, but Source B says Y and let users know there's disagreement.",
                 model=llm_model)                     


requirement_gathering_agent: Agent = Agent(name="requirement_gathering_agent",
                 instructions=" you are requested to gather all requirements for fulfilment of user quiery.",
                 handoff_description= "You are requested to gather all requirements for fulfilment of user quiery",
                 handoffs=[planner_agent,Conflict_Detection_agent],
                 model=llm_model)                     


