import os
from typing import Dict

import httpx
from agents import Agent, function_tool


@function_tool
def send_email(subject: str, html_body: str) -> Dict[str, str]:
    """Send an email with the given subject and HTML body"""
    resend_api_key = os.environ.get("RESEND_API_KEY")
    if not resend_api_key:
        raise ValueError("RESEND_API_KEY is not set")

    payload = {
        "from": "test@krmdev.site",  # put your verified sender here
        "to": ["rifkikarimr@gmail.com"],  # put your recipient here
        "subject": subject,
        "html": html_body,
    }
    headers = {
        "Authorization": f"Bearer {resend_api_key}",
        "Content-Type": "application/json",
    }

    with httpx.Client(timeout=10.0) as client:
        response = client.post("https://api.resend.com/emails", json=payload, headers=headers)

    if response.is_success:
        email_id = response.json().get("id", "unknown")
        print("Email response", response.status_code, email_id)
        return {"status": "success", "id": email_id}

    print("Email response", response.status_code, response.text)
    return {"status": "failure", "message": response.text}


INSTRUCTIONS = """You are able to send a nicely formatted HTML email based on a detailed report.
You will be provided with a detailed report. You should use your tool to send one email, providing the 
report converted into clean, well presented HTML with an appropriate subject line."""

email_agent = Agent(
    name="Email agent",
    instructions=INSTRUCTIONS,
    tools=[send_email],
    model="gpt-4o-mini",
)
