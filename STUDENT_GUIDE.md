# Student Guide: Individual Contributions

This document explains how each student contributes uniquely to the multi-agent system.

## Overview

Each of the 4 students must complete THREE requirements:

1. **Build an Agent** - Design system prompt, constraints, and reasoning logic
2. **Build a Tool** - Create a custom Python tool with type hints and docstrings
3. **Implement Testing** - Write test cases to validate the agent's output

---

## Student 1: Pipeline Monitor Agent

### Role
"You are responsible for the first agent - the Pipeline Monitor Agent that executes and monitors CI/CD pipeline stages."

### 1. Agent Design

**File**: `src/agents.py` - `PipelineMonitorAgent` class

Your agent must:
- Execute shell commands safely
- Monitor execution progress
- Capture complete stdout/stderr
- Detect failures immediately
- Report execution status

**System Prompt Template**:
```python
system_prompt = """You are a DevOps Pipeline Monitor Agent.

Your role is to:
1. Execute pipeline stages (Build, Lint, Test) in correct order
2. Monitor each stage execution and capture all outputs
3. Detect failures immediately and report them
4. Provide complete execution summaries

Constraints:
- Execute stages SEQUENTIALLY (no parallelization)
- Capture ALL stdout and stderr
- STOP immediately on failure
- Report stage timing information
- Provide detailed error context if any stage fails

When executing stages, always:
1. Start with Build stage
2. Then run Lint stage
3. Finally run Test stage
4. Pass execution logs to next agent if failure occurs
"""
```

**Constraints**: What the agent MUST follow
- Execute in order: Build → Lint → Test
- Never skip stages
- Timeout: 30 seconds per stage
- Capture ALL output
- Report on failure immediately

**Interaction Strategy**: How it communicates
- Receives: None (it's the starting agent)
- Calls: Your tool (execute_pipeline_stage)
- Passes to: Error Analyzer Agent (via shared context)
- Output type: JSON with execution details

### 2. Custom Tool

**Tool**: `execute_pipeline_stage()`

```python
def execute_pipeline_stage(stage_name: str, 
                          commands: List[str], 
                          timeout: int = 30) -> Tuple[bool, str, str]:
    """
    Execute a pipeline stage with given shell commands.
    
    This tool safely executes a series of shell commands for a pipeline stage
    (Build, Lint, or Test), capturing all output and error messages.
    
    Args:
        stage_name: Name of the stage being executed (e.g., "Build", "Test")
        commands: List of shell commands to execute sequentially
        timeout: Maximum time in seconds to wait for the stage (default 30)
    
    Returns:
        Tuple of (success: bool, output: str, error: str)
        - success: True if all commands succeeded, False otherwise
        - output: All stdout captured during execution
        - error: Error message or stderr if failure occurred
    
    Raises:
        subprocess.TimeoutExpired: If stage execution exceeds timeout
    
    Example:
        >>> success, output, error = execute_pipeline_stage(
        ...     stage_name="Build",
        ...     commands=["echo 'Building...'", "npm run build"],
        ...     timeout=30
        ... )
        >>> if not success:
        ...     print(f"Build failed: {error}")
    
    Notes:
        - Commands execute one-by-one
        - First failure stops execution
        - Shell=True allows piping and redirects
        - Output is captured in real-time
    """
```

**Requirements**:
- ✅ Type hints: `str`, `List[str]`, `int` for inputs; `Tuple[bool, str, str]` for output
- ✅ Docstring: Full documentation with example
- ✅ Error handling: Try-catch block, timeout protection
- ✅ Logging: Call `obs_logger.log_tool_call()` and `obs_logger.log_tool_result()`
- ✅ Validation: Check stage_name is valid, commands is not empty

### 3. Test Cases

**File**: `tests/test_agents.py` - `PipelineMonitorAgentTests` class

Write these 6 test cases:

```python
def test_execute_successful_stage(self):
    """Test that successful command execution returns success=True"""
    
def test_execute_failed_stage(self):
    """Test that failed command returns success=False and error message"""
    
def test_execute_stage_timeout(self):
    """Test that timeout triggers failure after specified seconds"""
    
def test_get_pipeline_status(self):
    """Test that pipeline status returns correct information"""
    
def test_pipeline_monitor_tool_accuracy(self):
    """LLM-as-a-Judge: Validate tool outputs contain expected information"""
    
def test_pipeline_monitor_error_safety(self):
    """Security Test: Ensure tool handles errors without crashes"""
```

**Testing Tips**:
- Use real shell commands like `echo`, `dir`, `exit 1`
- Test both success and failure paths
- Test timeout behavior
- Verify output contains expected strings
- Check error messages are informative

### 4. Proof of Contribution

You must provide:
1. **GitHub Commit Log**: Show all commits with your name
2. **Code Review**: Link to pull request showing peer review
3. **Documentation**: Updated docstrings and example usage

---

## Student 2: Error Analyzer Agent

### Role
"You are responsible for analyzing pipeline errors, determining their root causes, and categorizing them."

### 1. Agent Design

**File**: `src/agents.py` - `ErrorAnalyzerAgent` class

Your agent must:
- Parse pipeline error logs
- Categorize error types (build, test, lint, unknown)
- Determine root causes
- Assess error severity
- Extract error context

**System Prompt**:
```python
system_prompt = """You are an Error Analysis Specialist Agent.

Your role is to:
1. Receive pipeline execution logs from Pipeline Monitor
2. Parse error messages from the logs
3. Categorize the error INTO ONE OF: build_error, test_error, lint_error, unknown_error
4. Determine the ROOT CAUSE of the error
5. Assess SEVERITY: low, medium, high, or critical

When analyzing errors:
- Focus ONLY on the provided error context
- Be SPECIFIC and CONCISE in root cause analysis
- Look for patterns: compilation, test assertions, style violations
- Consider common causes: missing dependencies, syntax errors, assertions

Output your analysis as:
1. Error Category (which type of error)
2. Severity Level (how critical)
3. Root Cause (what caused it)
"""
```

**Constraints**:
- Only analyze provided logs (no external knowledge)
- Categorize into exactly: build_error, test_error, lint_error, unknown_error
- Severity: low, medium, high, critical
- Root cause must be specific, not generic
- Never speculate beyond provided context

**Interaction Strategy**:
- Receives: Pipeline execution logs from Agent 1 (via shared context)
- Calls: Your tools (parse_error_log, categorize_error)
- Passes to: Solution Generator (via shared context)
- Output type: ErrorAnalysisState object

### 2. Custom Tools

**Tool 1**: `parse_error_log()`

```python
def parse_error_log(log_content: str) -> Dict[str, Any]:
    """
    Parse error messages from raw log content.
    
    This tool analyzes raw pipeline execution logs, identifies error lines,
    and extracts relevant context around errors.
    
    Args:
        log_content: Complete raw log output as string
    
    Returns:
        Dict containing:
        - error_count: int, number of error lines found
        - error_lines: List[str], individual error lines
        - context: str, surrounding context for errors
    
    Example:
        >>> result = parse_error_log("Build started\\nerror: syntax\\nBuild failed")
        >>> result['error_count']
        1
        >>> "syntax" in result['error_lines'][0]
        True
    """
```

**Tool 2**: `categorize_error()`

```python
def categorize_error(error_message: str) -> Tuple[str, str]:
    """
    Determine error type and severity level.
    
    Analyzes error message to categorize it as build, test, lint, or unknown error,
    and assesses severity from low to critical.
    
    Args:
        error_message: Error message to analyze
    
    Returns:
        Tuple of (category: str, severity: str)
        Categories: "build_error", "test_error", "lint_error", "unknown_error"
        Severity: "low", "medium", "high", "critical"
    
    Example:
        >>> cat, sev = categorize_error("error: syntax error in parser.py")
        >>> cat
        'build_error'
        >>> sev in ['low', 'medium', 'high', 'critical']
        True
    """
```

**Tool 3**: `extract_root_cause()`

```python
def extract_root_cause(error_context: str, 
                      error_category: str) -> str:
    """
    Determine likely root cause from error context and category.
    
    Args:
        error_context: Error message and surrounding context
        error_category: Pre-determined error category
    
    Returns:
        Root cause analysis as string (2-3 sentences)
    """
```

**Requirements**:
- ✅ Type hints: Complete on all parameters and returns
- ✅ Docstrings: Full documentation with examples
- ✅ Error handling: Handle malformed input gracefully
- ✅ Logging: Call observation logger for all tool calls

### 3. Test Cases

**File**: `tests/test_agents.py` - `ErrorAnalyzerAgentTests` class

Write these 7 test cases:

```python
def test_parse_error_log_with_errors(self):
    """Test parsing logs with error messages"""
    
def test_categorize_build_error(self):
    """Test categorizing compilation/build errors"""
    
def test_categorize_test_error(self):
    """Test categorizing test assertion failures"""
    
def test_categorize_lint_error(self):
    """Test categorizing code style violations"""
    
def test_extract_root_cause(self):
    """Test root cause extraction"""
    
def test_error_analyzer_accuracy(self):
    """LLM-as-a-Judge: Validate categorization accuracy"""
    
def test_error_analyzer_completeness(self):
    """Property-Based Test: All error log fields are captured"""
```

### 4. Proof of Contribution

Provide:
1. All 3 tools implemented in src/tools.py
2. All 7 test cases passing
3. Git history showing your commits

---

## Student 3: Solution Generator Agent

### Role
"You are responsible for generating actionable solutions and remediation steps."

### 1. Agent Design

**File**: `src/agents.py` - `SolutionGeneratorAgent` class

Your agent must:
- Receive error analysis from Error Analyzer
- Generate specific, actionable fix steps
- Provide prevention recommendations
- Estimate fix complexity
- Build remediation plan

**System Prompt**:
```python
system_prompt = """You are a Solution Generation Expert Agent.

Your role is to:
1. Receive error analysis (error type, root cause, severity)
2. Generate 3-5 SPECIFIC, ACTIONABLE fix steps
3. Provide PREVENTION recommendations for future
4. Estimate COMPLEXITY (simple, moderate, complex)

When generating solutions:
- Be SPECIFIC (not "check logs", but "check /var/log/build.log line 42")
- PRIORITIZE immediate fixes
- Include VERIFICATION steps
- Focus on PRACTICAL solutions
- Consider ROOT CAUSE when generating steps

Output format:
1. Fix Steps (numbered, specific, actionable)
2. Prevention Tips (3-5 recommendations)
3. Complexity Estimate
"""
```

**Constraints**:
- Minimum 3 fix steps, maximum 5
- All steps must be actionable (not vague)
- Prevention tips must be practical
- Complexity: simple, moderate, or complex
- Solutions must address root cause

**Interaction Strategy**:
- Receives: ErrorAnalysisState from Agent 2
- Calls: Your tools
- Passes to: Notification Agent (via shared context)
- Output type: SolutionState object

### 2. Custom Tools

**Tool 1**: `generate_fix_steps()`

```python
def generate_fix_steps(error_category: str, 
                      error_context: str) -> List[str]:
    """
    Generate specific steps to fix the error.
    
    Based on error category and context, generates 3-5 concrete fix steps
    that team can immediately implement.
    
    Args:
        error_category: Type of error (build_error, test_error, etc)
        error_context: Description of the error
    
    Returns:
        List of 3-5 fix steps (strings), each specific and actionable
    
    Example:
        >>> steps = generate_fix_steps(
        ...     "build_error",
        ...     "Missing module 'axios'"
        ... )
        >>> len(steps) >= 3
        True
        >>> "npm install" in steps[0].lower()
        True
    """
```

**Tool 2**: `generate_prevention_tips()`

```python
def generate_prevention_tips(error_category: str) -> List[str]:
    """
    Generate prevention tips to avoid similar errors.
    
    Args:
        error_category: Type of error
    
    Returns:
        List of 3-5 prevention recommendations
    """
```

**Tool 3**: `estimate_fix_complexity()`

```python
def estimate_fix_complexity(error_category: str, 
                           error_context_length: int) -> str:
    """
    Estimate how complex the fix will be.
    
    Args:
        error_category: Type of error
        error_context_length: Length of error description
    
    Returns:
        Complexity level: "simple", "moderate", or "complex"
    """
```

**Requirements**:
- ✅ Type hints on all parameters and returns
- ✅ Comprehensive docstrings with examples
- ✅ Validation of inputs
- ✅ Proper error handling
- ✅ Observability logging

### 3. Test Cases

**File**: `tests/test_agents.py` - `SolutionGeneratorAgentTests` class

Write these 8 test cases:

```python
def test_generate_build_fix_steps(self):
    """Test fix steps for build errors"""
    
def test_generate_test_fix_steps(self):
    """Test fix steps for test errors"""
    
def test_generate_prevention_tips(self):
    """Test prevention tips generation"""
    
def test_estimate_fix_complexity_simple(self):
    """Test complexity estimation for simple errors"""
    
def test_estimate_fix_complexity_moderate(self):
    """Test complexity estimation for moderate errors"""
    
def test_estimate_fix_complexity_complex(self):
    """Test complexity estimation for complex errors"""
    
def test_solution_generator_completeness(self):
    """Property-Based Test: All error types generate solutions"""
    
def test_solution_generator_accuracy(self):
    """LLM-as-a-Judge: Validate fix steps are relevant"""
```

### 4. Proof of Contribution

Provide:
1. All 3 tools in src/tools.py
2. All 8 tests passing
3. Git commits showing your work

---

## Student 4: Notification Agent

### Role
"You are responsible for formatting and sending notifications to the team with complete failure context and solutions."

### 1. Agent Design

**File**: `src/agents.py` - `NotificationAgent` class

Your agent must:
- Format professional notifications
- Include pipeline details, error summary, and solutions
- Send via email
- Ensure actionability and clarity
- Track delivery

**System Prompt**:
```python
system_prompt = """You are a Notification Coordination Agent.

Your role is to:
1. Receive complete failure context from all agents
2. Format PROFESSIONAL notification message
3. Send EMAIL to team members
4. Ensure team can ACT immediately on recommendations

When formatting notifications:
- INCLUDE: Pipeline ID, Failed Stage, Error Summary
- PROVIDE: Top 5 recommended fix steps
- BE CLEAR and PROFESSIONAL
- Make it ACTIONABLE (not vague)
- STRUCTURE clearly with sections

Email structure:
1. Subject: Include pipeline ID and failed stage
2. Header: Show severity and impact
3. Error Details: What failed and why
4. Solutions: Specific fix steps
5. Footer: Links to logs and documentation
"""
```

**Constraints**:
- Must include pipeline ID
- Must list specific fix steps
- Professional tone required
- Message must be <2000 chars
- Delivery must be confirmed

**Interaction Strategy**:
- Receives: Complete execution context from all agents
- Calls: Your tools
- Final agent in chain
- Output type: NotificationState object

### 2. Custom Tools

**Tool 1**: `format_notification_message()`

```python
def format_notification_message(pipeline_id: str, 
                               failed_stage: str,
                               error_summary: str,
                               recommendations: List[str]) -> str:
    """
    Format professional notification message.
    
    Structures failure information and recommendations into a clear,
    well-organized email message that team can act on immediately.
    
    Args:
        pipeline_id: Unique pipeline execution identifier
        failed_stage: Name of the stage that failed (e.g., "Build")
        error_summary: Brief summary of what went wrong
        recommendations: List of recommended fix steps (3-5 items)
    
    Returns:
        Formatted message ready to send (string)
    
    Example:
        >>> msg = format_notification_message(
        ...     "PIPE-001",
        ...     "Build",
        ...     "Compilation failed: missing module",
        ...     ["npm install", "npm run build"]
        ... )
        >>> "PIPE-001" in msg
        True
        >>> "Build" in msg
        True
    
    The message includes:
    - Alert header
    - Pipeline ID and stage name
    - Error details
    - Recommended fixes (numbered)
    - Footer with links
    """
```

**Tool 2**: `send_notification()`

```python
def send_notification(recipient: str, 
                     message: str,
                     channel: str = "email") -> bool:
    """
    Send notification to recipient via specified channel.
    
    Delivers formatted notification to team member via email, Slack, or other
    channel, with error handling and delivery confirmation.
    
    Args:
        recipient: Email address or user ID to receive notification
        message: Formatted notification message
        channel: Delivery channel: "email", "slack", "teams" (default: "email")
    
    Returns:
        Success: True if sent successfully, False otherwise
    
    Example:
        >>> success = send_notification(
        ...     "devops@example.com",
        ...     "Pipeline failed: Build stage...",
        ...     "email"
        ... )
        >>> if success:
        ...     print("Notification sent!")
    
    Security Considerations:
    - Never expose credentials in message
    - Validate email/recipient format
    - Log delivery attempts
    """
```

**Requirements**:
- ✅ Type hints: Complete
- ✅ Docstrings: Full with examples
- ✅ Error handling: Try-catch, input validation
- ✅ Logging: Observation logger calls
- ✅ Security: No credential exposure

### 3. Test Cases

**File**: `tests/test_agents.py` - `NotificationAgentTests` class

Write these 7 test cases:

```python
def test_format_notification_message(self):
    """Test basic message formatting"""
    
def test_format_notification_includes_recommendations(self):
    """Test that all recommendations are included"""
    
def test_send_notification_success(self):
    """Test successful notification sending"""
    
def test_send_notification_error_handling(self):
    """Test graceful error handling"""
    
def test_notification_agent_message_quality(self):
    """LLM-as-a-Judge: Validate message quality"""
    
def test_notification_agent_security(self):
    """Security Test: No sensitive data exposure"""
    
# Plus 1 additional comprehensive test
```

### 4. Proof of Contribution

Provide:
1. Both tools in src/tools.py
2. All 7 tests passing
3. Git commit history

---

## How to Track Your Work

### GitHub Commits
Each student should ensure their commits are clearly identified:

```
$ git log --author="Your Name"

commit abc123... (Your Tool Implementation)
commit def456... (Your Tests)
commit ghi789... (Agent Design)
```

### Pull Requests
Create individual PRs for:
1. Agent implementation
2. Tool implementation
3. Test implementation

### Documentation
Update with your name and contributions:
1. `TECHNICAL_REPORT_TEMPLATE.md` - Section 8
2. `README.md` - Contributor section

---

## Grading Criteria

Each student is graded on:

| Criterion | Excellent (90-100%) | Very Good (80-89%) | Good (70-79%) |
|-----------|-------------------|------------------|--------------|
| **Agent Design (20%)** | Exceptional prompt engineering, zero hallucinations | Strong design, effective prompts, rare hallucinations | Good design, effective prompts, occasional issues |
| **Custom Tool (20%)** | Flawless Python, strict type hinting, comprehensive docstrings | Well-written, good type hinting, good docstrings | Functional with basic type hinting |
| **Testing (10%)** | Comprehensive evaluation (property-based + LLM-as-Judge) | Strong evaluation script, effective tests | Adequate evaluation, misses some cases |

---

## FAQ

**Q: Can I use code from other sources?**  
A: No. All code must be original. Cite external resources in comments, but implement from scratch.

**Q: What if my tool fails?**  
A: It's okay - focus on proper error handling. The test should verify error handling works.

**Q: Can I modify other students' tools?**  
A: No. But you can request changes via PR comments.

**Q: How do I ensure uniqueness?**  
A: Each student has completely separate agent, tool, and test. Your agent isn't used by others.

---

**Good luck! Remember: Quality over quantity.**
