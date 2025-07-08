from dotenv import load_dotenv
from agents import Agent, Runner, function_tool
import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from typing import Optional
from datetime import datetime, timezone


load_dotenv()  # must run before importing agents
# OPENAI_API_KEY now lives in os.environ


def get_current_datetime_info() -> str:
    """Get current date and time information for the agent context."""
    now = datetime.now(timezone.utc)
    return f"Current date and time: {now.strftime('%Y-%m-%d %H:%M:%S UTC')} (Year: {now.year})"


CODE_PROMPT = (
    "You are a virtual executive assistant that helps schedule meetings and send emails using Google APIs."
    f"IMPORTANT: {get_current_datetime_info()} "
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
def get_current_date_time() -> str:
    """
    Get the current date and time information.
    This tool helps the agent understand what 'today', 'tomorrow', 'next week' means.
    """
    now = datetime.now(timezone.utc)
    return f"Current date and time: {now.strftime('%A, %B %d, %Y at %H:%M:%S UTC')} (Year: {now.year})"


@function_tool
def schedule_meeting(
    summary: str,
    start_time: str,
    end_time: str,
    location: Optional[str] = "Online",
    description: Optional[str] = "Scheduled by your virtual EA",
    attendee_emails: Optional[str] = "",
    timezone: Optional[str] = "UTC",
):
    """
    Schedule a meeting in Google Calendar using stored credentials.

    Args:
        summary: The meeting title/summary
        start_time: Start time in ISO 8601 format (e.g., '2025-07-13T09:00:00-07:00')
        end_time: End time in ISO 8601 format (e.g., '2025-07-13T10:00:00-07:00')
        location: Meeting location (default: "Online")
        description: Meeting description (default: "Scheduled by your virtual EA")
        attendee_emails: Comma-separated email addresses (default: "email@domain.com")
        timezone: Timezone for the event (default: "UTC")

    Returns:
        str: HTML link to the created calendar event
    """
    try:
        creds = get_google_credentials()
        service = build("calendar", "v3", credentials=creds)

        # Parse attendees if provided
        attendees = []
        if attendee_emails:
            email_list = [email.strip() for email in attendee_emails.split(",")]
            attendees = [{"email": email} for email in email_list if email]

        event = {
            "summary": summary,
            "location": location,
            "description": description,
            "start": {
                "dateTime": start_time,
                "timeZone": timezone,
            },
            "end": {
                "dateTime": end_time,
                "timeZone": timezone,
            },
            "attendees": attendees,
            "reminders": {"useDefault": True},
        }

        created_event = (
            service.events().insert(calendarId="primary", body=event).execute()
        )
        print("created_event", created_event)
        return (
            f"Meeting '{summary}' scheduled successfully: {created_event['htmlLink']}"
        )
    except Exception as e:
        print("error", e)
        return f"Error scheduling meeting: {str(e)}"


google_agent = Agent(
    name="Google agent",
    instructions=CODE_PROMPT,
    model="o3-mini",
    tools=[schedule_meeting],
)


async def process_agent_message(msg: str) -> str:
    """Run the agent and get the final answer."""

    result = await Runner.run(google_agent, msg)
    return result.final_output
