"""
Updated main entry point for CrewAI-based multi-agent system.
"""
import sys
import logging
import click
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.config import Config
from src.agents import MultiAgentPipeline
from src.observability import get_observability_logger
from src.state_management import global_context, PipelineExecutionState
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
obs_logger = get_observability_logger()


@click.group()
def cli():
    """DevOps Helper Agent - Multi-Agent System for Pipeline Monitoring."""
    pass


@cli.command()
@click.option('--fail-at', default=None, 
              help='Force failure at specific stage for testing')
def run(fail_at):
    """Run the multi-agent pipeline monitoring system."""
    logger.info("="*70)
    logger.info("Starting Multi-Agent Pipeline Monitoring System")
    logger.info("="*70)
    
    # Initialize pipeline state
    execution_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    pipeline_state = PipelineExecutionState(
        execution_id=execution_id,
        pipeline_name=Config.PIPELINE_NAME,
        start_time=datetime.now()
    )
    global_context.update_pipeline_state(pipeline_state)
    
    # Create and execute multi-agent system
    pipeline = MultiAgentPipeline()
    result = pipeline.execute()
    
    # Get execution summary
    summary = global_context.get_execution_summary()
    
    logger.info("\n" + "="*70)
    logger.info("Multi-Agent System Execution Complete")
    logger.info("="*70)
    logger.info(f"Execution ID: {execution_id}")
    logger.info(f"Status: {result['status']}")
    
    if result['status'] == 'error':
        logger.error(f"Error: {result['error']}")
        sys.exit(1)
    
    # Print execution trace
    logger.info("\nExecution Trace:")
    for event in summary.get('history', [])[:10]:
        logger.info(f"  {event['timestamp']}: {event['message']}")


@cli.command()
def check_config():
    """Validate system configuration."""
    logger.info("Checking configuration...")
    
    # Check email config
    missing = Config.validate()
    if missing:
        logger.warning(f"Missing email configuration: {missing}")
        logger.info("Setup: Edit .env with your Gmail credentials")
    else:
        logger.info("✓ Email configured correctly")
    
    # Check Ollama connection
    from src.ai_agent import OllamaAgent
    agent = OllamaAgent()
    if agent.check_connection():
        logger.info("✓ Ollama is running")
    else:
        logger.warning("✗ Ollama is not running")
        logger.info("Setup: Run 'ollama serve' in another terminal")


@cli.command()
def run_tests():
    """Run comprehensive test suite."""
    logger.info("Running test suite...")
    
    import unittest
    from tests.test_agents import (
        PipelineMonitorAgentTests,
        ErrorAnalyzerAgentTests,
        SolutionGeneratorAgentTests,
        NotificationAgentTests,
        MultiAgentIntegrationTests,
        PerformanceTests
    )
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(PipelineMonitorAgentTests))
    suite.addTests(loader.loadTestsFromTestCase(ErrorAnalyzerAgentTests))
    suite.addTests(loader.loadTestsFromTestCase(SolutionGeneratorAgentTests))
    suite.addTests(loader.loadTestsFromTestCase(NotificationAgentTests))
    suite.addTests(loader.loadTestsFromTestCase(MultiAgentIntegrationTests))
    suite.addTests(loader.loadTestsFromTestCase(PerformanceTests))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)


@cli.command()
def show_logs():
    """Display execution logs and traces."""
    logger.info("Recent execution logs:")
    
    obs_logger = get_observability_logger()
    trace = obs_logger.get_execution_trace()
    
    for event in trace[-20:]:  # Show last 20 events
        logger.info(f"{event['timestamp']} - {event['event_type']}: {event['agent_name']}")


if __name__ == "__main__":
    cli()
