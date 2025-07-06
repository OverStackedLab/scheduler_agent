from dotenv import load_dotenv
from agents import Agent, Runner, function_tool
import os, asyncio

load_dotenv()  # must run before importing agents
# OPENAI_API_KEY now lives in os.environ


@function_tool
def get_weather(city: str) -> str:
    return f"The weather in {city} is sunny"


haiku_agent = Agent(
    name="Haiku agent",
    instructions="Always respond in haiku form",
    model="o3-mini",
    tools=[get_weather],
)


async def process_agent_message(msg: str) -> str:
    """Run the agent and get the final answer."""
    result = await Runner.run(haiku_agent, msg)
    return result.final_output
