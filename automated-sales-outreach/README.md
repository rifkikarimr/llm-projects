# 📧 Sales Agent Automation

Automated cold email generation and sending using **OpenAI Agents SDK** and **Resend API**.

## 🎯 Features

- ✅ **Multi-Agent System**: 3 specialized sales agents (Professional, Engaging, Concise)
- ✅ **Intelligent Selection**: Sales Manager picks the best draft
- ✅ **Automated Formatting**: Auto-generates subject line and HTML
- ✅ **Resend Integration**: Sends emails via Resend API
- ✅ **Streamlit UI**: Simple web interface for automation

## 🏗️ Architecture

```
User Input → Sales Manager
    ↓
    ├─→ Professional Agent (Draft A)
    ├─→ Engaging Agent (Draft B)
    └─→ Concise Agent (Draft C)
    ↓
Sales Manager Selects Best Draft
    ↓
Email Manager (Handoff)
    ├─→ Subject Writer
    ├─→ HTML Converter
    └─→ Send via Resend API
    ↓
✅ Email Sent!
```

## 📦 Installation

### 1. Clone Repository

```bash
git clone <your-repo-url>
cd sales-automation
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install OpenAI Agents SDK

```bash
# If available via git:
pip install git+https://github.com/openai/openai-agents-sdk.git

# OR if available on PyPI:
pip install openai-agents
```

### 5. Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` file:

```bash
RESEND_API_KEY=re_your_actual_api_key
SENDER_EMAIL=your-verified-email@yourdomain.com
SENDER_NAME=Your Company Name
RECIPIENT_EMAIL=default@example.com
```

## 🚀 Usage

### Option A: Streamlit Web App

```bash
streamlit run app.py
```

Then open browser at `http://localhost:8501`

### Option B: Command Line

```bash
python sales_agent.py
```

## 🎨 Streamlit UI Guide

1. **Configuration Sidebar**
   - View API key status
   - See sender configuration

2. **Main Form**
   - **Recipient Email**: Target email address
   - **Recipient Name**: Name/title (e.g., "CEO", "John Doe")
   - **Your Name**: Your name in email signature
   - **Email Topic**: Main subject/pain point

3. **Click "Generate & Send Email"**
   - Watch progress bar
   - View agent output
   - Email sent automatically!

## 📁 Project Structure

```
sales-automation/
├── app.py                 # Streamlit web interface
├── sales_agent.py         # Core agent workflow
├── .env                   # Environment variables (git-ignored)
├── .env.example          # Template for .env
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## 🔧 Customization

### Change Agent Instructions

Edit in `sales_agent.py`:

```python
instructions_professional = (
    "You are a professional sales agent..."
    # Customize this prompt
)
```

### Add More Agents

```python
# In sales_agent.py
new_agent = Agent(
    name="Creative Agent",
    instructions="Your custom instructions...",
    model="gpt-4o-mini"
)

# Add to tools list
tools.append(new_agent.as_tool("new_agent", "Description"))
```

### Modify Email Template

Edit in `sales_agent.py` → `html_converter` instructions

## 🐛 Troubleshooting

### Error: "RESEND_API_KEY is missing"

✅ Make sure `.env` file exists and contains valid API key

### Error: "gmail.com domain not verified"

✅ Use Resend sandbox email: `onboarding@resend.dev`  
✅ Add your personal email to Resend dashboard as verified recipient

### Error: "Event loop is already running"

✅ Already handled in code with `nest_asyncio`  
✅ Restart Streamlit if issue persists

## 📚 Learning Resources

- [OpenAI Agents SDK Docs](https://github.com/openai/openai-agents-sdk)
- [Resend API Docs](https://resend.com/docs)
- [Streamlit Docs](https://docs.streamlit.io)

## 🎓 Next Steps (Option B & C)

**Option B - Advanced Features:**
- Email preview before sending
- Draft comparison (side-by-side)
- Email history log
- Custom CSS styling

**Option C - Learning Deep Dive:**
- Detailed code explanations
- Best practices walkthrough
- Production deployment guide

## 📝 License

MIT License

## 👨‍💻 Author

Built as part of AI Engineering learning journey 🚀