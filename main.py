from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from .agent import process_agent_message
from google_auth_oauthlib.flow import Flow
import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
import json


class AgentRequest(BaseModel):
    message: str


app = FastAPI()

user_creds = {}


def get_calendar_service():
    if "token" not in user_creds:
        raise HTTPException(status_code=401, detail="User not authenticated")

    creds = Credentials.from_authorized_user_info(json.loads(user_creds["token"]))

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())


def get_google_flow():
    return Flow.from_client_config(
        {
            "web": {
                "client_id": os.getenv("GOOGLE_CLIENT_ID"),
                "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
                "redirect_uris": [os.getenv("GOOGLE_REDIRECT_URI")],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        },
        scopes=os.getenv("GOOGLE_SCOPES"),
        redirect_uri=os.getenv("GOOGLE_REDIRECT_URI"),
    )


@app.get("/login")
def login():
    flow = get_google_flow()
    authorization_url, state = flow.authorization_url(
        access_type="offline", include_granted_scopes="true"
    )
    return RedirectResponse(url=authorization_url)


@app.get("/redirect")
async def auth_redirect(code: str = Query(...)):
    flow = get_google_flow()
    flow.fetch_token(code=code)
    credentials = flow.credentials
    user_creds["token"] = credentials.to_json()
    print("user_creds", user_creds)
    return {"message": "Authentication successful", "token": credentials.token}


@app.post("/agent/chat")
async def agent_chat(request: AgentRequest):
    try:
        reply = await process_agent_message(request.message)
        return {"response": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def root():
    return {"message": "Hello World"}
