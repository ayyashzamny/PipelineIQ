"""Pipeline executor."""
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Optional

from pipeline.stages import PipelineStage, StageStatus, DEFAULT_STAGES


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PipelineExecutor:
    """Executes the CI/CD pipeline."""
    
    def __init__(self, stages: Optional[List[PipelineStage]] = None, 
                 fail_at: Optional[str] = None):
        self.stages = stages or DEFAULT_STAGES
        self.fail_at = fail_at  # Force failure at specific stage
        self.execution_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = None
        self.failed_stage = None
        self.error_details = None
        
    def run(self) -> bool:
        """
        Execute the pipeline.
        
        Returns:
            bool: True if all stages succeed, False otherwise
        """
        logger.info("=" * 60)
        logger.info(f"Starting Pipeline Execution: {self.execution_id}")
        logger.info("=" * 60)
        
        self.log_file = self._create_log_file()
        
        for stage in self.stages:
            logger.info(f"\n[STAGE] {stage.name} starting...")
            
            # Simulate forced failure
            if self.fail_at and stage.name.lower() == self.fail_at.lower():
                logger.error(f"[STAGE] {stage.name} FAILED (forced failure)")
                self.failed_stage = stage
                stage.status = StageStatus.FAILED
                stage.error = f"Intentional failure at {stage.name} stage"
                self._log_stage_failure(stage)
                return False
            
            # Run the stage
            success, output, error = stage.run()
            
            # Log output
            self._log_stage_output(stage, output)
            
            if not success:
                logger.error(f"[STAGE] {stage.name} FAILED")
                logger.error(f"Error: {error}")
                self.failed_stage = stage
                self.error_details = {
                    "stage": stage.name,
                    "output": output,
                    "error": error,
                    "duration": stage.get_duration()
                }
                self._log_stage_failure(stage)
                return False
            else:
                logger.info(f"[STAGE] {stage.name} PASSED (Duration: {stage.get_duration():.2f}s)")
        
        logger.info("\n" + "=" * 60)
        logger.info("Pipeline Execution SUCCESSFUL ✓")
        logger.info("=" * 60)
        return True
    
    def _create_log_file(self) -> Path:
        """Create a log file for this execution."""
        from src.config import Config
        
        Config.LOG_DIR.mkdir(exist_ok=True)
        log_file = Config.LOG_DIR / f"pipeline_{self.execution_id}.log"
        return log_file
    
    def _log_stage_output(self, stage: PipelineStage, output: str):
        """Log stage output to file."""
        with open(self.log_file, "a") as f:
            f.write(f"\n{'='*60}\n")
            f.write(f"STAGE: {stage.name}\n")
            f.write(f"STATUS: {stage.status.value if stage.status else 'UNKNOWN'}\n")
            f.write(f"DURATION: {stage.get_duration():.2f}s\n")
            f.write(f"{'='*60}\n")
            f.write(f"OUTPUT:\n{output}\n")
    
    def _log_stage_failure(self, stage: PipelineStage):
        """Log stage failure details."""
        with open(self.log_file, "a") as f:
            f.write(f"\nERROR:\n{stage.error}\n")
    
    def get_error_report(self) -> dict:
        """Get detailed error report."""
        if not self.failed_stage:
            return {}
        
        return {
            "pipeline_id": self.execution_id,
            "failed_stage": self.failed_stage.name,
            "error_message": self.failed_stage.error,
            "output": self.failed_stage.output,
            "log_file": str(self.log_file),
            "timestamp": datetime.now().isoformat()
        }
