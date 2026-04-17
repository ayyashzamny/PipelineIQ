"""Main entry point for DevOps Helper Agent."""
import sys
import logging
import click
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.config import Config
from src.pipeline import PipelineExecutor
from src.analyzer import ErrorAnalyzer
from src.ai_agent import OllamaAgent
from src.email_service import EmailService

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@click.group()
def cli():
    """DevOps Helper Agent - Local Pipeline Monitoring System."""
    pass


@cli.command()
@click.option('--fail-at', default=None, 
              help='Force failure at specific stage (Build, Test, Lint)')
def run(fail_at):
    """Run the pipeline once."""
    logger.info("Starting pipeline execution...")
    
    # Execute pipeline
    executor = PipelineExecutor(fail_at=fail_at)
    success = executor.run()
    
    if success:
        logger.info("✓ Pipeline completed successfully!")
        sys.exit(0)
    else:
        logger.error("✗ Pipeline failed!")
        _handle_failure(executor)
        sys.exit(1)


@cli.command()
def check_config():
    """Validate configuration."""
    logger.info("Checking configuration...")
    
    # Check email config
    missing = Config.validate()
    if missing:
        logger.warning(f"Missing email configuration: {missing}")
        logger.info("Setup: Edit .env with your Gmail credentials")
        return
    
    logger.info("✓ Email configured correctly")
    
    # Check Ollama connection
    agent = OllamaAgent()
    if agent.check_connection():
        logger.info("✓ Ollama is running")
    else:
        logger.warning("✗ Ollama is not running")
        logger.info("Setup: Run 'ollama serve' in another terminal")


@cli.command()
def test_email():
    """Test email configuration."""
    logger.info("Testing email configuration...")
    
    service = EmailService()
    
    # Send test email
    success = service.send_failure_report(
        pipeline_id="TEST_123",
        failed_stage="Test Stage",
        error_message="This is a test error message",
        ai_analysis={
            "analysis": "This is a test analysis",
            "recommendations": [
                "This is recommendation 1",
                "This is recommendation 2"
            ]
        }
    )
    
    if success:
        logger.info(f"✓ Test email sent to {service.recipient}")
    else:
        logger.error("✗ Failed to send test email")


def _handle_failure(executor: PipelineExecutor):
    """Handle pipeline failure - analyze and email."""
    logger.info("\n" + "="*60)
    logger.info("HANDLING FAILURE...")
    logger.info("="*60)
    
    # Get error report
    error_report = executor.get_error_report()
    if not error_report:
        logger.error("No error details available")
        return
    
    logger.info(f"Failed Stage: {error_report['failed_stage']}")
    logger.info(f"Error: {error_report['error_message']}")
    
    # Analyze error with AI
    logger.info("\nAnalyzing error with AI...")
    agent = OllamaAgent()
    ai_analysis = agent.analyze_error(
        error_message=error_report['error_message'],
        stage_name=error_report['failed_stage'],
        output=error_report.get('output', '')
    )
    
    logger.info(f"\nAI Analysis:\n{ai_analysis['analysis']}")
    logger.info("\nRecommendations:")
    for i, rec in enumerate(ai_analysis['recommendations'], 1):
        logger.info(f"  {i}. {rec}")
    
    # Send email
    logger.info("\nSending failure report email...")
    service = EmailService()
    email_sent = service.send_failure_report(
        pipeline_id=error_report['pipeline_id'],
        failed_stage=error_report['failed_stage'],
        error_message=error_report['error_message'],
        ai_analysis=ai_analysis
    )
    
    if email_sent:
        logger.info("✓ Email notification sent successfully!")
    else:
        logger.warning("⚠ Email notification failed (check configuration)")
    
    logger.info("="*60)


if __name__ == "__main__":
    cli()
