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
