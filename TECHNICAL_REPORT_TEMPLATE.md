# CTSE Assignment 2: Technical Report Template

**Course**: SE4010 - CTSE (Collaborative Tagged Software Engineering)  
**Assignment**: Assignment 2 - Machine Learning Multi-Agent System  
**Team Size**: 4 Students  
**Submission Date**: [INSERT DATE]  

---

## 1. Problem Domain (1 page)

### 1.1 Problem Statement
The DevOps industry faces a critical challenge: pipeline failures are frequent, but the time required to identify root causes and generate solutions is significant. Teams often spend hours analyzing logs, searching for similar issues, and coordinating responses.

### 1.2 Current Challenges
- Manual error analysis is time-consuming
- Root causes often require domain expertise
- Solution generation is repetitive
- Communication delays during incidents
- Knowledge not systematized across team

### 1.3 Proposed Solution
A Multi-Agent System that autonomously:
- Executes and monitors pipelines in real-time
- Analyzes failures automatically
- Generates context-aware solutions
- Notifies team with actionable recommendations
- Logs all decisions for knowledge capture

---

## 2. System Architecture (1.5 pages)

### 2.1 High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│              CrewAI Multi-Agent Orchestration Layer             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌───────────────┐   ┌──────────────┐   ┌────────────────┐   │
│  │   Pipeline    │◄──┤   Error      │◄──┤   Solution     │   │
│  │   Monitor     │   │   Analyzer   │   │   Generator    │   │
│  │   Agent       │   │   Agent      │   │   Agent        │   │
│  └───────────────┘   └──────────────┘   └────────────────┘   │
│        │                   │                    │               │
│  Pipeline Exec       Error Parsing        Solution Gen     Notification
│  Tools              Tools                 Tools            Agent
│                                                                 │
│        Shared State Management (PipelineExecutionState)        │
│        Observability Layer (JSONL Event Logging)               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Agent Roles & Responsibilities

| Agent | Role | Input | Output | Tools |
|-------|------|-------|--------|-------|
| Pipeline Monitor | Execute pipeline stages | Stage names | Execution logs | execute_pipeline_stage() |
| Error Analyzer | Analyze failures | Logs | Error category, root cause | parse_error_log() |
| Solution Generator | Generate fixes | Error analysis | Fix steps, prevention tips | generate_fix_steps() |
| Notification Agent | Alert team | All context | Sent notification | send_notification() |

### 2.3 Workflow Diagram

```
Start
  │
  ├─ Agent 1: Execute Build ──► Success?
  │                              │
  │                              ├─ Yes: Continue
  │                              │
  │                              └─ No:
  │                                  │
  ├─ Agent 2: Analyze Error ◄──────┤
  │   - Parse logs
  │   - Categorize
  │   - Find root cause
  │
  ├─ Agent 3: Generate Solutions ◄─┤
  │   - Create fix steps
  │   - Prevention tips
  │
  ├─ Agent 4: Notify Team ◄─────────┤
  │   - Format message
  │   - Send email
  │
  └─ End
```

---

## 3. Agent Design (2 pages)

### 3.1 Agent 1: Pipeline Monitor

**System Prompt**:
```
You are a DevOps Pipeline Monitor Agent.
Your role is to:
1. Execute pipeline stages (Build, Lint, Test) in order
2. Monitor execution and capture all outputs
3. Detect failures immediately
4. Report complete execution status

Constraints:
- Execute stages sequentially
- Capture all stdout/stderr
- Stop on first failure
- Report stage durations
```

**Agent Constraints**:
- Timeout: 30 seconds per stage
- Execute order: Build → Lint → Test
- Mandatory failure reporting
- Complete output capture

**Interaction Strategy**:
- Receives: None (starter agent)
- Calls: execute_pipeline_stage() tool
- Passes to: Error Analyzer (if failed)
- Outputs: Detailed execution report

**Sample System Prompt in Code**:
```python
system_prompt = """You are a DevOps Pipeline Monitor Agent.
Your role is to:
1. Execute pipeline stages (Build, Lint, Test)
2. Monitor stage execution and capture outputs
3. Detect any failures or issues
4. Pass execution details to the next agent

Constraints:
- Always execute stages in correct order
- Capture complete output and error logs
- Stop immediately on failure
- Report all execution details clearly"""
```

---

### 3.2 Agent 2: Error Analyzer

**System Prompt**:
```
You are an Error Analysis Specialist Agent.
Your role is to:
1. Receive pipeline execution logs
2. Parse and analyze error messages
3. Categorize error types
4. Determine root causes

Constraints:
- Analyze ONLY provided context
- Be concise in root cause analysis
- Categorize: build_error, test_error, lint_error, unknown_error
- Assess severity: low, medium, high, critical
```

**Agent Constraints**:
- Input validation required
- Error categorization mandatory
- Severity levels defined
- Root cause must be specific

**Interaction Strategy**:
- Receives: Execution logs from Agent 1
- Calls: parse_error_log(), categorize_error() tools
- Passes to: Solution Generator
- Outputs: Structured error analysis

---

### 3.3 Agent 3: Solution Generator

**System Prompt**:
```
You are a Solution Generation Expert Agent.
Your role is to:
1. Receive error analysis
2. Generate specific fix steps
3. Provide prevention recommendations
4. Estimate fix complexity

Constraints:
- Generate 3-5 specific, actionable steps
- Include prevention measures
- Keep solutions practical
- Estimate: simple, moderate, complex
```

**Agent Constraints**:
- Minimum 3 fix steps
- Actionability required
- Complexity estimation mandatory
- Prevention focused

**Interaction Strategy**:
- Receives: Error analysis from Agent 2
- Calls: generate_fix_steps() tool
- Passes to: Notification Agent
- Outputs: Comprehensive remediation plan

---

### 3.4 Agent 4: Notification Agent

**System Prompt**:
```
You are a Notification Coordination Agent.
Your role is to:
1. Format professional notification message
2. Send alert to team members
3. Include error details and solutions
4. Ensure clear, actionable communication

Constraints:
- Include pipeline ID and failed stage
- Provide top 5 recommendations
- Keep message concise
- Ensure professionalism
```

**Agent Constraints**:
- Message formatting required
- Recipient validation
- Delivery confirmation
- Error handling mandatory

**Interaction Strategy**:
- Receives: Complete context from all agents
- Calls: send_notification() tool
- Final agent in chain
- Outputs: Delivery confirmation

---

## 4. Custom Tools Description (1 page)

### 4.1 Pipeline Execution Tools

```python
def execute_pipeline_stage(stage_name: str, commands: List[str], 
                          timeout: int = 30) -> Tuple[bool, str, str]:
    """
    Execute a pipeline stage with given commands.
    
    Args:
        stage_name: Name of the stage (Build, Test, Lint)
        commands: List of shell commands to execute
        timeout: Timeout in seconds
    
    Returns:
        Tuple of (success: bool, output: str, error: str)
    
    Example:
        success, output, error = execute_pipeline_stage(
            "Build",
            ["npm install", "npm run build"],
            timeout=30
        )
        if not success:
            print(f"Build failed: {error}")
    """
```

**Type Hints**: Full coverage (input and output)  
**Docstring**: Complete with example  
**Error Handling**: Try-catch, timeout protection, input validation

### 4.2 Error Analysis Tools

```python
def categorize_error(error_message: str) -> Tuple[str, str]:
    """
    Categorize error and determine severity.
    
    Args:
        error_message: Error message to categorize
    
    Returns:
        Tuple of (category: str, severity: str)
        Categories: build_error, test_error, lint_error, unknown_error
        Severity: low, medium, high, critical
    """
```

### 4.3 Solution Generation Tools

```python
def generate_fix_steps(error_category: str, 
                      error_context: str) -> List[str]:
    """
    Generate fix steps for error.
    
    Args:
        error_category: Category of error
        error_context: Error context
    
    Returns:
        List of recommended fix steps (3-5 items)
    """
```

### 4.4 Notification Tools

```python
def send_notification(recipient: str, message: str, 
                     channel: str = "email") -> bool:
    """
    Send notification to recipient.
    
    Args:
        recipient: Recipient address/ID
        message: Message to send
        channel: Channel (email, slack, etc)
    
    Returns:
        Success status
    """
```

**All tools have**:
- ✅ Type hints for all parameters and returns
- ✅ Comprehensive docstrings with examples
- ✅ Error handling and logging
- ✅ Input validation
- ✅ Observable tool calls (logged)

---

## 5. State Management (1 page)

### 5.1 Global State Structure

```python
@dataclass
class PipelineExecutionState:
    execution_id: str
    pipeline_name: str
    start_time: datetime
    end_time: Optional[datetime]
    stages_executed: List[str]
    failed_stage: Optional[str]
    error_log: str

@dataclass
class ErrorAnalysisState:
    failed_stage: str
    raw_error: str
    root_cause: Optional[str]
    error_severity: str

@dataclass
class SolutionState:
    error_analysis: str
    recommendations: List[str]
    implementation_steps: List[str]
    confidence_score: float

@dataclass
class NotificationState:
    pipeline_id: str
    failed_stage: str
    recommendations: List[str]
    email_sent: bool
```

### 5.2 Context Passing Strategy

```
SharedContext (Singleton)
├── pipeline_state: PipelineExecutionState
├── error_state: ErrorAnalysisState
├── solution_state: SolutionState
├── notification_state: NotificationState
└── execution_history: List[Event]

Agent 1 ──write──> pipeline_state ──read──> Agent 2
Agent 2 ──write──> error_state ──read──> Agent 3
Agent 3 ──write──> solution_state ──read──> Agent 4
Agent 4 ──write──> notification_state
```

### 5.3 State Transitions

```
Initialization
    ↓
Agent 1: PipelineExecutionState (write)
    ↓
[Check for failure]
    ├─ Success: END
    └─ Failure:
        ↓
    Agent 2: ErrorAnalysisState (write)
        ↓
    Agent 3: SolutionState (write)
        ↓
    Agent 4: NotificationState (write)
        ↓
    END
```

**No context loss**: All data persisted in shared context throughout execution.

---

## 6. Evaluation Methodology (1 page)

### 6.1 Testing Strategy

#### Unit Tests (Per Agent)
- **Pipeline Monitor**: 6 tests
  - Successful stage execution
  - Failed stage handling
  - Timeout handling
  - Error categorization
  - Accuracy validation
  - Safety testing

- **Error Analyzer**: 7 tests
  - Error parsing
  - Error categorization
  - Severity assessment
  - Root cause extraction
  - Accuracy validation
  - Completeness testing

- **Solution Generator**: 8 tests
  - Fix step generation
  - Prevention tips
  - Complexity estimation
  - All error types
  - Completeness
  - Accuracy

- **Notification Agent**: 7 tests
  - Message formatting
  - Recommendation inclusion
  - Delivery testing
  - Error handling
  - Quality validation
  - Security testing

#### Integration Tests (3 tests)
- Pipeline Monitor → Error Analyzer flow
- Error Analyzer → Solution Generator flow
- Complete workflow (all 4 agents)

#### Performance Tests (3 tests)
- Tool response time (<1s)
- Reliability across iterations
- Edge case handling

**Total: 34 test cases**

### 6.2 Evaluation Methods

**Property-Based Testing**
- Input variations
- Edge cases (empty strings, very long, special chars)
- Invariant checking

**LLM-as-a-Judge Testing**
- Semantic accuracy of error analysis
- Quality of recommendations
- Relevance of solutions

**Security Testing**
- Error handling without crashes
- Input validation
- No sensitive data leakage

### 6.3 Performance Metrics

| Metric | Target | Actual |
|--------|--------|--------|
| Tool response time | <1s | [MEASURE] |
| Full pipeline | 2-5 min | [MEASURE] |
| State lookup | O(1) | [VERIFY] |
| Memory usage | <500MB | [MEASURE] |
| CPU overhead | <5% | [MEASURE] |

---

## 7. Results & Performance (0.5 pages)

### 7.1 Test Results
```
Test Suite: 34 tests
Passed: [__/34]
Failed: [__/34]
Skipped: [__/34]
Coverage: [__]%
```

### 7.2 Performance Results
[Insert measurements from actual runs]

### 7.3 Reliability Analysis
[Insert reliability statistics]

---

## 8. Individual Contributions

### Student 1: [Name]
**Agent Developed**: Pipeline Monitor Agent
- **System Prompt**: [Provided in src/agents.py:PipelineMonitorAgent]
- **Constraints**: Execute in order, capture all output, stop on failure
- **Tool Implemented**: `execute_pipeline_stage(stage_name, commands, timeout)`
  - Type Hints: Complete (stage_name:str, commands:List[str], timeout:int, returns:Tuple[bool,str,str])
  - Docstring: Complete with example usage
  - Error Handling: Try-catch, timeout protection, input validation
- **Test Cases**: PipelineMonitorAgentTests (6 tests)
  - test_execute_successful_stage()
  - test_execute_failed_stage()
  - test_execute_stage_timeout()
  - test_get_pipeline_status()
  - test_pipeline_monitor_tool_accuracy()
  - test_pipeline_monitor_error_safety()
- **Challenges**: [Describe]
- **Proof of Contribution**: [Attach git commit log]

### Student 2: [Name]
**Agent Developed**: Error Analyzer Agent
- **System Prompt**: [Provided in src/agents.py:ErrorAnalyzerAgent]
- **Constraints**: Analyze provided context, categorize errors, assess severity
- **Tool Implemented**: `parse_error_log(log_content)`, `categorize_error(error_message)`
  - Type Hints: Complete
  - Docstring: Complete with examples
  - Error Handling: Comprehensive
- **Test Cases**: ErrorAnalyzerAgentTests (7 tests)
  - test_parse_error_log_with_errors()
  - test_categorize_build_error()
  - test_categorize_test_error()
  - test_categorize_lint_error()
  - test_extract_root_cause()
  - test_error_analyzer_accuracy()
  - test_error_analyzer_completeness()
- **Challenges**: [Describe]
- **Proof of Contribution**: [Attach git commit log]

### Student 3: [Name]
**Agent Developed**: Solution Generator Agent
- **System Prompt**: [Provided in src/agents.py:SolutionGeneratorAgent]
- **Constraints**: Generate actionable steps, include prevention, estimate complexity
- **Tool Implemented**: `generate_fix_steps()`, `estimate_fix_complexity()`
  - Type Hints: Complete
  - Docstring: Complete with examples
  - Error Handling: Full coverage
- **Test Cases**: SolutionGeneratorAgentTests (8 tests)
  - test_generate_build_fix_steps()
  - test_generate_test_fix_steps()
  - test_generate_prevention_tips()
  - test_estimate_fix_complexity_*()
  - test_solution_generator_completeness()
  - test_solution_generator_accuracy()
- **Challenges**: [Describe]
- **Proof of Contribution**: [Attach git commit log]

### Student 4: [Name]
**Agent Developed**: Notification Agent
- **System Prompt**: [Provided in src/agents.py:NotificationAgent]
- **Constraints**: Professional formatting, include all details, ensure actionability
- **Tool Implemented**: `format_notification_message()`, `send_notification()`
  - Type Hints: Complete
  - Docstring: Complete with examples
  - Error Handling: Robust
- **Test Cases**: NotificationAgentTests (7 tests)
  - test_format_notification_message()
  - test_format_notification_includes_recommendations()
  - test_send_notification_success()
  - test_send_notification_error_handling()
  - test_notification_agent_message_quality()
  - test_notification_agent_security()
- **Challenges**: [Describe]
- **Proof of Contribution**: [Attach git commit log]

---

## 9. Repository & Resources

**GitHub Repository**: [INSERT LINK]
**Framework**: CrewAI  
**LLM**: Ollama (llama2)  
**Language**: Python 3.9+  
**License**: Academic Use

**Key Files**:
- `src/agents.py` - All 4 agent definitions
- `src/tools.py` - All custom tools
- `src/state_management.py` - State management
- `src/observability.py` - Logging & tracing
- `tests/test_agents.py` - All 34 test cases

---

## 10. Conclusion

This Multi-Agent System demonstrates:
- ✅ Multi-agent orchestration with 4 distinct agents
- ✅ Custom Python tools with comprehensive documentation
- ✅ State management without context loss
- ✅ Complete observability and logging
- ✅ Comprehensive testing (34 tests)
- ✅ Local execution (Ollama only)
- ✅ Professional architecture and design

The system successfully automates DevOps pipeline monitoring and provides autonomous solutions to team members.

---

**Report Version**: 1.0  
**Prepared by**: [Team Name]  
**Submission Date**: [INSERT DATE]  
**Word Count**: [~2000 words, 4-5 pages]
