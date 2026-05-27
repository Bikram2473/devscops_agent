# 🛡️ DevSecOps Incident Triage & Automated Runbook Agent

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-red.svg)
![LangGraph](https://img.shields.io/badge/LangGraph-Agentic-green.svg)
![Gemini](https://img.shields.io/badge/Gemini-2.5_Flash-orange.svg)

An autonomous, stateful triage pipeline that intercepts production failures, performs automated root-cause analysis (RCA), and generates contextualized engineering tickets. 
This project bridges the gap between system observability and developer workflows using LangGraph orchestration and the Model Context Protocol (MCP).

## ✨ Key Features

* **🧠 Stateful Agentic Workflow:** Uses LangGraph to manage the lifecycle of an incident, recursively routing tasks from error ingestion to diagnostic analysis and automated ticket creation.
* **🔌 Protocol-Driven Context (MCP):** Leverages the Model Context Protocol (MCP) to securely search GitHub commit logs, repository issues, and file structures without hardcoding sensitive API credentials.
* **🔍 Autonomous RCA:** Gemini 2.5 Flash performs structural analysis on raw stack traces, correlating failures with recent code changes to identify the breaking component in real-time.
* **⚡ One-Click Integration:** Bridges the gap between incident detection and developer action:
  * **Automated Triage:** Automatically files structured, high-context tickets in Linear/GitHub.
  * **Visual Triage Room:** Monitors incident status and agent reasoning logs in real-time via a Streamlit control center.
  * **Self-Healing Documentation:** Generates suggested remediation runbooks based on historical repository data.

## 🚀 Complete Installation & Setup

Follow these sequential terminal commands to stand up the project within a clean local environment:

### 1. Repository Preparation
```bash
git clone https://github.com/yourusername/devsecops-triage-agent.git
cd devsecops-triage-agent
```

### 2. Create a Virtual Environment
```bash
# For Windows
python -m venv venv
.\venv\Scripts\Activate.ps1

# For Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
```bash
# Get this from Google AI Studio
GOOGLE_API_KEY=your_gemini_api_key_here

# Required for MCP GitHub server to read commits and issues
GITHUB_PERSONAL_ACCESS_TOKEN=your_github_pat_here
```

### 5. Launch the Infrastructure
```bash
# Terminal 1 (The Backend WebHook)
uvicorn api:app --reload
```

```bash
# Terminal 2 (The Control Room):
streamlit run app.py
```

Open your web browser to http://localhost:8501 to monitor production incidents and trigger your first autonomous triage run!
