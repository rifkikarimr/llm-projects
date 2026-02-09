import os
import asyncio
import httpx
from typing import Dict, Optional
from dotenv import load_dotenv
import logging

from agents import Agent, Runner, trace, function_tool

# =========================
# LOGGING SETUP
# =========================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# =========================
# ENV SETUP
# =========================
load_dotenv(override=True)

RESEND_API_KEY = os.getenv("RESEND_API_KEY")
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "test@krmdev.site")
SENDER_NAME = os.getenv("SENDER_NAME", "ComplAI")

# Validation
if not RESEND_API_KEY:
    raise ValueError("❌ RESEND_API_KEY is missing in .env file")

# =========================
# SALES AGENT INSTRUCTIONS
# =========================
instructions_professional = (
    "You are a professional sales agent working for ComplAI, "
    "a SaaS product that helps companies achieve SOC2 compliance using AI. "
    "You write formal, professional cold emails. "
    "IMPORTANT: Do NOT use placeholders like [Your Contact Information]. "
    "Use realistic contact details: contact@complai.io, www.complai.io, +1 (555) 123-4567. "
    "Always end with a professional signature including: "
    "Best regards, [sender name], Sales Manager, ComplAI, contact@complai.io, www.complai.io"
)

instructions_engaging = (
    "You are a humorous and engaging sales agent working for ComplAI. "
    "You write witty, creative cold emails that encourage replies. "
    "IMPORTANT: Do NOT use placeholders like [Your Contact Information]. "
    "Use realistic contact details: contact@complai.io, www.complai.io, +1 (555) 123-4567. "
    "Always end with a friendly signature including: "
    "Cheers, [sender name], Sales Manager, ComplAI, contact@complai.io"
)

instructions_concise = (
    "You are a busy sales agent working for ComplAI. "
    "You write short, concise, straight-to-the-point cold emails. "
    "IMPORTANT: Do NOT use placeholders like [Your Contact Information]. "
    "Use realistic contact details: contact@complai.io, www.complai.io. "
    "Always end with a brief signature: "
    "[sender name], ComplAI | contact@complai.io"
)

# =========================
# SALES AGENTS
# =========================
sales_agent_professional = Agent(
    name="Professional Sales Agent",
    instructions=instructions_professional,
    model="gpt-4o-mini"
)

sales_agent_engaging = Agent(
    name="Engaging Sales Agent",
    instructions=instructions_engaging,
    model="gpt-4o-mini"
)

sales_agent_concise = Agent(
    name="Busy Sales Agent",
    instructions=instructions_concise,
    model="gpt-4o-mini"
)

# =========================
# EMAIL SENDING TOOLS
# =========================

# Global variable to store current recipient (will be set per workflow)
_CURRENT_RECIPIENT_EMAIL = None

async def _send_resend_email(payload: dict) -> Dict[str, str]:
    """Internal async function for Resend API calls"""
    headers = {
        "Authorization": f"Bearer {RESEND_API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.resend.com/emails",
                json=payload,
                headers=headers,
                timeout=10.0
            )
            
            if response.status_code == 200:
                email_id = response.json().get("id", "unknown")
                recipients_str = ", ".join(payload['to'])
                logger.info(f"✅ Email sent successfully to {recipients_str}: {email_id}")
                return {"status": "success", "id": email_id, "recipients": recipients_str}
            
            logger.error(f"❌ Email failed: {response.text}")
            return {"status": "failure", "message": response.text}
            
    except httpx.RequestError as e:
        logger.error(f"❌ Network error: {str(e)}")
        return {"status": "failure", "message": f"Network error: {str(e)}"}
    except Exception as e:
        logger.error(f"❌ Unexpected error: {str(e)}")
        return {"status": "failure", "message": f"Unexpected error: {str(e)}"}

def _create_send_email_tool():
    """Factory function to create send_html_email tool with current recipient"""
    
    @function_tool
    def send_html_email(subject: str, html_body: str) -> Dict[str, str]:
        """Send HTML email via Resend (sync wrapper for async function)"""
        # Use global recipient set by workflow (can be list or string)
        recipients = _CURRENT_RECIPIENT_EMAIL or os.getenv("RECIPIENT_EMAIL", "rifkikarimr@gmail.com")
        
        # Convert to list if string
        if isinstance(recipients, str):
            recipients = [recipients]
        
        recipients_str = ", ".join(recipients)
        logger.info(f"📧 Preparing to send email to: {recipients_str}")
        
        payload = {
            "from": f"{SENDER_NAME} <{SENDER_EMAIL}>",
            "to": recipients,  # Resend API accepts array of emails
            "subject": subject,
            "html": html_body
        }
        
        # Run async function in sync context
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # If loop is already running (e.g., in Streamlit), create new task
                import nest_asyncio
                nest_asyncio.apply()
            return loop.run_until_complete(_send_resend_email(payload))
        except RuntimeError:
            # Fallback: create new event loop
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(_send_resend_email(payload))
            loop.close()
            return result
    
    return send_html_email

# =========================
# EMAIL FORMATTER AGENTS (Static - reusable)
# =========================
subject_writer = Agent(
    name="Email Subject Writer",
    instructions="Write a compelling subject line for a cold sales email. Keep it under 60 characters.",
    model="gpt-4o-mini"
)

html_converter = Agent(
    name="HTML Converter",
    instructions=(
        "Convert a text email into a clean, professional HTML email with proper formatting. "
        "IMPORTANT RULES: "
        "1. Replace [Your Contact Information] with realistic contact details: "
        "   - Email: contact@complai.io "
        "   - Website: www.complai.io "
        "   - Phone: +1 (555) 123-4567 "
        "2. Use current year (2025) for copyright footer, not 2023. "
        "3. Use proper HTML structure with <p> tags for paragraphs. "
        "4. Add professional styling with proper spacing. "
        "5. Make signature block look professional with contact details. "
        "6. Do NOT include any placeholders like [Your Contact Information] in final output. "
        "7. Format the email with proper HTML structure including: "
        "   - Clean typography with good line-height "
        "   - Professional color scheme (dark text on white background) "
        "   - Proper spacing between sections "
        "   - Clickable email and website links "
        "8. Include a footer with: ComplAI | contact@complai.io | www.complai.io | © 2025 ComplAI"
    ),
    model="gpt-4o-mini"
)

subject_tool = subject_writer.as_tool("subject_writer", "Write email subject")
html_tool = html_converter.as_tool("html_converter", "Convert email to HTML")

# =========================
# HTML TEMPLATE HELPER
# =========================
def _get_email_template() -> str:
    """Get professional HTML email template"""
    from datetime import datetime
    current_year = datetime.now().year
    
    return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f4f4f4;">
    <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f4f4f4;">
        <tr>
            <td align="center" style="padding: 40px 20px;">
                <table width="600" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <!-- Header -->
                    <tr>
                        <td style="padding: 30px 40px; background-color: #2563eb; border-radius: 8px 8px 0 0;">
                            <h1 style="margin: 0; color: #ffffff; font-size: 24px; font-weight: bold;">ComplAI</h1>
                            <p style="margin: 5px 0 0 0; color: #e0e7ff; font-size: 14px;">SOC2 Compliance Made Simple</p>
                        </td>
                    </tr>
                    
                    <!-- Body Content (will be replaced) -->
                    <tr>
                        <td style="padding: 40px; color: #1f2937; font-size: 16px; line-height: 1.6;">
                            {{BODY_CONTENT}}
                        </td>
                    </tr>
                    
                    <!-- Footer -->
                    <tr>
                        <td style="padding: 30px 40px; background-color: #f9fafb; border-top: 1px solid #e5e7eb; border-radius: 0 0 8px 8px;">
                            <p style="margin: 0 0 10px 0; color: #6b7280; font-size: 14px;">
                                <strong>ComplAI</strong><br>
                                Email: <a href="mailto:contact@complai.io" style="color: #2563eb; text-decoration: none;">contact@complai.io</a><br>
                                Website: <a href="https://www.complai.io" style="color: #2563eb; text-decoration: none;">www.complai.io</a><br>
                                Phone: +1 (555) 123-4567
                            </p>
                            <p style="margin: 15px 0 0 0; color: #9ca3af; font-size: 12px;">
                                © {current_year} ComplAI. All rights reserved.
                            </p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
"""

def _create_emailer_agent():
    """Factory function to create Email Manager with current send tool"""
    send_tool = _create_send_email_tool()
    
    return Agent(
        name="Email Manager",
        instructions=(
            "You receive an email body, generate a subject, convert it to HTML, "
            "and send the email using tools."
        ),
        tools=[subject_tool, html_tool, send_tool],
        model="gpt-4o-mini",
        handoff_description="Format and send the selected email"
    )

# =========================
# SALES AGENTS TOOLS (Static - reusable)
# =========================
tools = [
    sales_agent_professional.as_tool("sales_agent_professional", "Write a professional cold sales email"),
    sales_agent_engaging.as_tool("sales_agent_engaging", "Write an engaging cold sales email"),
    sales_agent_concise.as_tool("sales_agent_concise", "Write a concise cold sales email"),
]

def _create_sales_manager():
    """Factory function to create Sales Manager with dynamic emailer agent"""
    emailer_agent = _create_emailer_agent()
    
    return Agent(
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
# MAIN WORKFLOW FUNCTION
# =========================
async def run_sales_workflow(message: str, recipient_email: Optional[str] = None) -> str:
    """
    Execute the sales agent workflow
    
    Args:
        message: The prompt for generating sales email
        recipient_email: Single email or comma-separated emails (e.g., "a@x.com, b@y.com")
        
    Returns:
        Final output from the workflow
    """
    global _CURRENT_RECIPIENT_EMAIL
    
    # Parse recipient emails
    if recipient_email:
        # Split by comma and clean up whitespace
        recipients = [email.strip() for email in recipient_email.split(',') if email.strip()]
    else:
        # Use default from environment
        default_email = os.getenv("RECIPIENT_EMAIL", "rifkikarimr@gmail.com")
        recipients = [default_email]
    
    # Set current recipient(s) for this workflow run
    _CURRENT_RECIPIENT_EMAIL = recipients
    
    recipients_str = ", ".join(recipients)
    logger.info(f"🚀 Starting workflow: {message}")
    logger.info(f"📧 Target recipient(s): {recipients_str}")
    
    # Create fresh sales manager with correct recipient binding
    sales_manager = _create_sales_manager()
    
    with trace("Automated Sales Outreach"):
        result = await Runner.run(sales_manager, message)
    
    logger.info("✅ Workflow completed")
    return result.final_output

# =========================
# STANDALONE EXECUTION
# =========================
async def main():
    """Main function for standalone execution"""
    message = "Send a cold sales email addressed to Dear CEO from Alice"
    result = await run_sales_workflow(message)
    print(f"\n✅ Automated Sales Outreach completed.\n{result}")

if __name__ == "__main__":
    asyncio.run(main())