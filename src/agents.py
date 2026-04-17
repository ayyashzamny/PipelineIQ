"""
Multi-agent system using CrewAI framework.
Defines 4 distinct agents for DevOps pipeline monitoring.
"""
from crewai import Agent, Task, Crew, LLM
from typing import Optional, Dict, Any
import logging

from src.tools import (
    PipelineExecutionTools,
    ErrorAnalysisTools, 
    SolutionGenerationTools,
    NotificationTools
)
from src.config import Config
from src.observability import get_observability_logger
from src.state_management import global_context

logger = logging.getLogger(__name__)
obs_logger = get_observability_logger()


class PipelineMonitorAgent:
    """
    Agent 1: Pipeline Monitor
    Responsible for executing and monitoring pipeline stages.
    """
    
    @staticmethod
    def create_agent() -> Agent:
        """Create Pipeline Monitor agent."""
        
        system_prompt = """You are a DevOps Pipeline Monitor Agent.
        
Your role is to:
1. Execute pipeline stages (Build, Test, Lint)
2. Monitor stage execution and capture outputs
3. Detect any failures or issues
4. Pass execution details to the next agent

Constraints:
- Always execute stages in correct order: Build → Lint → Test
- Capture complete output and error logs
- Stop immediately on failure
- Report all execution details clearly

Your tools allow you to execute stages and get pipeline status."""
        
        return Agent(
            name="Pipeline Monitor",
            role="DevOps Pipeline Monitor",
            goal="Execute pipeline stages and detect failures early",
            backstory="Expert DevOps engineer monitoring CI/CD pipelines for issues",
            verbose=True,
            allow_delegation=False,
            system_prompt=system_prompt,
            llm=_get_ollama_llm()
        )


class ErrorAnalyzerAgent:
    """
    Agent 2: Error Analyzer
    Analyzes failures and determines root causes.
    """
    
    @staticmethod
    def create_agent() -> Agent:
        """Create Error Analyzer agent."""
        
        system_prompt = """You are an Error Analysis Specialist Agent.

Your role is to:
1. Receive pipeline execution logs from Pipeline Monitor
2. Parse and analyze error messages
3. Categorize errors (build, test, lint)
4. Determine root causes
5. Assess error severity

Constraints:
- Analyze ONLY the provided error context
- Be concise and specific in root cause analysis
- Categorize into: build_error, test_error, lint_error, unknown_error
- Assign severity: low, medium, high, critical
- Avoid speculation

Your tools help parse logs and categorize errors."""
        
        return Agent(
            name="Error Analyzer",
            role="Error Analysis Specialist",
            goal="Identify root causes of pipeline failures",
            backstory="Seasoned debugging expert with deep knowledge of CI/CD systems",
            verbose=True,
            allow_delegation=False,
            system_prompt=system_prompt,
            llm=_get_ollama_llm()
        )


class SolutionGeneratorAgent:
    """
    Agent 3: Solution Generator
    Generates actionable solutions and recommendations.
    """
    
    @staticmethod
    def create_agent() -> Agent:
        """Create Solution Generator agent."""
        
        system_prompt = """You are a Solution Generation Expert Agent.

Your role is to:
1. Receive error analysis from Error Analyzer
2. Generate specific fix steps
3. Provide prevention recommendations
4. Estimate fix complexity
5. Create actionable remediation plan

Constraints:
- Generate 3-5 specific, actionable fix steps
- Include prevention measures
- Keep solutions practical and implementable
- Estimate complexity: simple, moderate, complex
- Focus on immediate fixes first

Your tools generate comprehensive remediation plans."""
        
        return Agent(
            name="Solution Generator",
            role="Solution Generation Expert",
            goal="Create actionable remediation plans for pipeline failures",
            backstory="Expert DevOps architect with 10+ years of troubleshooting experience",
            verbose=True,
            allow_delegation=False,
            system_prompt=system_prompt,
            llm=_get_ollama_llm()
        )


class NotificationAgent:
    """
    Agent 4: Notification Agent
    Handles sending notifications with solutions.
    """
    
    @staticmethod
    def create_agent() -> Agent:
        """Create Notification agent."""
        
        system_prompt = """You are a Notification Coordination Agent.

Your role is to:
1. Receive complete failure context from previous agents
2. Format professional notification message
3. Send alert to team members
4. Include error details and recommendations
5. Ensure communication is clear and actionable

Constraints:
- Include pipeline ID, failed stage, error summary
- Provide top remediation steps
- Keep messages concise but comprehensive
- Use professional tone
- Ensure recipient can act immediately

Your tools format and send notifications."""
        
        return Agent(
            name="Notification Agent",
            role="Notification Coordinator",
            goal="Ensure team is promptly notified with actionable solutions",
            backstory="Communication expert skilled in incident response and escalation",
            verbose=True,
            allow_delegation=False,
            system_prompt=system_prompt,
            llm=_get_ollama_llm()
        )


class PipelineTaskChain:
    """Defines the task chain for the multi-agent system."""
    
    @staticmethod
    def create_pipeline_monitoring_tasks() -> list:
        """Create tasks for full pipeline monitoring workflow."""
        
        tasks = []
        
        # Task 1: Execute Pipeline
        task1 = Task(
            description="Execute the DevOps pipeline. Run Build stage, then Lint stage, then Test stage. "
                       "Capture all outputs and error messages. Report complete execution status.",
            expected_output="Detailed pipeline execution report with all stage outputs or failure details",
            agent=PipelineMonitorAgent.create_agent()
        )
        tasks.append(task1)
        
        # Task 2: Analyze Errors
        task2 = Task(
            description="Analyze the pipeline execution report. If successful, report success. "
                       "If failed, parse the error logs, categorize the error type, and determine root cause basis on the error context.",
            expected_output="Error analysis including: category, severity, root cause, and error summary",
            agent=ErrorAnalyzerAgent.create_agent()
        )
        tasks.append(task2)
        
        # Task 3: Generate Solutions
        task3 = Task(
            description="Based on the error analysis, generate comprehensive remediation plan. "
                       "Create specific fix steps, prevention recommendations, and complexity assessment.",
            expected_output="Remediation plan with fix steps, prevention tips, and complexity level",
            agent=SolutionGeneratorAgent.create_agent()
        )
        tasks.append(task3)
        
        # Task 4: Notify Team
        task4 = Task(
            description="Format and send notification with complete failure context and solutions. "
                       "Include pipeline ID, failed stage, error summary, and all recommendations.",
            expected_output="Notification sent with complete failure report and remediation steps",
            agent=NotificationAgent.create_agent()
        )
        tasks.append(task4)
        
        return tasks


class MultiAgentPipeline:
    """Main multi-agent system orchestrator."""
    
    def __init__(self):
        """Initialize the multi-agent pipeline."""
        self.crew = None
        self.tasks = PipelineTaskChain.create_pipeline_monitoring_tasks()
        
        obs_logger.log_state_transition(
            "not_initialized",
            "initialized",
            {"num_agents": 4, "num_tasks": len(self.tasks)}
        )
    
    def initialize_crew(self) -> None:
        """Initialize CrewAI crew with all agents."""
        agents = [
            PipelineMonitorAgent.create_agent(),
            ErrorAnalyzerAgent.create_agent(),
            SolutionGeneratorAgent.create_agent(),
            NotificationAgent.create_agent()
        ]
        
        self.crew = Crew(
            agents=agents,
            tasks=self.tasks,
            verbose=True
        )
        
        obs_logger.log_state_transition(
            "initialized",
            "crew_ready",
            {"num_agents": len(agents)}
        )
    
    def execute(self) -> Dict[str, Any]:
        """Execute the multi-agent pipeline."""
        if not self.crew:
            self.initialize_crew()
        
        obs_logger.log_event_start("system", "pipeline_execution")
        
        try:
            result = self.crew.kickoff()
            
            # Check if failure was detected and send email
            result_str = str(result).lower()
            if "failed" in result_str or "error" in result_str or "failure" in result_str:
                logger.info("\n" + "="*70)
                logger.info("FAILURE DETECTED - Sending email notification...")
                logger.info("="*70)
                
                # Extract pipeline info from context
                pipeline_state = global_context.get_pipeline_state()
                execution_id = pipeline_state.execution_id if pipeline_state else "unknown"
                
                # Prepare AI analysis data
                ai_analysis = {
                    "analysis": "Pipeline execution detected failures. Review error details and recommendations below.",
                    "recommendations": [
                        "Check build/lint/test stage logs",
                        "Verify environment configuration",
                        "Review recent code changes",
                        "Run diagnostics on failed stage"
                    ],
                    "model": "Ollama (llama2:latest)"
                }
                
                # Import and use NotificationTools to send email
                from src.tools import NotificationTools
                success = NotificationTools.send_notification(
                    pipeline_id=execution_id,
                    failed_stage="Pipeline Execution",
                    error_message=str(result)[:500],  # First 500 chars of error
                    ai_analysis=ai_analysis
                )
                
                if success:
                    logger.info("✅ EMAIL NOTIFICATION SENT SUCCESSFULLY")
                else:
                    logger.warning("⚠️  Email notification could not be sent - check configuration")
                logger.info("="*70)
            
            obs_logger.log_state_transition(
                "crew_ready",
                "execution_complete",
                {"status": "success"}
            )
            
            return {
                "status": "success",
                "result": result
            }
        except Exception as e:
            logger.error(f"Pipeline execution failed: {e}")
            
            obs_logger.log_state_transition(
                "crew_ready",
                "execution_failed",
                {"error": str(e)}
            )
            
            return {
                "status": "error",
                "error": str(e)
            }


def _get_ollama_llm() -> LLM:
    """Get Ollama LLM configuration for agents."""
    return LLM(
        model=Config.OLLAMA_MODEL,
        base_url=Config.OLLAMA_API_URL,
        api_key="ollama"  # Ollama doesn't require API key
    )
