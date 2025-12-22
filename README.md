# LLM Projects

This repository is a collection of hands-on projects built while learning
**AI Agents and LLM Engineering**.

The goal of this repo is to serve as a **playbook and portfolio**
demonstrating practical implementations of:
- Large Language Models (LLMs)
- Agent-based architectures
- Tool calling and agent handoffs
- Multi-agent workflows
- Real-world AI automation use cases

Each subfolder represents an **independent project**
developed as part of structured learning and experimentation.

---

## 🧠 Tech Stack & Concepts

- Python
- OpenAI API
- OpenAI Agents SDK
- Async workflows
- Tool calling (function calling)
- Multi-agent orchestration
- Gradio (UI)
- External API integrations (Email, Notifications)

Dependency management is handled centrally using **uv** (`pyproject.toml` + `uv.lock`).

---

## 📂 Projects

### 1️⃣ Automated Sales Outreach
A multi-agent system that automatically generates, evaluates, formats,
and sends cold sales emails using AI agents with different personas.

**Key concepts:**
- Parallel agent execution
- Agent selection and decision making
- Agent-to-agent handoff
- Tool-based email delivery

📁 Folder: `automated-sales-outreach/`

---

### 2️⃣ Career Conversation Agent
An AI-powered conversational agent designed to represent a professional profile.
The agent answers career-related questions using personal background data
and captures potential leads via tool calling.

**Key concepts:**
- System prompt engineering
- Context injection (resume & LinkedIn data)
- Tool calling for lead capture
- Gradio-based chat interface

📁 Folder: `career-conversation-agent/`

---

## 🚀 Deployment Strategy

- **GitHub**: This repository acts as a learning archive and portfolio.
- **HuggingFace Spaces**: Each project is deployed independently
  as a standalone application.

---

## ⚠️ Notes

- Environment variables (`.env`) are intentionally excluded.
- Each project contains a `.env.example` to document required variables.

---

## 📌 Author

Built by **Rifki Karim**  
Learning path: AI Agents & LLM Engineering
