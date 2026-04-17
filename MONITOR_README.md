# DevOps Security Monitor - Multi-Pipeline Orchestration

A security-first DevOps system that starts with a **Security Monitor Agent**, then orchestrates and watches **3 realistic local pipelines** with built-in failure recovery.

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│         Security Monitor Agent (Starts First)                   │
│         🔐 Initialization → Load → Execute → Report             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Monitors 3 Parallel YAML Pipelines:                           │
│                                                                 │
│  Pipeline 1                Pipeline 2             Pipeline 3    │
│  ┌──────────────┐      ┌──────────────┐      ┌──────────────┐  │
│  │   DEPLOY     │      │    TEST      │      │  SECURITY    │  │
│  │              │      │              │      │              │  │
│  │ • Prepare    │      │ • Setup      │      │ • Dep Check  │  │
│  │ • Build      │      │ • Unit Tests │      │ • SAST Scan  │  │
│  │ • Deploy     │  →   │ • Int Tests  │  →   │ • Container  │  │
│  │ • Healthck   │      │ • Code Qual  │      │ • Licensing  │  │
│  └──────────────┘      └──────────────┘      └──────────────┘  │
│       ✓/✗                   ✓/✗                    ✓/✗          │
│                                                                 │
│  Auto-Retry on Failure → Continue Monitoring Loop              │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Comprehensive Report: Summary + Details + Retries     │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 📋 Pipeline Definitions

All pipelines are defined in **YAML** format for realism and portability:

### 1. **Deploy Pipeline** (`pipelines/deploy.yml`)
- **Purpose**: Production deployment with health checks  
- **Stages**: Prepare → Build → Deploy → Healthcheck
- **Timeout**: 60 seconds
- **Critical**: Yes (failures are tracked)
- **Retry**: Up to 2 attempts

### 2. **Test Pipeline** (`pipelines/test.yml`)
- **Purpose**: Continuous testing and code quality
- **Stages**: Setup → Unit Tests → Integration Tests → Code Quality
- **Timeout**: 60 seconds
- **Critical**: No (non-blocking)
- **Retry**: Up to 1 attempt

### 3. **Security Pipeline** (`pipelines/security.yml`)
- **Purpose**: Security scanning and vulnerability checks
- **Stages**: Dependency Check → SAST Scan → Container Scan → License Check
- **Timeout**: 60 seconds
- **Critical**: Yes (must pass)
- **Retry**: Up to 1 attempt

## 🚀 Quick Start

### Installation

```bash
# Navigate to project directory
cd "d:\Devops Agent"

# Install dependencies (including PyYAML for YAML parsing)
pip install -r requirements.txt
```

### Running the Monitor

```bash
# Run Security Monitor - starts agent first, executes all 3 pipelines
python monitor_main.py
```

## 📊 Execution Flow

### Phase 1: Loading Pipelines
- Security Monitor Agent initializes
- Loads all 3 YAML pipeline definitions from `pipelines/` directory
- Validates pipeline configurations

### Phase 2: Executing Pipelines
- Each pipeline runs independently
- Agent watches and logs each stage
- Auto-retry mechanism on failure (configurable per pipeline)
- Continues to next pipeline even if current fails (unless critical)
- Detailed output for each stage

### Phase 3: Report Generation
- Summary statistics (total, passed, failed, success rate)
- Detailed breakdown per pipeline
- Stage-by-stage results
- Retry attempts tracked
- Total execution time

## 🔄 Failure Handling

### Retry Logic
Each pipeline has configurable retry behavior:
- `retry_on_failure`: Enable/disable auto-retry
- `max_retries`: Number of retry attempts
- **On failure**: Pipeline re-executes from start
- **Monitoring continues**: Agent doesn't stop, watches all pipelines

### Critical Pipelines
- Marked with `critical: true` in YAML
- Failures are logged and reported
- Monitor continues (completeness over strictness)

### Example Output
```
▶ Starting Pipeline: Deploy (Attempt 1)
  Description: Production deployment with health checks

[STAGE 1/4] Prepare
  > echo [DEPLOY] Preparing deployment environment...
  [DEPLOY] Preparing deployment environment...
  > echo [DEPLOY] Versioning application...
  [DEPLOY] Versioning application...
  ✓ Stage passed (0.10s)

[STAGE 2/4] Build
  > echo [DEPLOY] Building Docker image...
  [DEPLOY] Building Docker image...
  ✓ Stage passed (0.20s)

✓ Pipeline PASSED: Deploy
```

## 🔧 Configuration

### Adding New Pipelines
1. Create `pipelines/myepipeline.yml`:
```yaml
name: My Pipeline
description: Pipeline description

stages:
  - name: Stage 1
    commands:
      - echo "Running stage 1"
      - python script.py

  - name: Stage 2
    commands:
      - echo "Running stage 2"

timeout: 60
retry_on_failure: true
max_retries: 1
critical: true
```

2. Re-run the monitor - new pipeline loads automatically

### Modifying Existing Pipelines
Edit the corresponding YAML file in `pipelines/` and re-run. Changes apply immediately.

## 📈 Features

✅ **Multi-Pipeline Orchestration**
- 3 independent, realistic pipelines
- Run in sequence with centralized monitoring

✅ **Automatic Failure Recovery**
- Retry logic built into each pipeline
- Configurable retry attempts
- Continues monitoring on failures

✅ **Real YAML Definitions**
- Realistic CI/CD pipeline format
- Portable across systems (runs locally on Windows/Linux/Mac)
- Human-readable configuration

✅ **Comprehensive Monitoring**
- Security Monitor Agent starts first
- Watches all pipeline execution
- Detailed event logging
- Real-time output display

✅ **Detailed Reporting**
- Phase-based execution display
- Success/failure metrics
- Retry tracking
- Execution times

## 📝 Exit Codes

- `0`: All pipelines passed
- `1`: One or more pipelines failed

## 🔐 Security Features

- Monitor Agent validates pipeline configurations
- Runs locally (no external dependencies)
- Timeout protection on all stages
- Comprehensive execution logging

## 📚 Project Structure

```
pipelines/
  ├── deploy.yml       # Deployment pipeline (critical)
  ├── test.yml         # Testing pipeline
  └── security.yml     # Security scanning pipeline

src/
  ├── monitor.py       # Security Monitor Agent (main orchestrator)
  ├── yaml_pipeline.py # YAML loader and executor
  ├── config.py        # Configuration management
  ├── observability.py # Execution logging
  └── ...

monitor_main.py        # New entry point - starts agent first
```

## 🎯 Next Steps

1. ✅ Run: `python monitor_main.py`
2. Watch: Security Monitor orchestrates 3 pipelines
3. Review: Comprehensive report at end
4. Customize: Add your own pipelines in `pipelines/` directory

---

**Agent starts first** → **Loads 3 YAML pipelines** → **Monitors execution** → **Handles failures** → **Reports results**
