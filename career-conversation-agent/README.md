# Career Conversation Agent

An **AI-powered conversational agent** designed to represent my professional profile
and engage visitors in meaningful, career-related conversations.

This project simulates a chatbot that could be embedded into a personal website
or portfolio to interact with recruiters, potential clients, or collaborators.

---

## 🎯 Purpose

The goal of this project is to:
- Provide an interactive way to explore my professional background
- Answer questions about my career, skills, and experience
- Capture potential leads when users express interest
- Log unanswered questions for future improvement

---

## 🧠 Core Capabilities

- Answers career and experience-related questions using contextual data
- Maintains a consistent persona via system prompt engineering
- Captures user contact details through tool calling
- Records unanswered questions automatically
- Supports natural, conversational interactions

---

## 🧩 Architecture Overview

### Key Components

- **LLM (OpenAI)**  
  Generates conversational responses.

- **System Prompt**  
  Ensures the agent stays in character and represents my profile accurately.

- **Context Sources**
  - Personal summary (`summary.txt`)
  - LinkedIn profile data (`karim_linkedin.pdf`)

- **Tools (Function Calling)**
  - `record_user_details` — captures user email and context
  - `record_unknown_question` — logs questions the agent cannot answer

- **User Interface**
  - Gradio-based chat interface

---

## 🔧 Key Concepts Demonstrated

- System prompt engineering
- Tool calling (function calling)
- Context injection from documents
- Conversation state management
- Human-like conversational flow

---

## 🛠️ Tech Stack

- Python
- OpenAI API
- Gradio
- PyPDF
- External notification service (Pushover)

---

## ▶️ How It Works

1. A user interacts with the chat interface
2. The agent responds using career and experience context
3. If the agent cannot answer a question, the question is logged
4. If user interest is detected, contact details are captured via tools

---

## ⚠️ Environment Variables

Create a `.env` file (not committed to the repository):

```env
OPENAI_API_KEY=your_openai_api_key
PUSHOVER_TOKEN=your_pushover_token
PUSHOVER_USER=your_pushover_user
