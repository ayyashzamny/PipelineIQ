import sys
import json
import logging
from pathlib import Path
from src.agents import TriggeredAIAgent
from src.config import Config
from src.state_management import global_context, PipelineExecutionState
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("AgentTrigger")

def run_triggered_agent():
    logger.info("="*70)
    logger.info("AGENTIC AI SYSTEM - TRIGGERED ANALYSIS")
    logger.info("="*70)
    
    report_path = Config.LOG_DIR / "last_pipeline_failure.json"
    
    if not report_path.exists():
        logger.error(f"No failure report found at: {report_path}")
        logger.error("Please run the pipeline first using 'python run_pipeline.py'.")
        return
    
    try:
        with open(report_path, "r") as f:
            error_report = json.load(f)
    except Exception as e:
        logger.error(f"Failed to load failure report: {e}")
        return

    # Check Ollama connection
    from src.ai_agent import OllamaAgent
    agent_check = OllamaAgent()
    if not agent_check.check_connection():
        logger.error("✗ Ollama is not running! Please start Ollama before running the agent.")
        return
    
    # Initialize and execute triggered agent
    agent_system = TriggeredAIAgent(error_report)
    result = agent_system.execute()
    
    if result['status'] == 'success':
        logger.info("\n" + "="*70)
        logger.info("AI ANALYSIS AND NOTIFICATION COMPLETE")
        logger.info("="*70 + "\n")
    else:
        logger.error(f"AI System failed: {result.get('error')}")

if __name__ == "__main__":
    run_triggered_agent()
