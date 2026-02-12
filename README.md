<div align="center">

# 🤖 Agentic AI Analytics Platform

**Autonomous multi-agent system for intelligent data scraping, analysis, and report generation — powered by CrewAI, FastAPI, and Azure cloud services.**

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![CrewAI](https://img.shields.io/badge/CrewAI-Multi--Agent-FF6B35?style=for-the-badge)](https://www.crewai.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Azure](https://img.shields.io/badge/Microsoft_Azure-0078D4?style=for-the-badge&logo=microsoftazure&logoColor=white)](https://azure.microsoft.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org)
[![Firecrawl](https://img.shields.io/badge/Firecrawl-Web%20Scraping-FF6600?style=for-the-badge)](https://firecrawl.dev)
[![LangSmith](https://img.shields.io/badge/LangSmith-Tracing-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)](https://smith.langchain.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

---

[Features](#-features) • [Architecture](#-architecture) • [Tech Stack](#-tech-stack) • [Getting Started](#-getting-started) • [Usage](#-usage) • [API Reference](#-api-reference)

</div>

---

## 📋 Overview

The **Agentic AI Analytics Platform** is a production-grade, full-stack application that orchestrates autonomous AI agents to perform end-to-end data analysis workflows — from web scraping and data extraction through deep analysis to structured Markdown report generation. Each agent operates with a defined role, goal, and toolset, collaborating seamlessly without human intervention.

Built with a **FastAPI** backend, **Streamlit** dashboard, and **Azure cloud infrastructure**, the platform demonstrates modern patterns for deploying multi-agent AI systems at scale.

---

## ✨ Features

- **Multi-Agent Orchestration** — Autonomous agent collaboration using CrewAI with role-based task delegation (scraping → analysis → report writing)
- **Intelligent Web Scraping** — Firecrawl-powered data extraction delivering clean, structured Markdown from any web source
- **RESTful API Layer** — FastAPI endpoints exposing agent workflows as reliable, documented API services
- **Real-Time Dashboard** — Streamlit-based UI for triggering analyses, monitoring agent activity, and viewing system performance metrics
- **Cloud-Native Persistence** — Azure PostgreSQL for structured transaction/action logging; Azure Blob Storage for archiving generated Markdown reports
- **Modular Architecture** — Clean separation of concerns with environment-based configuration and rigorous data validation
- **Comprehensive Logging** — Every agent action and transaction is tracked with full audit trail
- **LLM Observability** — LangSmith tracing for end-to-end visibility into agent reasoning, token usage, latency, and chain execution

---

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Streamlit Dashboard                     │
│            (Trigger Analysis • View Reports)             │
└──────────────────────┬──────────────────────────────────┘
                       │ HTTP
┌──────────────────────▼──────────────────────────────────┐
│                    FastAPI Backend                        │
│              (REST API • Validation • Auth)               │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│               CrewAI Agent Orchestration                  │
│  ┌──────────┐  ┌──────────────┐  ┌────────────────┐     │
│  │ Scraper  │→ │   Analyst    │→ │ Report Writer  │     │
│  │  Agent   │  │    Agent     │  │     Agent      │     │
│  │(Firecrawl│  └──────────────┘  └────────────────┘     │
│  └──────────┘                                            │
└──────┬──────────────────────┬───────────────┬───────────┘
       │                      │               │
       │                      │        ┌──────▼──────────┐
       │                      │        │    LangSmith    │
       │                      │        │   (Tracing &    │
       │                      │        │  Observability) │
       │                      │        └─────────────────┘
┌──────▼──────────────┐    ┌──▼──────────────────────────┐
│  Azure PostgreSQL   │    │     Azure Blob Storage       │
│  (Transaction Logs) │    │    (Markdown Reports)        │
└─────────────────────┘    └──────────────────────────────┘
```

---

## 🛠 Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **AI Orchestration** | CrewAI | Multi-agent design, task delegation, autonomous workflows |
| **Web Scraping** | Firecrawl | LLM-ready web extraction, structured Markdown output |
| **Backend** | FastAPI | REST API, request validation, endpoint management |
| **Frontend** | Streamlit | Interactive dashboard, real-time monitoring |
| **Database** | Azure PostgreSQL | Structured logging, transaction tracking, audit trails |
| **Object Storage** | Azure Blob Storage | Persistent archive for generated Markdown reports |
| **Observability** | LangSmith | LLM tracing, token analytics, latency monitoring, debugging |
| **Language** | Python 3.11+ | Core application language |
| **Validation** | Pydantic | Data modeling and request/response validation |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Azure account with PostgreSQL and Blob Storage provisioned
- OpenAI API key (or compatible LLM provider)
- Firecrawl API key ([firecrawl.dev](https://firecrawl.dev))

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/agentic-ai-analytics.git
cd agentic-ai-analytics

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Environment Configuration

Create a `.env` file in the project root:

```env
# LLM Configuration
OPENAI_API_KEY=your_openai_api_key

# Firecrawl Web Scraping
FIRECRAWL_API_KEY=your_firecrawl_api_key

# Azure PostgreSQL
AZURE_PG_HOST=your-server.postgres.database.azure.com
AZURE_PG_DATABASE=your_database
AZURE_PG_USER=your_username
AZURE_PG_PASSWORD=your_password

# Azure Blob Storage
AZURE_STORAGE_CONNECTION_STRING=your_connection_string
AZURE_STORAGE_CONTAINER=reports

# LangSmith Tracing
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langsmith_api_key
LANGCHAIN_PROJECT=agentic-ai-analytics
```

### Launch the Application

```bash
# Start the FastAPI backend
uvicorn app.main:app --reload --port 8000

# In a separate terminal, start the Streamlit dashboard
streamlit run dashboard/app.py
```

---

## 💡 Usage

### Via Dashboard

1. Navigate to `http://localhost:8501`
2. Select an analysis type and configure parameters
3. Trigger the agent workflow and monitor progress in real time
4. View generated reports and system performance metrics

### Via API

```bash
# Trigger an analysis workflow
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"target": "your_analysis_target", "depth": "comprehensive"}'

# Retrieve a generated report
curl http://localhost:8000/api/v1/reports/{report_id}
```

---

## 📡 API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/analyze` | Trigger a new agent analysis workflow |
| `GET` | `/api/v1/reports` | List all generated reports |
| `GET` | `/api/v1/reports/{id}` | Retrieve a specific report |
| `GET` | `/api/v1/logs` | View agent transaction logs |
| `GET` | `/api/v1/health` | System health check |

---

## 📁 Project Structure

```
agentic-ai-analytics/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── api/
│   │   └── routes/          # API endpoint definitions
│   ├── agents/
│   │   ├── scraper.py       # Firecrawl-powered web scraping agent
│   │   ├── analyst.py       # Data analysis agent
│   │   └── writer.py        # Report generation agent
│   ├── crews/
│   │   └── analysis_crew.py # CrewAI orchestration config
│   ├── models/              # Pydantic data models
│   └── services/
│       ├── database.py      # Azure PostgreSQL integration
│       └── storage.py       # Azure Blob Storage integration
├── dashboard/
│   └── app.py               # Streamlit dashboard
├── .env.example
├── requirements.txt
└── README.md
```

---

## 🔑 Key Design Decisions

- **Agent Specialization** — Each agent has a distinct role (e.g., "Senior Analyst") with scoped goals and tools, enabling focused task execution and clean handoffs between pipeline stages
- **Firecrawl for Scraping** — Purpose-built for LLM pipelines, Firecrawl returns clean Markdown instead of raw HTML — eliminating brittle parsing logic and feeding agents structured, ready-to-analyze content
- **Structured + Unstructured Storage** — PostgreSQL handles metadata, logs, and transaction records while Blob Storage persists the rich Markdown artifacts — a pattern well-suited for AI systems generating both structured telemetry and unstructured outputs
- **Environment-Driven Configuration** — All secrets and deployment-specific settings managed via environment variables with Pydantic validation, supporting seamless local-to-cloud transitions
- **LLM Observability with LangSmith** — Full tracing across every agent call provides visibility into reasoning chains, token consumption, and latency bottlenecks — critical for debugging and optimizing multi-agent workflows in production

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Built using CrewAI, FastAPI, and Azure**

</div>