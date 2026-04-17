"""
Custom tools for multi-agent system.
Each agent has access to specialized tools.
"""
from typing import Dict, List, Tuple, Any
from pathlib import Path
import subprocess
import logging
from datetime import datetime

from src.observability import get_observability_logger
from src.email_service import EmailService

logger = logging.getLogger(__name__)
obs_logger = get_observability_logger()


class PipelineExecutionTools:
    """Tools used by Pipeline Monitor Agent."""
    
    @staticmethod
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
        """
        obs_logger.log_tool_call("PipelineMonitor", "execute_pipeline_stage", {
            "stage": stage_name,
            "num_commands": len(commands),
            "timeout": timeout
        })
        
        output = ""
        try:
            for cmd in commands:
                result = subprocess.run(
                    cmd,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=timeout
                )
                output += result.stdout
                
                if result.returncode != 0:
                    error = result.stderr
                    obs_logger.log_tool_result(
                        "PipelineMonitor", "execute_pipeline_stage",
                        output, error
                    )
                    return False, output, error
            
            obs_logger.log_tool_result(
                "PipelineMonitor", "execute_pipeline_stage",
                output, None
            )
            return True, output, ""
            
        except subprocess.TimeoutExpired as e:
            error = f"Timeout after {timeout}s"
            obs_logger.log_tool_result(
                "PipelineMonitor", "execute_pipeline_stage",
                output, error
            )
            return False, output, error
        except Exception as e:
            error = str(e)
            obs_logger.log_tool_result(
                "PipelineMonitor", "execute_pipeline_stage",
                output, error
            )
            return False, output, error
    
    @staticmethod
    def get_pipeline_status(execution_id: str) -> Dict[str, Any]:
        """
        Get status of a pipeline execution.
        
        Args:
            execution_id: Pipeline execution identifier
        
        Returns:
            Dictionary with pipeline status info
        """
        obs_logger.log_tool_call("PipelineMonitor", "get_pipeline_status", {
            "execution_id": execution_id
        })
        
        status = {
            "execution_id": execution_id,
            "status": "running",
            "timestamp": datetime.now().isoformat()
        }
        
        obs_logger.log_tool_result(
            "PipelineMonitor", "get_pipeline_status",
            str(status)
        )
        return status


class ErrorAnalysisTools:
    """Tools used by Error Analyzer Agent."""
    
    @staticmethod
    def parse_error_log(log_content: str) -> Dict[str, Any]:
        """
        Parse error from log content.
        
        Args:
            log_content: Raw log content
        
        Returns:
            Dictionary with parsed error details
        """
        obs_logger.log_tool_call("ErrorAnalyzer", "parse_error_log", {
            "log_length": len(log_content)
        })
        
        lines = log_content.split("\n")
        error_lines = [l for l in lines if "error" in l.lower() or "fail" in l.lower()]
        
        result = {
            "error_count": len(error_lines),
            "error_lines": error_lines[:10],  # First 10 errors
            "context": log_content[-500:]  # Last 500 chars
        }
        
        obs_logger.log_tool_result(
            "ErrorAnalyzer", "parse_error_log",
            f"Found {len(error_lines)} error lines"
        )
        return result
    
    @staticmethod
    def categorize_error(error_message: str) -> Tuple[str, str]:
        """
        Categorize error and determine severity.
        
        Args:
            error_message: Error message to categorize
        
        Returns:
            Tuple of (category: str, severity: str)
        """
        obs_logger.log_tool_call("ErrorAnalyzer", "categorize_error", {
            "message_length": len(error_message)
        })
        
        error_lower = error_message.lower()
        
        # Categorize
        if any(word in error_lower for word in ["build", "compile", "syntax"]):
            category = "build_error"
        elif any(word in error_lower for word in ["test", "assert", "failed"]):
            category = "test_error"
        elif any(word in error_lower for word in ["lint", "style", "format"]):
            category = "lint_error"
        else:
            category = "unknown_error"
        
        # Determine severity
        if any(word in error_lower for word in ["critical", "fatal", "crash"]):
            severity = "critical"
        elif any(word in error_lower for word in ["error", "fail"]):
            severity = "high"
        else:
            severity = "medium"
        
        result = (category, severity)
        obs_logger.log_tool_result(
            "ErrorAnalyzer", "categorize_error",
            f"{category} - {severity}"
        )
        return result
    
    @staticmethod
    def extract_root_cause(error_context: str, error_category: str) -> str:
        """
        Extract likely root cause from error.
        
        Args:
            error_context: Error context/message
            error_category: Category of error
        
        Returns:
            Root cause analysis
        """
        obs_logger.log_tool_call("ErrorAnalyzer", "extract_root_cause", {
            "category": error_category,
            "context_length": len(error_context)
        })
        
        if error_category == "build_error":
            cause = "Build compilation failed - likely syntax error or missing dependency"
        elif error_category == "test_error":
            cause = "Test case assertion failed - logic or implementation issue"
        elif error_category == "lint_error":
            cause = "Code style violations - formatting or linting standards not met"
        else:
            cause = "Unknown error - requires manual investigation"
        
        obs_logger.log_tool_result(
            "ErrorAnalyzer", "extract_root_cause",
            cause
        )
        return cause


class SolutionGenerationTools:
    """Tools used by Solution Generator Agent."""
    
    @staticmethod
    def generate_fix_steps(error_category: str, 
                          error_context: str) -> List[str]:
        """
        Generate fix steps for error.
        
        Args:
            error_category: Category of error
            error_context: Error context
        
        Returns:
            List of recommended fix steps
        """
        obs_logger.log_tool_call("SolutionGenerator", "generate_fix_steps", {
            "category": error_category
        })
        
        if error_category == "build_error":
            steps = [
                "Review syntax errors in the build logs",
                "Check for missing imports or dependencies",
                "Verify all required build tools are installed",
                "Try clean build (remove cache/artifacts)",
                "Update package dependencies if needed"
            ]
        elif error_category == "test_error":
            steps = [
                "Check test assertions and expected values",
                "Verify test data and mock objects are correct",
                "Debug failing test with print statements",
                "Check for timing or async issues",
                "Run test in isolation to identify conflicts"
            ]
        elif error_category == "lint_error":
            steps = [
                "Review linting rule violations",
                "Format code according to style guide",
                "Use auto-formatter (black, prettier, etc)",
                "Check line length and indentation",
                "Fix naming conventions and imports"
            ]
        else:
            steps = [
                "Review error message carefully",
                "Check system logs for more details",
                "Search project documentation",
                "Consult team or community resources",
                "Create minimal reproducible example"
            ]
        
        obs_logger.log_tool_result(
            "SolutionGenerator", "generate_fix_steps",
            f"Generated {len(steps)} fix steps"
        )
        return steps
    
    @staticmethod
    def generate_prevention_tips(error_category: str) -> List[str]:
        """
        Generate prevention tips for future occurrences.
        
        Args:
            error_category: Category of error
        
        Returns:
            List of prevention recommendations
        """
        obs_logger.log_tool_call("SolutionGenerator", "generate_prevention_tips", {
            "category": error_category
        })
        
        tips = [
            "Set up pre-commit hooks to catch errors early",
            "Use IDE linting and real-time error detection",
            "Implement automated testing in CI/CD pipeline",
            "Use type hints and static analysis tools",
            "Code review before merging to main",
            "Monitor logs and alerting in production"
        ]
        
        obs_logger.log_tool_result(
            "SolutionGenerator", "generate_prevention_tips",
            f"Generated {len(tips)} prevention tips"
        )
        return tips
    
    @staticmethod
    def estimate_fix_complexity(error_category: str, 
                               error_context_length: int) -> str:
        """
        Estimate complexity of fix.
        
        Args:
            error_category: Category of error
            error_context_length: Length of error context
        
        Returns:
            Complexity level: simple, moderate, complex
        """
        obs_logger.log_tool_call("SolutionGenerator", "estimate_fix_complexity", {
            "category": error_category,
            "context_length": error_context_length
        })
        
        if error_context_length < 100:
            complexity = "simple"
        elif error_context_length < 500:
            complexity = "moderate"
        else:
            complexity = "complex"
        
        obs_logger.log_tool_result(
            "SolutionGenerator", "estimate_fix_complexity",
            complexity
        )
        return complexity


class NotificationTools:
    """Tools used by Notification Agent."""
    
    @staticmethod
    def format_notification_message(pipeline_id: str, failed_stage: str,
                                   error_summary: str, 
                                   recommendations: List[str]) -> str:
        """
        Format notification message.
        
        Args:
            pipeline_id: Pipeline execution ID
            failed_stage: Name of failed stage
            error_summary: Summary of error
            recommendations: List of recommendations
        
        Returns:
            Formatted notification message
        """
        obs_logger.log_tool_call("NotificationAgent", "format_notification_message", {
            "pipeline": pipeline_id,
            "stage": failed_stage,
            "num_recs": len(recommendations)
        })
        
        message = f"""
Pipeline Failure Alert
======================
Pipeline ID: {pipeline_id}
Failed Stage: {failed_stage}
Error: {error_summary}

Recommendations:
{chr(10).join(f"- {rec}" for rec in recommendations[:5])}
        """
        
        obs_logger.log_tool_result(
            "NotificationAgent", "format_notification_message",
            f"Formatted message ({len(message)} chars)"
        )
        return message
    
    @staticmethod
    def send_notification(pipeline_id: str, failed_stage: str,
                         error_message: str, ai_analysis: dict) -> bool:
        """
        Send email notification with failure report.
        
        Args:
            pipeline_id: Execution ID
            failed_stage: Failed pipeline stage
            error_message: Error details
            ai_analysis: Dictionary with analysis and recommendations
        
        Returns:
            Success status
        """
        obs_logger.log_tool_call("NotificationAgent", "send_notification", {
            "pipeline_id": pipeline_id,
            "failed_stage": failed_stage,
            "has_analysis": bool(ai_analysis)
        })
        
        try:
            email_service = EmailService()
            success = email_service.send_failure_report(
                pipeline_id=pipeline_id,
                failed_stage=failed_stage,
                error_message=error_message,
                ai_analysis=ai_analysis
            )
            
            if success:
                obs_logger.log_tool_result(
                    "NotificationAgent", "send_notification",
                    f"Email sent successfully to {email_service.recipient}"
                )
                logger.info(f"✅ NOTIFICATION SENT - Email delivered for pipeline {pipeline_id}")
            else:
                obs_logger.log_tool_result(
                    "NotificationAgent", "send_notification",
                    "", "Email service returned false"
                )
                logger.warning(f"⚠️ Email sending failed for pipeline {pipeline_id}")
            
            return success
            
        except Exception as e:
            error_msg = str(e)
            obs_logger.log_tool_result(
                "NotificationAgent", "send_notification",
                "", error_msg
            )
            logger.error(f"❌ NOTIFICATION FAILED - {error_msg}")
            return False
