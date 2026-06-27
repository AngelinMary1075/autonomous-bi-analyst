## Autonomous Business Intelligence Analyst (MCP + Agentic AI)
```markdown
Autonomous Business Intelligence Analyst (MCP + Agentic AI)

An AI-driven Business Intelligence platform that utilizes local LLMs and the Model Context Protocol (MCP) to autonomously triage, investigate, and analyze enterprise datasets. 

The platform follows a modular, agentic architecture designed for high security, low latency, and absolute data sovereignty by running completely on local hardware.



🚀 Key Features

* Zero-Shot Semantic Triage: Parses raw, unstructured analytical prompts to seamlessly isolate core business metrics, target timelines, and product categories.
* Autonomous Tool Orchestration: Leverages advanced **ReAct (Reasoning and Action)** framework logic to dynamically query local databases and generate data visualizations to build evidence-based context.
* Automated Standardized Reporting: Evaluates data payloads and autonomously compiles executive KPI summaries alongside structured JSON reports saved directly to the filesystem.
* Explainable AI (XAI) Audit Trail: Provides a highly deterministic trail of tool execution steps, forcing the model to verify its facts via database queries to completely eliminate LLM hallucinations.



🏗️ System Architecture & Workflow

The platform leverages a cyclical ReAct loop to process natural language requests down to executable actions:

[User Prompt] ──> [ReAct Agent Engine] ──> [MCP Tool Call]
                         ▲                         │
                         │                         ▼
                  [Final Answer] <─── [SQL / Data Observation]

```

1. **Reasoning**: The local model breaks down the user request and determines what data it lacks.
2. **Action**: The agent selects and triggers an MCP tool (e.g., executing a multi-table SQL join).
3. **Observation**: The system pipes the tool's raw data output back into the model's context window.
4. **Output**: The process loops until the agent reaches a definitive, evidence-backed conclusion.

---

## 🛠️ Prerequisites & Tech Stack

### Core Technologies

* **Language:** Python 3.10+
* **LLM Engine:** Ollama (Llama 3.2)
* **Frameworks:** FastAPI, Model Context Protocol (MCP), ReAct
* **Data Processing:** Pandas, SQLite3, Matplotlib

### System Requirements

1. **Ollama Installed & Running**: Ensure Ollama is running locally.
2. **Pull the Model**:
```bash
ollama pull llama3.2

```



---

## 📁 Repository Structure

```text
autonomous-bi-analyst/
│
├── data/
│   └── business_data.db       # Generated Local SQLite Database
│
├── src/
│   ├── __init__.py
│   ├── database.py            # Automated multi-table schema generator
│   ├── tools.py               # Modular MCP tool registry (SQL, Plots)
│   ├── agent.py               # Core ReAct loop & Ollama HTTP Client
│   └── main.py                # FastAPI endpoints gateway
│
├── requirements.txt           # Project dependencies
└── README.md                  # Project documentation

```

---

## 🏃‍♂️ Quickstart Guide

### 1. Set Up Your Environment

Clone the repository, open your terminal inside the root directory, and set up a virtual environment:

```bash
# Create a virtual environment
python -m venv venv

# Activate the environment
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# Mac/Linux:
source venv/bin/activate

```

### 2. Install Dependencies

```bash
pip install -r requirements.txt

```

### 3. Initialize the Database

Before running the API, generate your local mock database with historical sales and inventory datasets:

```bash
python -m src.database

```

### 4. Run the Application

Start the FastAPI server via Uvicorn:

```bash
uvicorn src.main:app --reload

```

The server will boot up and wait for requests on `http://127.0.0.1:8000`.

---

## 🧪 Testing the Agent

You can interact with your autonomous analyst by sending a raw JSON payload via terminal or API clients like Postman.

```powershell
Invoke-RestMethod -Uri "http://localhost:8000/analytics/ask" -Method Post -ContentType "application/json" -Body '{"prompt": "Which products are currently running low on stock? Do we have any immediate inventory risks?"}'

```

### Sample Terminal Audit Trail Output

```text
--- [Agent Step 1] ---
Thought: I need to inspect the inventory levels and check which products are falling below their restock thresholds.
Action: execute_sql_query(SELECT product_name, stock_level, restock_threshold FROM inventory WHERE stock_level < restock_threshold)

Observation: 
product_name    stock_level    restock_threshold
Ergonomic Chair 4              5

--- [Agent Step 2] ---
Thought: The database shows Ergonomic Chairs are below threshold. I can now compile my report.
Final Answer: Urgent attention required: Ergonomic Chairs are at a critical stock level of 4 units, dropping below the safety restock threshold of 5. It is recommended to initiate a reorder from suppliers immediately.

```

```
Why this is a great update:
* It keeps the code clean since we are leaving the `data/` folder out of GitHub entirely.
* It documents the **ReAct workflow** textually so recruiters or other developers instantly understand the "Agentic AI" aspect of your code.
* It gives clean copy-paste copy for your project profile!

```
