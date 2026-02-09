import streamlit as st
import asyncio
from sales_agent import run_sales_workflow
import os
from dotenv import load_dotenv

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Sales Agent Automation",
    page_icon="📧",
    layout="centered"
)

# =========================
# LOAD ENV
# =========================
load_dotenv(override=True)

# =========================
# HEADER
# =========================
st.title("📧 Sales Agent Automation")
st.markdown("### Automated Cold Email Generation & Sending")
st.markdown("---")

# =========================
# SIDEBAR - CONFIG
# =========================
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Check API key
    if os.getenv("RESEND_API_KEY"):
        st.success("✅ Resend API Key: Loaded")
    else:
        st.error("❌ Resend API Key: Missing")
    
    st.markdown("---")
    
    # Sender info (read-only display)
    sender_name = os.getenv("SENDER_NAME", "ComplAI")
    sender_email = os.getenv("SENDER_EMAIL", "test@krmdev.site")
    
    st.info(f"**Sender:**\n\n{sender_name}\n\n{sender_email}")
    
    st.markdown("---")
    st.caption("💡 Edit `.env` file to change sender configuration")

# =========================
# MAIN FORM
# =========================
with st.form("email_form"):
    st.subheader("📝 Email Details")
    
    # Recipient Email (Multiple)
    recipient_email = st.text_area(
        "Recipient Email(s)",
        value=os.getenv("RECIPIENT_EMAIL", "rifkikarimr@gmail.com"),
        placeholder="email1@example.com, email2@example.com, email3@example.com",
        help="Enter one or multiple emails separated by commas",
        height=80
    )
    
    # Show parsed emails preview
    if recipient_email:
        parsed_emails = [email.strip() for email in recipient_email.split(',') if email.strip()]
        if len(parsed_emails) > 1:
            st.info(f"📧 **{len(parsed_emails)} recipients detected:** {', '.join(parsed_emails[:3])}{'...' if len(parsed_emails) > 3 else ''}")
        elif len(parsed_emails) == 1:
            st.info(f"📧 **1 recipient:** {parsed_emails[0]}")
    
    # Recipient Name
    recipient_name = st.text_input(
        "Recipient Name/Title",
        value="CEO",
        placeholder="John Doe / CEO",
        help="Name or title of the primary recipient"
    )
    
    # Sender Name (in email)
    sender_person = st.text_input(
        "Your Name (in email)",
        value="Alice",
        placeholder="Alice Johnson",
        help="Your name as it appears in the email"
    )
    
    # Email Topic
    email_topic = st.text_area(
        "Email Topic/Context",
        value="SOC2 compliance audit",
        placeholder="What is this email about?",
        help="Main topic or pain point to address",
        height=100
    )
    
    # Submit button
    submit_button = st.form_submit_button(
        "🚀 Generate & Send Email",
        use_container_width=True,
        type="primary"
    )

# =========================
# PROCESS FORM
# =========================
if submit_button:
    # Parse emails
    parsed_emails = [email.strip() for email in recipient_email.split(',') if email.strip()]
    
    # Validation
    if not parsed_emails:
        st.error("❌ Please enter at least one recipient email address")
    elif any("@" not in email for email in parsed_emails):
        st.error("❌ One or more email addresses are invalid")
    elif not email_topic.strip():
        st.error("❌ Please enter an email topic")
    else:
        # Build prompt
        prompt = f"Send a cold sales email addressed to Dear {recipient_name} from {sender_person} regarding {email_topic}."
        
        # Display info
        with st.expander("📋 Workflow Details", expanded=False):
            st.write(f"**Prompt:** {prompt}")
            st.write(f"**Recipients ({len(parsed_emails)}):**")
            for idx, email in enumerate(parsed_emails, 1):
                st.write(f"  {idx}. {email}")
        
        # Show progress
        with st.spinner("🤖 AI Agents are working..."):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # Update progress
                status_text.text("⏳ Generating 3 email drafts...")
                progress_bar.progress(25)
                
                # Run workflow
                result = asyncio.run(run_sales_workflow(prompt, recipient_email))
                
                # Update progress
                status_text.text("⏳ Selecting best draft...")
                progress_bar.progress(50)
                
                status_text.text("⏳ Formatting HTML...")
                progress_bar.progress(75)
                
                status_text.text("⏳ Sending email...")
                progress_bar.progress(90)
                
                # Complete
                progress_bar.progress(100)
                status_text.text("✅ Complete!")
                
                # Show success
                if len(parsed_emails) > 1:
                    st.success(f"✅ Email sent successfully to **{len(parsed_emails)} recipients**!")
                else:
                    st.success(f"✅ Email sent successfully to **{parsed_emails[0]}**!")
                
                # Show result
                with st.expander("📄 Agent Output", expanded=True):
                    st.markdown(result)
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.exception(e)

# =========================
# FOOTER
# =========================
st.markdown("---")
st.caption("🤖 Powered by OpenAI Agents SDK + Resend API")