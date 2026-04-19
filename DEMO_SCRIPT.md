# Demo Video Script

**Duration**: 4-5 minutes (NOT beyond 5 minutes)  
**Target**: Show complete multi-agent system functioning locally

## Scene 1: Introduction (30 seconds)

```
[SCREEN: Title slide]
NARRATOR: "This is the DevOps Helper Agent - a Multi-Agent System that 
autonomously monitors CI/CD pipelines, detects failures, analyzes root causes,
and sends email notifications with recommended solutions.

All running locally with Ollama. No cloud APIs. No costs."

[SCREEN: Architecture diagram]
NARRATOR: "The system uses 4 agents working together:
1. Pipeline Monitor - executes and monitors stages
2. Error Analyzer - determines root causes
3. Solution Generator - creates fix recommendations
4. Notification Agent - alerts the team"
```

## Scene 2: System Startup (30 seconds)

```
[SCREEN: Terminal]
NARRATOR: "Let's start the system."

$ python main_mas.py check-config
✓ Email configured correctly
✓ Ollama is running

NARRATOR: "Configuration is verified. Now let's run a pipeline."
```

## Scene 3: Pipeline Execution - Success Case (45 seconds)

```
[SCREEN: Terminal running pipeline]

$ python main_mas.py run

============================================================
Starting Multi-Agent Pipeline Monitoring System
============================================================

[AGENT 1: Pipeline Monitor] ▶ Executing Build stage...
[OUTPUT] Building application... ✓ PASSED (2.1s)

[AGENT 1: Pipeline Monitor] ▶ Executing Lint stage...
[OUTPUT] Checking code style... ✓ PASSED (1.5s)

[AGENT 1: Pipeline Monitor] ▶ Executing Test stage...
[OUTPUT] Running tests... ✓ PASSED (3.2s)

============================================================
Pipeline Execution SUCCESSFUL ✓
============================================================

NARRATOR: "All stages passed successfully. The system detected
no issues and reported success."
```

## Scene 4: Pipeline Execution - Manual Run (60 seconds)

```
[SCREEN: Terminal]

$ python run_pipeline.py Test

============================================================
MANUAL PIPELINE EXECUTION
============================================================

✓ Build stage PASSED (2.1s)
✓ Lint stage PASSED (1.5s)
✗ Test stage FAILED

ERROR: Test assertion failed
Output: Expected 5 but got 3

PIPELINE FAILED at stage: Test
Failure report saved to: logs/last_pipeline_failure.json
You can now run 'python run_agent.py' to analyze this failure.

NARRATOR: "The pipeline is run manually. Here we see it failed 
at the Test stage. I have now disconnected the agent from the 
live pipeline run to show you how the AI system works independently."
```

## Scene 5: Starting the Agentic AI System (60 seconds)

```
[SCREEN: Terminal]

$ python run_agent.py

============================================================
AGENTIC AI SYSTEM - TRIGGERED ANALYSIS
============================================================

STARTING AI ANALYSIS FOR PIPELINE: 20260417_214530

[AGENT 2: Error Analyzer] ▶ Analyzing error...
  ├─ Parsing error logs...
  ├─ Error Category: test_error
  ├─ Severity: HIGH
  └─ Root Cause: "Test assertion failure - logic mismatch"

NARRATOR: "Now I trigger the Agentic AI system manually. 
It picks up the failure report and starts its multi-agent chain."
```

NARRATOR: "The Error Analyzer parsed the logs and determined:
- This is a test error (not a build or lint issue)
- Severity is HIGH
- Root cause is an assertion failure in the test logic

Now the Solution Generator takes over."

[AGENT 3: Solution Generator] ▶ Generating solutions...
  ├─ Analyzing fix strategies...
  ├─ Fix Complexity: MODERATE
  └─ Recommendations:
      1. Review test assertions and expected values
      2. Debug failing test with print statements
      3. Check test data mocks are correct
      4. Run test in isolation to identify conflicts
      5. Check for timing or async issues

NARRATOR: "The Solution Generator created 5 specific fix steps
based on the error analysis. It also rated this as a MODERATE 
complexity fix."
```

## Scene 6: Notification & Resolution (60 seconds)

```
[SCREEN: Showing email being sent]

[AGENT 4: Notification Agent] ▶ Formatting notification...
[OUTPUT] Notification prepared with:
  - Pipeline ID: exec_20260415_143022
  - Failed Stage: Test
  - Error Summary: Test assertion failed
  - Recommendations: 5 steps

[SENDING] Email notification sent to ops-team@company.com

✓ Notification delivered successfully

NARRATOR: "The Notification Agent formatted a professional email
with the complete failure context and all 5 recommended fix steps,
then sent it to the team. The team can now act immediately."
```

## Scene 7: Observability & Logs (30 seconds)

```
[SCREEN: Log files]

$ python main_mas.py show-logs

Recent execution events:
2026-04-15 14:30:22 - agent_start: Pipeline Monitor
2026-04-15 14:30:24 - tool_call: execute_pipeline_stage
2026-04-15 14:30:26 - tool_result: Build succeeded
2026-04-15 14:30:28 - tool_call: execute_pipeline_stage  
2026-04-15 14:30:32 - tool_result: Test FAILED
2026-04-15 14:30:32 - agent_end: Pipeline Monitor
2026-04-15 14:30:33 - agent_start: Error Analyzer
2026-04-15 14:30:35 - tool_call: parse_error_log
2026-04-15 14:30:36 - tool_result: 1 error lines found
...

NARRATOR: "The system logs every agent action, tool call,
and decision. This complete execution trace is available for
debugging, compliance, and improvement analysis."
```

## Scene 8: Key Features Highlight (30 seconds)

```
[SCREEN: Feature summary]

✅ Multi-Agent Orchestration
   4 distinct agents working together

✅ Custom Tools
   Pipeline execution, error analysis, solution generation
   All with type hints and docstrings

✅ State Management
   Global context shared between agents with zero data loss

✅ Observability
   Complete JSONL logging of all agent decisions

✅ Comprehensive Testing
   34 test cases validating agent accuracy and reliability

✅ Local Execution
   Ollama only - no cloud APIs, no costs

NARRATOR: "The system demonstrates all core requirements for
a production-grade Multi-Agent System."
```

## Scene 9: Conclusion (15 seconds)

```
[SCREEN: Architecture diagram]

NARRATOR: "This Multi-Agent System automates DevOps pipeline
monitoring completely. From execution to solution delivery,
all without human intervention.

Technology: CrewAI, Ollama, Python
Framework: Open source, zero-cost
Status: Fully functional and ready for production"

[FADE OUT]
```

---

## Recording Tips

1. **Audio**: Use clear microphone, professional tone
2. **Screen**: 1920x1080 resolution, large fonts
3. **Pacing**: Don't rush, give 2-3 seconds for output to appear
4. **Terminal**: Use light background for visibility
5. **Editing**: Show key parts (skip long output)
6. **Subtitles**: Add timestamps for key events

## Total Duration

- Scene 1: 0:30
- Scene 2: 0:30
- Scene 3: 0:45
- Scene 4: 1:00
- Scene 5: 1:00
- Scene 6: 1:00
- Scene 7: 0:30
- Scene 8: 0:30
- Scene 9: 0:15

**TOTAL: 5:40** (Under 5-minute max with tight editing)

## Recording Checklist

- [ ] Ollama running
- [ ] Python environment activated
- [ ] Email configured (for test)
- [ ] Terminal open with clear view
- [ ] Screen recording software ready
- [ ] Audio input working
- [ ] Files ready for demo
- [ ] Timing checked
- [ ] No proprietary data visible
- [ ] Video exported and uploaded

---

Good luck with your demo!
