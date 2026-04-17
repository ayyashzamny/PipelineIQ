"""Security Monitor Agent - Entry point that starts first."""
import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List

from src.yaml_pipeline import YAMLPipelineLoader, YAMLPipelineExecutor
from src.observability import get_observability_logger

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
obs_logger = get_observability_logger()


class SecurityMonitorAgent:
    """
    Main Security Monitor Agent
    
    Responsibilities:
    1. Start first as security/monitoring agent
    2. Load all 3 YAML pipelines
    3. Monitor and orchestrate their execution
    4. Track failures and manage retry loops
    5. Report comprehensive results
    """
    
    def __init__(self, pipelines_dir: str = "pipelines"):
        self.pipelines_dir = pipelines_dir
        self.pipelines = {}
        self.execution_results = []
        self.start_time = datetime.now()
        
        logger.info("🔐 Security Monitor Agent Initialized")
    
    def load_pipelines(self) -> bool:
        """Load all available pipelines."""
        logger.info("\n" + "=" * 70)
        logger.info("📋 PHASE 1: Loading Pipelines")
        logger.info("=" * 70)
        
        try:
            self.pipelines = YAMLPipelineLoader.load_all_pipelines(self.pipelines_dir)
            
            if not self.pipelines:
                logger.error("✗ No pipelines found!")
                return False
            
            logger.info(f"\n✓ Successfully loaded {len(self.pipelines)} pipelines:")
            for pipeline_name, config in self.pipelines.items():
                logger.info(f"  • {pipeline_name}: {config.description}")
            
            return True
            
        except Exception as e:
            logger.error(f"✗ Failed to load pipelines: {e}")
            return False
    
    def execute_pipelines(self) -> Dict[str, bool]:
        """
        Execute all pipelines and monitor them.
        
        Returns:
            Dict mapping pipeline names to success status
        """
        logger.info("\n" + "=" * 70)
        logger.info("▶ PHASE 2: Executing Pipelines")
        logger.info("=" * 70)
        
        results = {}
        
        for pipeline_name, pipeline_config in self.pipelines.items():
            logger.info(f"\n{'→' * 35}")
            
            # Setup executor
            executor = YAMLPipelineExecutor(pipeline_config)
            
            # Execute pipeline (with built-in retry logic)
            success = executor.run()
            results[pipeline_name] = success
            
            # Store detailed results
            self.execution_results.append({
                'pipeline': pipeline_name,
                'success': success,
                'critical': pipeline_config.critical,
                'details': executor.get_summary()
            })
            
            # Log result
            status_icon = "✓" if success else "✗"
            status_text = "PASSED" if success else "FAILED"
            logger.info(f"{status_icon} Pipeline '{pipeline_name}' {status_text}\n")
            
            # If critical pipeline fails, optionally stop (or continue for this demo)
            if not success and pipeline_config.critical:
                logger.warning(f"⚠ Critical pipeline '{pipeline_name}' failed!")
                # For demo purposes, we continue anyway and let all pipelines run
            
            # Log to observability
            self._log_execution(pipeline_name, success)
        
        return results
    
    def generate_report(self, results: Dict[str, bool]) -> None:
        """Generate comprehensive execution report."""
        logger.info("\n" + "=" * 70)
        logger.info("📊 PHASE 3: Execution Report")
        logger.info("=" * 70)
        
        total = len(results)
        passed = sum(1 for success in results.values() if success)
        failed = total - passed
        
        logger.info(f"\n📈 Summary Statistics:")
        logger.info(f"  Total Pipelines:    {total}")
        logger.info(f"  ✓ Passed:           {passed}")
        logger.info(f"  ✗ Failed:           {failed}")
        logger.info(f"  Success Rate:       {(passed/total*100):.1f}%")
        
        logger.info(f"\n📋 Detailed Results:")
        for result in self.execution_results:
            status_icon = "✓" if result['success'] else "✗"
            critical_badge = " [CRITICAL]" if result['critical'] else ""
            logger.info(f"\n  {status_icon} {result['pipeline']}{critical_badge}")
            
            details = result['details']
            stages_passed = sum(1 for s in details['stages'] if s['status'] == 'passed')
            total_stages = len(details['stages'])
            
            logger.info(f"     Stages: {stages_passed}/{total_stages}")
            logger.info(f"     Status: {details['status'].upper()}")
            if details['total_retries'] > 0:
                logger.info(f"     Retries: {details['total_retries']}")
            
            for stage in details['stages']:
                stage_icon = "✓" if stage['status'] == 'passed' else "✗"
                logger.info(f"       {stage_icon} {stage['name']}")
        
        # Overall status
        logger.info("\n" + "=" * 70)
        if failed == 0:
            logger.info("🎉 All pipelines completed successfully!")
        else:
            logger.info(f"⚠ {failed} pipeline(s) failed during execution")
        logger.info("=" * 70)
        
        end_time = datetime.now()
        duration = (end_time - self.start_time).total_seconds()
        logger.info(f"\n⏱ Execution completed in {duration:.2f} seconds")
    
    def _log_execution(self, pipeline_name: str, success: bool) -> None:
        """Log pipeline execution to observability."""
        try:
            obs_logger.log_event({
                'event': 'pipeline_execution',
                'pipeline': pipeline_name,
                'status': 'success' if success else 'failed',
                'timestamp': datetime.now().isoformat()
            })
        except Exception as e:
            logger.debug(f"Could not log to observability: {e}")
    
    def run(self) -> int:
        """
        Main execution flow.
        
        Returns:
            Exit code (0 for success, 1 for failure)
        """
        try:
            # Phase 1: Load pipelines
            if not self.load_pipelines():
                return 1
            
            # Phase 2: Execute pipelines
            results = self.execute_pipelines()
            
            # Phase 3: Generate report
            self.generate_report(results)
            
            # Return exit code based on results
            return 0 if all(results.values()) else 1
            
        except Exception as e:
            logger.error(f"✗ Security Monitor Agent failed: {e}")
            import traceback
            traceback.print_exc()
            return 1


def main():
    """Entry point."""
    agent = SecurityMonitorAgent(pipelines_dir="pipelines")
    exit_code = agent.run()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
