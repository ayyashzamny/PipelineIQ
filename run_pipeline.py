import sys
import json
import logging
from pathlib import Path
from src.pipeline import PipelineExecutor
from src.config import Config
from src.state_management import global_context, PipelineExecutionState
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("ManualPipeline")

def run_manual_pipeline(fail_at=None):
    logger.info("="*70)
    logger.info("MANUAL PIPELINE EXECUTION")
    logger.info("="*70)
    
    # Initialize pipeline state
    execution_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    pipeline_state = PipelineExecutionState(
        execution_id=execution_id,
        pipeline_name=Config.PIPELINE_NAME,
        start_time=datetime.now()
    )
    global_context.update_pipeline_state(pipeline_state)
    
    # Create and run executor
    executor = PipelineExecutor(fail_at=fail_at)
    success = executor.run()
    
    if not success:
        report = executor.get_error_report()
        report_path = Config.LOG_DIR / "last_pipeline_failure.json"
        
        with open(report_path, "w") as f:
            json.dump(report, f, indent=4)
        
        logger.error("\n" + "!"*70)
        logger.error(f"PIPELINE FAILED at stage: {report['failed_stage']}")
        logger.error(f"Failure report saved to: {report_path}")
        logger.error("You can now run 'python run_agent.py' to analyze this failure.")
        logger.error("!"*70 + "\n")
        return False
    else:
        logger.info("\n" + "="*70)
        logger.info("PIPELINE COMPLETED SUCCESSFULLY ✓")
        logger.info("="*70 + "\n")
        return True

if __name__ == "__main__":
    # Allow forcing failure via command line argument
    fail_stage = sys.argv[1] if len(sys.argv) > 1 else "Test"
    run_manual_pipeline(fail_at=fail_stage)
