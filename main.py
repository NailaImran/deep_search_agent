from agents import Runner
import asyncio
import requests
from openai.types.responses import ResponseTextDeltaEvent
from my_tools.my_tools import UserContext
from my_agent_list.my_agents import requirement_gathering_agent
from dotenv import load_dotenv

load_dotenv()



async def main():

    user_context = UserContext(name="abdullah", city="Karachi", topic="AI engenier" )
    
    result: Runner = Runner.run_streamed(requirement_gathering_agent, input="tell me about future trend of Ai agents", context=user_context)
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta, end="", flush=True)


if __name__ == "__main__":

    asyncio.run(main())
          