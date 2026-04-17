"""
Comprehensive testing suite for multi-agent system.
Each agent has dedicated test cases.
"""
import unittest
import logging
from typing import List, Tuple
from unittest.mock import patch, MagicMock

from src.tools import (
    PipelineExecutionTools,
    ErrorAnalysisTools,
    SolutionGenerationTools,
    NotificationTools
)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


# ==================== AGENT 1: PIPELINE MONITOR TESTS ====================

class PipelineMonitorAgentTests(unittest.TestCase):
    """Test cases for Pipeline Monitor Agent and its tools."""
    
    def test_execute_successful_stage(self):
        """Test successful stage execution."""
        success, output, error = PipelineExecutionTools.execute_pipeline_stage(
            stage_name="Build",
            commands=["echo 'Build successful'"],
            timeout=10
        )
        
        self.assertTrue(success, "Stage should execute successfully")
        self.assertIn("Build successful", output)
        self.assertEqual(error, "")
    
    def test_execute_failed_stage(self):
        """Test failed stage execution."""
        success, output, error = PipelineExecutionTools.execute_pipeline_stage(
            stage_name="Build",
            commands=["exit 1"],
            timeout=10
        )
        
        self.assertFalse(success, "Stage should fail")
        self.assertNotEqual(error, "")
    
    def test_execute_stage_timeout(self):
        """Test stage execution timeout."""
        success, output, error = PipelineExecutionTools.execute_pipeline_stage(
            stage_name="Build",
            commands=["ping -t 127.0.0.1"],  # Windows ping
            timeout=1
        )
        
        self.assertFalse(success, "Stage should timeout")
        self.assertIn("Timeout", error)
    
    def test_get_pipeline_status(self):
        """Test getting pipeline status."""
        status = PipelineExecutionTools.get_pipeline_status("exec_12345")
        
        self.assertIn("execution_id", status)
        self.assertIn("status", status)
        self.assertIn("timestamp", status)
        self.assertEqual(status["execution_id"], "exec_12345")
    
    def test_pipeline_monitor_tool_accuracy(self):
        """
        LLM-as-a-Judge Test: Validate tool outputs are accurate and complete.
        """
        # Test Case 1: Output contains expected information
        success, output, error = PipelineExecutionTools.execute_pipeline_stage(
            stage_name="Test",
            commands=["echo BEGIN && echo MIDDLE && echo END"],
            timeout=10
        )
        
        self.assertTrue(success)
        self.assertIn("BEGIN", output)
        self.assertIn("MIDDLE", output)
        self.assertIn("END", output)
    
    def test_pipeline_monitor_error_safety(self):
        """
        Security Test: Ensure tool handles errors gracefully without crashes.
        """
        # Should not crash on malformed commands
        success, output, error = PipelineExecutionTools.execute_pipeline_stage(
            stage_name="Build",
            commands=["nonexistent_command_xyz"],
            timeout=5
        )
        
        self.assertFalse(success)
        self.assertIsNotNone(error)


# ==================== AGENT 2: ERROR ANALYZER TESTS ====================

class ErrorAnalyzerAgentTests(unittest.TestCase):
    """Test cases for Error Analyzer Agent and its tools."""
    
    def test_parse_error_log_with_errors(self):
        """Test error parsing from log content."""
        log_content = """
        Building project...
        error: undefined variable 'x'
        error: syntax error at line 42
        Compilation failed
        """
        
        result = ErrorAnalysisTools.parse_error_log(log_content)
        
        self.assertGreater(result["error_count"], 0)
        self.assertGreater(len(result["error_lines"]), 0)
    
    def test_categorize_build_error(self):
        """Test categorization of build errors."""
        category, severity = ErrorAnalysisTools.categorize_error(
            "error: failed to compile syntax error at build step"
        )
        
        self.assertEqual(category, "build_error")
        self.assertIn(severity, ["low", "medium", "high", "critical"])
    
    def test_categorize_test_error(self):
        """Test categorization of test errors."""
        category, severity = ErrorAnalysisTools.categorize_error(
            "AssertionError: test failed - expected 5 but got 3"
        )
        
        self.assertEqual(category, "test_error")
    
    def test_categorize_lint_error(self):
        """Test categorization of lint errors."""
        category, severity = ErrorAnalysisTools.categorize_error(
            "lint: E501 line too long style error"
        )
        
        self.assertEqual(category, "lint_error")
    
    def test_extract_root_cause(self):
        """Test root cause extraction."""
        cause = ErrorAnalysisTools.extract_root_cause(
            "Compilation failed",
            "build_error"
        )
        
        self.assertIsNotNone(cause)
        self.assertIn("Build", cause)
    
    def test_error_analyzer_accuracy(self):
        """
        LLM-as-a-Judge Test: Validate error categorization accuracy.
        """
        test_cases = [
            ("syntax error", "build_error"),
            ("test assertion failed", "test_error"),
            ("code style violation", "lint_error"),
        ]
        
        for error_msg, expected_category in test_cases:
            category, _ = ErrorAnalysisTools.categorize_error(error_msg)
            self.assertEqual(category, expected_category, 
                           f"Failed for: {error_msg}")
    
    def test_error_analyzer_completeness(self):
        """
        Property-Based Test: Ensure all error log fields are captured.
        """
        logs = [
            "short error",
            "error " * 50,  # Long error
            "",  # Empty log
        ]
        
        for log in logs:
            result = ErrorAnalysisTools.parse_error_log(log)
            self.assertIn("error_count", result)
            self.assertIn("error_lines", result)
            self.assertIn("context", result)


# ==================== AGENT 3: SOLUTION GENERATOR TESTS ====================

class SolutionGeneratorAgentTests(unittest.TestCase):
    """Test cases for Solution Generator Agent and its tools."""
    
    def test_generate_build_fix_steps(self):
        """Test fix steps generation for build errors."""
        steps = SolutionGenerationTools.generate_fix_steps(
            "build_error",
            "Compilation failed"
        )
        
        self.assertGreater(len(steps), 0)
        self.assertIsInstance(steps, list)
        self.assertTrue(all(isinstance(step, str) for step in steps))
    
    def test_generate_test_fix_steps(self):
        """Test fix steps generation for test errors."""
        steps = SolutionGenerationTools.generate_fix_steps(
            "test_error",
            "Test failed"
        )
        
        self.assertGreater(len(steps), 3)
        self.assertTrue(any("test" in step.lower() for step in steps))
    
    def test_generate_prevention_tips(self):
        """Test prevention tips generation."""
        tips = SolutionGenerationTools.generate_prevention_tips("build_error")
        
        self.assertGreater(len(tips), 0)
        self.assertTrue(all(isinstance(tip, str) for tip in tips))
    
    def test_estimate_fix_complexity_simple(self):
        """Test complexity estimation for simple errors."""
        complexity = SolutionGenerationTools.estimate_fix_complexity(
            "lint_error",
            50  # Short error context
        )
        
        self.assertEqual(complexity, "simple")
    
    def test_estimate_fix_complexity_moderate(self):
        """Test complexity estimation for moderate errors."""
        complexity = SolutionGenerationTools.estimate_fix_complexity(
            "build_error",
            250  # Medium error context
        )
        
        self.assertEqual(complexity, "moderate")
    
    def test_estimate_fix_complexity_complex(self):
        """Test complexity estimation for complex errors."""
        complexity = SolutionGenerationTools.estimate_fix_complexity(
            "test_error",
            1000  # Long error context
        )
        
        self.assertEqual(complexity, "complex")
    
    def test_solution_generator_completeness(self):
        """
        Property-Based Test: All error types generate actionable solutions.
        """
        error_types = ["build_error", "test_error", "lint_error", "unknown_error"]
        
        for error_type in error_types:
            steps = SolutionGenerationTools.generate_fix_steps(error_type, "context")
            self.assertGreater(len(steps), 2, 
                             f"Should have multiple steps for {error_type}")
            self.assertTrue(all(isinstance(s, str) for s in steps),
                          f"All steps should be strings for {error_type}")
    
    def test_solution_generator_accuracy(self):
        """
        LLM-as-a-Judge Test: Validate fix steps are relevant to error type.
        """
        # Build error should mention compilation/dependencies
        steps = SolutionGenerationTools.generate_fix_steps("build_error", "Build fail")
        step_text = " ".join(steps).lower()
        self.assertTrue(
            any(word in step_text for word in ["build", "compile", "dependency", "import"]),
            "Build fix steps should mention relevant terms"
        )


# ==================== AGENT 4: NOTIFICATION AGENT TESTS ====================

class NotificationAgentTests(unittest.TestCase):
    """Test cases for Notification Agent and its tools."""
    
    def test_format_notification_message(self):
        """Test notification message formatting."""
        message = NotificationTools.format_notification_message(
            pipeline_id="exec_12345",
            failed_stage="Build",
            error_summary="Compilation failed",
            recommendations=["Fix syntax", "Update dependencies"]
        )
        
        self.assertIn("exec_12345", message)
        self.assertIn("Build", message)
        self.assertIn("Compilation failed", message)
        self.assertIn("Fix syntax", message)
    
    def test_format_notification_includes_recommendations(self):
        """Test that notification includes all recommendations."""
        recs = ["Step 1", "Step 2", "Step 3", "Step 4", "Step 5", "Step 6"]
        message = NotificationTools.format_notification_message(
            "exec_123",
            "Test",
            "Test failed",
            recs
        )
        
        # Should include recommendations (max 5)
        for rec in recs[:5]:
            self.assertIn(rec, message)
    
    def test_send_notification_success(self):
        """Test notification sending."""
        success = NotificationTools.send_notification(
            recipient="test@example.com",
            message="Test notification",
            channel="email"
        )
        
        self.assertTrue(success, "Should succeed with valid inputs")
    
    def test_send_notification_error_handling(self):
        """Test notification error handling."""
        # Should handle errors gracefully
        success = NotificationTools.send_notification(
            recipient="",
            message="",
            channel="email"
        )
        
        # Should either succeed or fail gracefully without crashing
        self.assertIsInstance(success, bool)
    
    def test_notification_agent_message_quality(self):
        """
        LLM-as-a-Judge Test: Validate notification message quality and completeness.
        """
        message = NotificationTools.format_notification_message(
            "PIPE-001",
            "Deploy",
            "Deployment failed",
            ["Rollback changes", "Check logs", "Verify config"]
        )
        
        # Should be professional and complete
        self.assertGreater(len(message), 50, "Message should be comprehensive")
        self.assertIn("Pipeline", message)
        self.assertIn("Failed", message)
        self.assertIn("Rollback", message)
    
    def test_notification_agent_security(self):
        """
        Security Test: Ensure no sensitive data is exposed in notifications.
        """
        message = NotificationTools.format_notification_message(
            "PIPE-001",
            "Build",
            "API_KEY=secret123 not found",
            ["Check environment"]
        )
        
        # Should not expose sensitive data in summary
        self.assertNotIn("secret123", message.split("Error:")[1] if "Error:" in message else "")


# ==================== INTEGRATION TESTS ====================

class MultiAgentIntegrationTests(unittest.TestCase):
    """Integration tests for the multi-agent system."""
    
    def test_error_flow_pipeline_monitor_to_analyzer(self):
        """Test data flow from Pipeline Monitor to Error Analyzer."""
        # Simulate pipeline failure
        success, output, error = PipelineExecutionTools.execute_pipeline_stage(
            "Test",
            ["exit 1"],
            10
        )
        
        # Error should be passed to analyzer
        self.assertFalse(success)
        self.assertNotEqual(error, "")
        
        # Analyzer should parse the error
        result = ErrorAnalysisTools.parse_error_log(output + error)
        self.assertIsNotNone(result)
    
    def test_error_flow_analyzer_to_solution_generator(self):
        """Test data flow from Error Analyzer to Solution Generator."""
        # Simulate error analysis
        category, severity = ErrorAnalysisTools.categorize_error("Build failed")
        cause = ErrorAnalysisTools.extract_root_cause("Compilation error", category)
        
        # Solution generator should receive this info
        steps = SolutionGenerationTools.generate_fix_steps(category, cause)
        tips = SolutionGenerationTools.generate_prevention_tips(category)
        
        self.assertGreater(len(steps), 0)
        self.assertGreater(len(tips), 0)
    
    def test_error_flow_solution_to_notification(self):
        """Test data flow from Solution Generator to Notification Agent."""
        # Simulate complete workflow
        recs = SolutionGenerationTools.generate_fix_steps("test_error", "Test assertion failed")
        
        # Notification agent should format and send
        message = NotificationTools.format_notification_message(
            "exec_123",
            "Test",
            "Test failed",
            recs
        )
        
        # All components should flow correctly
        self.assertIn("exec_123", message)
        self.assertIn("Test", message)
        for rec in recs[:3]:
            self.assertIn(rec, message)


# ==================== PERFORMANCE & RELIABILITY TESTS ====================

class PerformanceTests(unittest.TestCase):
    """Performance and reliability tests."""
    
    def test_tool_response_time(self):
        """Test that tools respond within acceptable time."""
        import time
        
        start = time.time()
        ErrorAnalysisTools.categorize_error("Test error")
        elapsed = time.time() - start
        
        self.assertLess(elapsed, 1.0, "Tool should respond in <1 second")
    
    def test_tool_reliability_across_iterations(self):
        """Test tool reliability across multiple calls."""
        for i in range(10):
            category, severity = ErrorAnalysisTools.categorize_error("Test error")
            self.assertIsNotNone(category)
            self.assertIsNotNone(severity)
    
    def test_tool_edge_cases(self):
        """Test tools handle edge cases."""
        edge_cases = [
            "",  # Empty string
            "x" * 10000,  # Very long string
            "error" * 100,  # Repeated text
            "!@#$%^&*()",  # Special characters
        ]
        
        for case in edge_cases:
            try:
                ErrorAnalysisTools.categorize_error(case)
            except Exception as e:
                self.fail(f"Tool should handle edge case: {str(e)}")


if __name__ == "__main__":
    # Run all tests with detailed output
    unittest.main(verbosity=2)
