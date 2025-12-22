import os
import json
import asyncio
import requests
from typing import Dict
from dotenv import load_dotenv

from agents import Agent, Runner, trace, function_tool
from openai.types.responses import ResponseTextDeltaEvent

# =========================
# ENV SETUP
# =========================
load_dotenv(override=True)
RESEND_API_KEY = os.getenv("RESEND_API_KEY")

# =========================
# SALES AGENT INSTRUCTIONS
# =========================
instructions1 = (
    "You are a professional sales agent working for ComplAI, "
    "a SaaS product that helps companies achieve SOC2 compliance using AI. "
    "You write formal, professional cold emails."
)

instructions2 = (
    "You are a humorous and engaging sales agent working for ComplAI. "
    "You write witty, creative cold emails that encourage replies."
)

instructions3 = (
    "You are a busy sales agent working for ComplAI. "
    "You write short, concise, straight-to-the-point cold emails."
)

# =========================
# SALES AGENTS
# =========================
sales_agent1 = Agent(
    name="Professional Sales Agent",
    instructions=instructions1,
    model="gpt-4o-mini"
)

sales_agent2 = Agent(
    name="Engaging Sales Agent",
    instructions=instructions2,
    model="gpt-4o-mini"
)

sales_agent3 = Agent(
    name="Busy Sales Agent",
    instructions=instructions3,
    model="gpt-4o-mini"
)

# =========================
# EMAIL SENDING TOOLS
# =========================
@function_tool
def send_email(body: str) -> Dict[str, str]:
    """Send a plain text email using Resend"""

    payload = {
        "from": "Rifki Karim <test@krmdev.site>",
        "to": ["rifkikarimr@gmail.com"],
        "subject": "Sales Email",
        "html": f"<p>{body}</p>"
    }

    headers = {
        "Authorization": f"Bearer {RESEND_API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        "https://api.resend.com/emails",
        json=payload,
        headers=headers
    )

    return {"status": "success"} if response.status_code == 202 else {
        "status": "failure",
        "message": response.text
    }

# =========================
# EMAIL FORMATTER AGENTS
# =========================
subject_writer = Agent(
    name="Email Subject Writer",
    instructions="Write a compelling subject line for a cold sales email.",
    model="gpt-4o-mini"
)

html_converter = Agent(
    name="HTML Converter",
    instructions="Convert a text email into a clean, professional HTML email.",
    model="gpt-4o-mini"
)

subject_tool = subject_writer.as_tool("subject_writer", "Write email subject")
html_tool = html_converter.as_tool("html_converter", "Convert email to HTML")

@function_tool
def send_html_email(subject: str, html_body: str) -> Dict[str, str]:
    """Send HTML email via Resend"""

    payload = {
        "from": "ComplAI <test@krmdev.site>",
        "to": ["rifkikarimr@gmail.com"],
        "subject": subject,
        "html": html_body
    }

    headers = {
        "Authorization": f"Bearer {RESEND_API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        "https://api.resend.com/emails",
        json=payload,
        headers=headers
    )

    return {"status": "success"} if response.status_code == 202 else {
        "status": "failure",
        "message": response.text
    }

emailer_agent = Agent(
    name="Email Manager",
    instructions=(
        "You receive an email body, generate a subject, convert it to HTML, "
        "and send the email using tools."
    ),
    tools=[subject_tool, html_tool, send_html_email],
    model="gpt-4o-mini",
    handoff_description="Format and send the selected email"
)

# =========================
# SALES MANAGER AGENT
# =========================
tools = [
    sales_agent1.as_tool("sales_agent1", "Write a cold sales email"),
    sales_agent2.as_tool("sales_agent2", "Write a cold sales email"),
    sales_agent3.as_tool("sales_agent3", "Write a cold sales email"),
]

sales_manager = Agent(
    name="Sales Manager",
    instructions=(
        "You are a sales manager at ComplAI. "
        "You must generate sales emails using the tools. "
        "Try all three agents and select the best one. "
        "Then hand off to Email Manager to format and send the email."
    ),
    tools=tools,
    handoffs=[emailer_agent],
    model="gpt-4o-mini"
)

# =========================
# MAIN WORKFLOW
# =========================
async def main():
    message = "Send a cold sales email addressed to Dear CEO from Alice"

    with trace("Automated Sales Outreach"):
        result = await Runner.run(sales_manager, message)

    print("\n✅ Automated Sales Outreach completed.")
    print(result.final_output)

# =========================
# ENTRY POINT
# =========================
if __name__ == "__main__":
    asyncio.run(main())
