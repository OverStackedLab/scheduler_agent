from dotenv import load_dotenv
from agents import Agent, Runner, function_tool
import os, asyncio
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


load_dotenv()  # must run before importing agents
# OPENAI_API_KEY now lives in os.environ
CODE_PROMPT = (
    "You are a virtual executive assistant that helps schedule meetings and send emails using Google APIs. "
    "When a user instructs you to schedule a meeting, you must call the 'schedule_meeting' function with appropriate parameters. "
    "Similarly, if the user asks you to send an email, call the 'send_email' function. "
    "Use clear, concise language. When a function call is needed, output a JSON-formatted call."
)


@function_tool
def get_weather(city: str) -> str:
    return f"The weather in {city} is sunny"


def get_google_credentials() -> Credentials:
    """
    Retrieve google credentials from the environment variables.
    """
    return Credentials(
        token=os.getenv("GOOGLE_ACCESS_TOKEN"),
        refresh_token="",
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.getenv("GOOGLE_CLIENT_ID"),
        client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    )


@function_tool
def schedule_meeting(message: str) -> str:
    """Add a Google Calendar event and return its link."""
    """
    Schedule a meeting in Google Calendar using stored credentials.
    start_time and end_time must be ISO 8601 strings.
    """
    creds = get_google_credentials()
    service = build("calendar", "v3", credentials=creds)
    event = {
        "summary": "Test Meeting",
        "location": "Online",
        "description": "Scheduled by your virtual EA",
        "start": {
            "dateTime": "2025-07-13T09:00:00-07:00",
            "timeZone": "UTC",
        },
        "end": {
            "dateTime": "2025-07-13T10:00:00-07:00",
            "timeZone": "UTC",
        },
        "attendees": [{"email": "overstacked@icloud.com"}],
        "reminders": {"useDefault": True},
    }
    created_event = service.events().insert(calendarId="primary", body=event).execute()
    print("created_event", created_event)
    return created_event["htmlLink"]


haiku_agent = Agent(
    name="Google agent",
    instructions=CODE_PROMPT,
    model="o3-mini",
    tools=[schedule_meeting],
)


async def process_agent_message(msg: str) -> str:
    """Run the agent and get the final answer."""
    result = await Runner.run(haiku_agent, msg)
    return result.final_output
