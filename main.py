import chainlit as cl
from agents import Runner
from openai.types.responses import ResponseTextDeltaEvent
from my_tools.my_tools import UserContext
from my_agent_list.my_agents import requirement_gathering_agent


@cl.on_chat_start
async def start_chat():
    await cl.Message(content="👋 Hi! I’m your Research Assistant. What would you like me to find for you today?").send()


@cl.on_message
async def main(message: cl.Message):
    # Create user context (you can also make this dynamic later)
    user_context = UserContext(name="Abdullah", city="Karachi", topic="AI Engineer")

    # Run your agent pipeline with streaming
    result: Runner = Runner.run_streamed(requirement_gathering_agent, message.content, context=user_context)

    final_response = ""
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            delta = event.data.delta
            final_response += delta
            await cl.Message(content=delta, author="Agent").send()

    # Send final response as a complete message
    await cl.Message(content=f"✅ Final Answer:\n\n{final_response}").send()
