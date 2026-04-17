"""
Main entry point - Security Monitor starts first, then orchestrates 3 pipelines.

Usage:
    python monitor_main.py
    
This will:
1. Start Security Monitor Agent
2. Load 3 realistic YAML pipelines (Deploy, Test, Security)
3. Execute each pipeline and monitor them
4. Continue on failures (retry logic built-in)
5. Generate comprehensive report
"""

import sys
import logging
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.monitor import SecurityMonitorAgent

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """
    Main entry point.
    
    Flow:
    1. Initialize Security Monitor Agent
    2. Load 3 pipelines from pipelines/ directory
    3. Execute each pipeline with monitoring
    4. Generate detailed report
    """
    logger.info("\n" + "🔐" * 35)
    logger.info("   DEVOPS SECURITY MONITOR - STARTING")
    logger.info("🔐" * 35 + "\n")
    
    # Create and run the security monitor agent
    agent = SecurityMonitorAgent(pipelines_dir="pipelines")
    exit_code = agent.run()
    
    if exit_code == 0:
        logger.info("\n✅ All pipelines executed successfully!")
    else:
        logger.info("\n❌ One or more pipelines failed")
    
    return exit_code


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
