# Deep Research

Multi-agent research workflow with a Gradio UI. The app plans web searches, summarizes results, writes a detailed markdown report, and sends the final report by email.

## What it does

1. Accepts a research query from the UI.
2. Creates a search plan (5 searches by default).
3. Runs searches concurrently with `WebSearchTool`.
4. Synthesizes all results into a long-form markdown report.
5. Converts/sends the report by running the email agent tool (Resend API).

The UI streams progress updates while the workflow runs.

## Architecture

- `deep_research.py`
  - Gradio entrypoint and async runner.
- `research_manager.py`
  - Orchestrates plan -> search -> write -> email.
  - Emits OpenAI trace URL and status messages.
- `planner_agent.py`
  - Produces a structured `WebSearchPlan` (`HOW_MANY_SEARCHES = 5`).
- `search_agent.py`
  - Uses `WebSearchTool(search_context_size="low")` for each planned query.
- `writer_agent.py`
  - Generates structured `ReportData`:
    - `short_summary`
    - `markdown_report`
    - `follow_up_questions`
- `email_agent.py`
  - Sends HTML email via Resend (`https://api.resend.com/emails`).

## Requirements

- Python `>=3.12`
- Dependencies installed from the project root (`requirements.txt` or `pyproject.toml`)
- Environment variables:
  - `OPENAI_API_KEY`
  - `RESEND_API_KEY`

## Setup

From the project root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create/update `.env` in project root:

```dotenv
OPENAI_API_KEY=your_openai_key
RESEND_API_KEY=your_resend_key
```

## Configure email sender/recipient

Current sender/recipient are defined directly in `email_agent.py`:

- `payload["from"]`
- `payload["to"]`

Use a Resend-verified sender domain/address before running in production.

## Run

From the `deep-research` directory:

```bash
python3 deep_research.py
```

This opens the Gradio app in your browser (`ui.launch(inbrowser=True)`).

## Notes

- Search execution is concurrent with `asyncio`.
- Failed individual searches are skipped and do not stop the workflow.
- Final report is yielded in markdown and also sent by email.
