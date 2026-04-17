# DevOps Helper Agent - Multi-Agent System

A locally-hosted **Multi-Agent System (MAS)** that autonomously monitors CI/CD pipelines, detects failures, analyzes root causes using AI, and generates actionable solutions with email notifications.

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                   Multi-Agent Orchestration (CrewAI)            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Agent 1               Agent 2              Agent 3   Agent 4   │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐  ┌──────────┐   │
│  │ Pipeline │───▶│  Error   │───▶│ Solution │─▶│   Alert  │   │
│  │ Monitor  │    │ Analyzer │    │Generator │  │ & Notify │   │
│  └──────────┘    └──────────┘    └──────────┘  └──────────┘   │
│       │               │                │             │          │
│       └───────────────┴────────────────┴─────────────┘          │
│                                                                 │
│        Shared State Management & Observability Logging          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 🎯 Core Features

### Multi-Agent Orchestration (15%)
- **4 Distinct Agents** with specialized roles
- Agents communicate via shared context
- Sequential task execution with state transitions
- CrewAI framework for orchestration

### Tool Integration (10%)
- Custom Python tools with type hints & docstrings
- Pipeline execution tools
- Error analysis tools  
- Solution generation tools
- Notification tools

### State Management (10%)
- Global context shared across all agents
- Dataclass-based state objects
- State transitions logged and tracked
- Zero context loss between agents

### Observability (10%)
- JSONL execution logs
- Event tracking (agent start/end, tool calls, decisions)
- Complete execution traces
- Performance metrics

## 📋 System Components

### 1. **Pipeline Monitor Agent**
- **Role**: Execute and monitor pipeline stages
- **Tools**: Pipeline execution, status monitoring
- **Output**: Execution logs with success/failure details

### 2. **Error Analyzer Agent**
- **Role**: Parse errors and determine root causes
- **Tools**: Log parsing, error categorization, severity assessment
- **Output**: Error analysis with root cause and severity

### 3. **Solution Generator Agent**
- **Role**: Create actionable remediation plans
- **Tools**: Fix step generation, prevention tips
- **Output**: Remediation plan with complexity assessment

### 4. **Notification Agent**
- **Role**: Alert team with solutions
- **Tools**: Message formatting, notification sending
- **Output**: Email with complete failure report

## ⚙️ Technical Stack

- **Framework**: CrewAI (multi-agent orchestration)
- **LLM Engine**: Ollama (local, no API keys)
- **Language**: Python 3.9+
- **State**: Dataclasses + JSON
- **Observability**: Custom JSONL logging

## 🚀 Quick Start

### Prerequisites
```bash
# 1. Install Ollama
# Download from https://ollama.ai
ollama serve

# 2. Pull model in new terminal
ollama pull llama2
```

### Setup
```bash
cd "d:\Devops Agent"
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Configure
cp .env.example .env
# Edit .env with your Gmail credentials
```

### Run Multi-Agent System
```bash
python main_mas.py run
```

### Run Tests
```bash
python main_mas.py run-tests
```

## 📁 Project Structure

```
d:\Devops Agent\
├── src/
│   ├── agents.py               # 4 Agent definitions (CrewAI)
│   ├── tools.py                # Custom tools for each agent
│   ├── state_management.py     # Shared context & state
│   ├── observability.py        # Logging & tracing
│   ├── config.py               # Configuration
│   ├── pipeline.py             # Pipeline executor
│   ├── analyzer.py             # Error analysis
│   ├── ai_agent.py             # Ollama integration
│   └── email_service.py        # Email notifications
├── tests/
│   └── test_agents.py          # Comprehensive test suite
├── pipeline/
│   ├── stages.py               # Pipeline stage definitions
│   └── __init__.py
├── logs/
│   └── observability/          # Execution logs
├── main_mas.py                 # Multi-agent entry point
├── main.py                     # Original entry point
├── requirements.txt
├── .env.example
├── README.md
└── ARCHITECTURE.md             # Detailed design doc
```

## 🧪 Testing

### Test Coverage
- **Pipeline Monitor**: Stage execution, timeouts, error handling
- **Error Analyzer**: Categorization, severity assessment, root cause
- **Solution Generator**: Fix steps, prevention tips, complexity
- **Notification Agent**: Message formatting, delivery
- **Integration**: Multi-agent data flow
- **Performance**: Tool response time, reliability

### Run Full Test Suite
```bash
python main_mas.py run-tests
```

### Test Evaluation Methods
- **Property-Based Testing**: Input variations, edge cases
- **LLM-as-a-Judge**: Semantic accuracy validation
- **Security Tests**: Error handling, data protection
- **Integration Tests**: Complete workflow validation

## 📊 State Management

### Execution Flow
```
PipelineExecutionState
    ↓
ErrorAnalysisState (if failed)
    ↓
SolutionState
    ↓
NotificationState
```

All states maintained in `shared_context` without loss of data.

## 🔍 Observability

### Logged Events
- `agent_start` - Agent begins task
- `agent_end` - Agent completes task
- `tool_call` - Agent invokes tool
- `tool_result` - Tool execution result
- `decision` - Agent decision point
- `state_transition` - Global state change

### View Logs
```bash
python main_mas.py show-logs
```

## 📧 Email Configuration

1. Go to [Google Account Security](https://mail.google.com/mail/u/0/accounts/rescueaccount)
2. Enable 2-factor authentication
3. Generate App Password for "Mail" and "Windows Device"
4. Add to `.env`:
```ini
EMAIL_SENDER=your-email@gmail.com
EMAIL_PASSWORD=your-16char-app-password
EMAIL_RECIPIENT=recipient@example.com
```

## 🔗 Integration with CI/CD

Can be integrated with:
- GitHub Actions
- GitLab CI
- Jenkins
- Azure Pipelines

By running as scheduled job or webhook trigger.

## 📚 Documentation

- [ARCHITECTURE.md](ARCHITECTURE.md) - Detailed technical design
- [QUICKSTART.md](QUICKSTART.md) - Setup guide
- [Agent Designs](src/agents.py) - Agent system prompts
- [Tool Specifications](src/tools.py) - Tool documentation

## 🎓 Academic Assignment

This project fulfills SE4010 - CTSE Assignment 2 requirements:
- ✅ Multi-agent system with 3-4 distinct agents
- ✅ Custom Python tools with type hints & docstrings
- ✅ State management across agents
- ✅ Observability & logging system
- ✅ Comprehensive testing suite
- ✅ Local execution (Ollama only)
- ✅ GitHub repository ready

## 📝 License

Academic use

---

**Created**: April 2026 | **Framework**: CrewAI | **LLM**: Ollama (Local)

