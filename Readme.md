# WorkIQ + Vertex AI Demo

A VS Code-friendly Python demo that uses:
- Google ADK as the orchestrator
- Gemini on Vertex AI as the model
- Microsoft WorkIQ as the MCP server
- Streamlit as the UI

## Repo contents

- `workiq_agent/agent.py` - ADK agent wired to WorkIQ MCP over stdio
- `streamlit_app.py` - simple polished demo UI
- `.vscode/launch.json` - run profiles for Streamlit and ADK Web
- `.env.example` - environment variable template

## Prerequisites

1. Python 3.10+
2. Node.js 18+ (includes npm and npx)
3. VS Code with Python extension
4. Google Cloud SDK (`gcloud`)
5. A Google Cloud project with Vertex AI enabled
6. A Microsoft 365 tenant that can grant WorkIQ admin consent
7. Microsoft 365 Copilot / WorkIQ access in the tenant

## Setup

### 1. Create and activate a virtual environment

#### Windows PowerShell
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

#### macOS / Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure WorkIQ

Choose one option.

#### Option A - use `npx` on demand (recommended)

```bash
npx -y @microsoft/workiq@latest version
npx -y @microsoft/workiq@latest accept-eula
```


### 4. Authenticate to Vertex AI locally

```bash
gcloud auth application-default login
```

### 5. Configure environment variables

Copy `.env.example` to `.env` and update the values.

#### Windows PowerShell
```powershell
copy .env.example .env
```

#### macOS / Linux
```bash
cp .env.example .env
```

Set at least:
- `GOOGLE_GENAI_USE_VERTEXAI=TRUE`
- `GOOGLE_CLOUD_PROJECT=your-project-id`
- `GOOGLE_CLOUD_LOCATION=us-central1`
- `VERTEX_MODEL=gemini-2.5-flash`

### 6. Run the demo

#### Streamlit UI
```bash
python -m streamlit run streamlit_app.py
```

#### ADK Web debug UI
```bash
adk web --no-reload
```

## Recommended test prompts

- `What meetings do I have this week?`
- `Summarize emails from Sarah about the budget`
- `Find documents I worked on yesterday`
- `Who is working on Project Alpha?`

## Recommended build order

1. Confirm WorkIQ runs in the terminal
2. Confirm `gcloud auth application-default login` is done
3. Run `adk web --no-reload` and verify MCP tool calls work
4. Run the Streamlit UI

## Notes

- This is a demo starter, not a production deployment.
- If `npx` is not found inside VS Code, restart VS Code after installing Node.js.
- If WorkIQ fails on first use, check tenant admin consent before debugging the Python code.
