# Automated Sales Outreach

An **AI-powered multi-agent sales outreach system**
that generates, evaluates, formats, and sends cold sales emails automatically.

This project simulates an **Automated SDR (Sales Development Representative)**
workflow using multiple AI agents with different writing styles and responsibilities.

---

## 🎯 Problem

Cold sales outreach is time-consuming and inconsistent.
Different tones (professional, humorous, concise) work better for different audiences,
but manually testing them is inefficient.

---

## 💡 Solution

This system uses **multiple AI agents** to:
1. Generate multiple versions of a cold sales email
2. Evaluate and select the most effective one
3. Format the email professionally
4. Send it automatically via an email API

---

## 🧠 Architecture Overview

### Agents Involved

| Agent | Responsibility |
|------|---------------|
| Professional Sales Agent | Writes formal, professional emails |
| Engaging Sales Agent | Writes witty, engaging emails |
| Busy Sales Agent | Writes concise, direct emails |
| Sales Manager | Orchestrates agents and selects the best email |
| Email Manager | Formats the email and sends it |

---

## 🔧 Key Concepts Demonstrated

- Parallel agent execution
- Agent-as-tool pattern
- Agent evaluation and decision-making
- Agent handoff (Sales Manager → Email Manager)
- External API integration (email delivery)

---

## 🛠️ Tools & Integrations

- OpenAI Agents SDK
- Resend Email API
- Async agent orchestration
- Tool calling

---

## ▶️ How It Works (High Level)

1. Sales Manager asks multiple sales agents to generate emails
2. Sales Manager evaluates all responses
3. Best email is selected
4. Email Manager generates subject & HTML
5. Email is sent via API

---

## ⚠️ Environment Variables

Create a `.env` file (not committed):

```env
OPENAI_API_KEY=your_openai_api_key
RESEND_API_KEY=your_resend_api_key
