# Architecture & Design Document

## 1. System Overview

### Problem Domain
DevOps teams spend significant time analyzing pipeline failures and determining root causes. This Multi-Agent System automates:
- Pipeline execution and monitoring
- Error detection and categorization
- Root cause analysis
- Solution generation
- Team notification

### Solution Design
A autonomous multi-agent system that orchestrates 4 specialized agents using CrewAI, where each agent has distinct responsibilities and tools.

## 2. Multi-Agent Architecture

### 2.1 Agent Roles & Responsibilities

#### Agent 1: Pipeline Monitor
**Purpose**: Execute and monitor CI/CD pipeline stages

**System Prompt**:
```
You are a DevOps Pipeline Monitor Agent.
Your role is to:
1. Execute pipeline stages (Build, Test, Lint)
2. Monitor stage execution and capture outputs
3. Detect any failures or issues
4. Pass execution details to the next agent
```

**Constraints**:
- Execute stages in order: Build → Lint → Test
- Capture complete outputs
- Stop on failure
- Report details clearly

**Tools**:
- `execute_pipeline_stage(stage_name, commands, timeout)` - Run commands
- `get_pipeline_status(execution_id)` - Get execution status

**Output**: Detailed pipeline execution report with all outputs or failure details

---

#### Agent 2: Error Analyzer
**Purpose**: Analyze pipeline failures and determine root causes

**System Prompt**:
```
You are an Error Analysis Specialist Agent.
Your role is to:
1. Receive pipeline logs
2. Parse and analyze error messages
3. Categorize errors
4. Determine root causes
```

**Constraints**:
- Analyze provided context only
- Be concise and specific
- Categorize: build_error, test_error, lint_error, unknown_error
- Assess severity: low, medium, high, critical

**Tools**:
- `parse_error_log(log_content)` - Extract errors from logs
- `categorize_error(error_message)` - Determine error type & severity
- `extract_root_cause(error_context, error_category)` - Find root cause

**Output**: Error analysis with category, severity, and root cause

---

#### Agent 3: Solution Generator
**Purpose**: Generate actionable remediation plans

**System Prompt**:
```
You are a Solution Generation Expert Agent.
Your role is to:
1. Receive error analysis
2. Generate specific fix steps
3. Provide prevention recommendations
4. Estimate fix complexity
```

**Constraints**:
- Generate 3-5 specific steps
- Include prevention measures
- Keep solutions practical
- Estimate complexity
- Focus on immediate fixes

**Tools**:
- `generate_fix_steps(error_category, error_context)` - Create fix steps
- `generate_prevention_tips(error_category)` - Prevention recommendations
- `estimate_fix_complexity(error_category, context_length)` - Complexity assessment

**Output**: Remediation plan with fix steps, prevention tips, and complexity level

---

#### Agent 4: Notification Agent
**Purpose**: Alert team with complete failure context and solutions

**System Prompt**:
```
You are a Notification Coordination Agent.
Your role is to:
1. Receive failure context
2. Format professional notification
3. Send alert to team
4. Ensure communication is clear
```

**Constraints**:
- Include pipeline ID and failed stage
- Provide remediation steps
- Keep message concise but comprehensive
- Professional tone
- Ensure actionability

**Tools**:
- `format_notification_message(pipeline_id, stage, error, recs)` - Format message
- `send_notification(recipient, message, channel)` - Send via email/Slack

**Output**: Notification sent with complete failure report and remediation

### 2.2 Agent Orchestration Flow

```
INPUT: Pipeline Execution Request
    ↓
[Agent 1: Pipeline Monitor]
    ├─ Execute Build stage
    ├─ Execute Lint stage
    ├─ Execute Test stage
    └─ Capture success or failure
    ↓
[Check: Success?]
    ├─ Yes → Report success, exit
    └─ No ↓
         [Agent 2: Error Analyzer]
           ├─ Parse error logs
           ├─ Categorize error type
           └─ Determine root cause
         ↓
         [Agent 3: Solution Generator]
           ├─ Generate fix steps
           ├─ Generate prevention tips
           └─ Estimate complexity
         ↓
         [Agent 4: Notification Agent]
           ├─ Format notification
           ├─ Send to team
           └─ Log notification
         ↓
OUTPUT: Team Notified with Solutions
```

## 3. State Management

### 3.1 State Objects

```python
PipelineExecutionState
├── execution_id: str
├── pipeline_name: str
├── start_time: datetime
├── stages_executed: List[str]
├── failed_stage: Optional[str]
└── error_log: str

ErrorAnalysisState
├── failed_stage: str
├── raw_error: str
├── root_cause: Optional[str]
└── error_severity: str

SolutionState
├── error_analysis: str
├── recommendations: List[str]
├── implementation_steps: List[str]
└── confidence_score: float

NotificationState
├── pipeline_id: str
├── failed_stage: str
├── error_message: str
├── recommendations: List[str]
└── email_sent: bool
```

### 3.2 State Transitions

```
Initialization
    ↓
PipelineExecutionState (Agent 1)
    ↓
[If Failed]
    ↓
ErrorAnalysisState (Agent 2)
    ↓
SolutionState (Agent 3)
    ↓
NotificationState (Agent 4)
    ↓
Completion
```

All states accessible via `SharedContext` without context loss.

## 4. Tool Design

### 4.1 Tool Categories

**Pipeline Execution Tools**
- Execute shell commands safely
- Capture output and errors
- Handle timeouts
- Type hints: Full coverage
- Docstrings: Complete

**Error Analysis Tools**
- Parse structured logs
- Categorize errors
- Extract context
- Type hints: Full coverage
- Docstrings: Complete

**Solution Generation Tools**
- Generate fix procedures
- Prevention recommendations
- Complexity assessment
- Type hints: Full coverage
- Docstrings: Complete

**Notification Tools**
- Format messages
- Send notifications
- Track delivery
- Type hints: Full coverage
- Docstrings: Complete

### 4.2 Tool Error Handling

All tools implement:
- Try-catch blocks
- Graceful degradation
- Detailed error logging
- Type validation
- Input sanitization

## 5. Observability & Logging

### 5.1 Event Types

```
EventType
├── AGENT_START - Agent begins task
├── AGENT_END - Agent completes task
├── TOOL_CALL - Tool invocation
├── TOOL_RESULT - Tool result
├── DECISION - Agent decision
├── ERROR - Error event
└── STATE_TRANSITION - State change
```

### 5.2 Logging Output

JSONL format (one event per line):
```json
{
  "timestamp": "2026-04-15T10:30:45.123456",
  "event_type": "tool_call",
  "agent_name": "ErrorAnalyzer",
  "details": {
    "tool_name": "parse_error_log",
    "inputs": {"log_length": 1505},
    "status": "called"
  }
}
```

### 5.3 Execution Trace

Complete trace recoverable from logs for:
- Debugging
- Performance analysis
- Compliance audit
- Improvement insights

## 6. Individual Contributions

### Student 1: Pipeline Monitor
- **Agent**: PipelineMonitorAgent
- **Tool**: `execute_pipeline_stage()`
- **Tests**: PipelineMonitorAgentTests (6 test cases)

### Student 2: Error Analyzer
- **Agent**: ErrorAnalyzerAgent
- **Tool**: `parse_error_log()`, `categorize_error()`
- **Tests**: ErrorAnalyzerAgentTests (7 test cases)

### Student 3: Solution Generator
- **Agent**: SolutionGeneratorAgent
- **Tool**: `generate_fix_steps()`, `estimate_fix_complexity()`
- **Tests**: SolutionGeneratorAgentTests (8 test cases)

### Student 4: Notification Agent
- **Agent**: NotificationAgent
- **Tool**: `format_notification_message()`, `send_notification()`
- **Tests**: NotificationAgentTests (7 test cases)

## 7. Testing Strategy

### 7.1 Test Types

**Unit Tests**
- Individual tool functionality
- Edge case handling
- Error conditions

**Integration Tests**
- Multi-agent data flow
- State transitions
- Complete workflows

**Property-Based Tests**
- Input variations
- Edge cases
- Invariant checking

**LLM-as-a-Judge Tests**
- Semantic accuracy
- Output quality
- Constraint compliance

**Security Tests**
- Error handling
- Data protection
- Attack resistance

**Performance Tests**
- Tool response time
- Reliability across iterations
- Stress testing

### 7.2 Test Coverage

```
Pipeline Monitor:  6 tests
Error Analyzer:    7 tests
Solution Generator: 8 tests
Notification Agent: 7 tests
Integration:       3 tests
Performance:       3 tests
━━━━━━━━━━━━━━━━━━━━━━
Total:            34 tests
```

## 8. Robustness & Reliability

### Error Handling
- All exceptions caught
- Graceful degradation
- Clear error messages
- Logging for debugging

### State Consistency
- No context loss between agents
- Atomic state transitions
- Rollback on error
- History tracking

### Tool Reliability
- Timeout protection
- Input validation
- Output verification
- Retry logic

## 9. Deployment

### Local Execution
- No cloud dependencies
- Single machine
- No API keys required
- Ollama only

### Integration Points
- GitHub Actions
- GitLab CI
- Jenkins
- Direct scheduling

## 10. Performance Characteristics

- **Tool Response Time**: <1 second
- **Full Pipeline**: ~2-5 minutes (including LLM calls)
- **State Management**: O(1) lookup
- **Logging Overhead**: <1% CPU
- **Memory**: ~500MB for typical workload

## 11. Security Considerations

- Credential management via .env
- Input sanitization
- Command injection protection
- Log sanitization
- Email encryption ready

---

**Document Version**: 1.0  
**Created**: April 2026  
**Framework**: CrewAI  
**LLM**: Ollama (Local)
