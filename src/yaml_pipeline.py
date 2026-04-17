"""YAML Pipeline loader and executor."""
import yaml
import logging
from pathlib import Path
from typing import List, Dict, Any
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class PipelineConfig:
    """Parsed pipeline configuration."""
    name: str
    description: str
    stages: List[Dict[str, Any]]
    timeout: int
    retry_on_failure: bool
    max_retries: int
    critical: bool


class YAMLPipelineLoader:
    """Loads and parses YAML pipeline definitions."""
    
    @staticmethod
    def load_pipeline(yml_path: str) -> PipelineConfig:
        """Load pipeline from YAML file."""
        path = Path(yml_path)
        
        if not path.exists():
            raise FileNotFoundError(f"Pipeline file not found: {yml_path}")
        
        with open(path, 'r') as f:
            data = yaml.safe_load(f)
        
        return PipelineConfig(
            name=data.get('name', 'Unknown Pipeline'),
            description=data.get('description', ''),
            stages=data.get('stages', []),
            timeout=data.get('timeout', 60),
            retry_on_failure=data.get('retry_on_failure', True),
            max_retries=data.get('max_retries', 1),
            critical=data.get('critical', False)
        )
    
    @staticmethod
    def load_all_pipelines(pipelines_dir: str) -> Dict[str, PipelineConfig]:
        """Load all YAML pipelines from directory."""
        pipelines_path = Path(pipelines_dir)
        pipelines = {}
        
        if not pipelines_path.exists():
            logger.warning(f"Pipelines directory not found: {pipelines_dir}")
            return pipelines
        
        for yml_file in pipelines_path.glob('*.yml'):
            try:
                pipeline = YAMLPipelineLoader.load_pipeline(str(yml_file))
                pipelines[pipeline.name] = pipeline
                logger.info(f"✓ Loaded pipeline: {pipeline.name}")
            except Exception as e:
                logger.error(f"✗ Failed to load {yml_file.name}: {e}")
        
        return pipelines


class YAMLPipelineExecutor:
    """Executes YAML pipeline stages."""
    
    def __init__(self, pipeline_config: PipelineConfig):
        self.config = pipeline_config
        self.execution_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.results = {
            'pipeline': pipeline_config.name,
            'execution_id': self.execution_id,
            'status': 'pending',
            'stages': [],
            'start_time': None,
            'end_time': None,
            'total_retries': 0
        }
    
    def run(self, retry_count: int = 0) -> bool:
        """
        Execute the pipeline.
        
        Args:
            retry_count: Current retry attempt
            
        Returns:
            bool: True if successful, False otherwise
        """
        import subprocess
        import time
        
        self.results['start_time'] = datetime.now().isoformat()
        
        logger.info("=" * 70)
        logger.info(f"▶ Starting Pipeline: {self.config.name} (Attempt {retry_count + 1})")
        logger.info(f"  Description: {self.config.description}")
        logger.info("=" * 70)
        
        for idx, stage in enumerate(self.config.stages, 1):
            stage_name = stage.get('name', f'Stage {idx}')
            commands = stage.get('commands', [])
            
            logger.info(f"\n[STAGE {idx}/{len(self.config.stages)}] {stage_name}")
            logger.info("-" * 70)
            
            stage_result = {
                'name': stage_name,
                'status': 'pending',
                'output': '',
                'error': '',
                'duration': 0
            }
            
            stage_start = time.time()
            
            try:
                for cmd_idx, command in enumerate(commands, 1):
                    logger.info(f"  > {command}")
                    
                    result = subprocess.run(
                        command,
                        shell=True,
                        capture_output=True,
                        text=True,
                        timeout=self.config.timeout
                    )
                    
                    if result.stdout:
                        stage_result['output'] += result.stdout
                        logger.info(result.stdout.strip())
                    
                    if result.returncode != 0:
                        stage_result['status'] = 'failed'
                        stage_result['error'] = result.stderr
                        logger.error(f"✗ Stage failed: {result.stderr}")
                        self.results['stages'].append(stage_result)
                        self.results['status'] = 'failed'
                        
                        # Retry if configured
                        if self.config.retry_on_failure and retry_count < self.config.max_retries:
                            logger.warning(f"⟳ Retrying pipeline ({retry_count + 1}/{self.config.max_retries})...")
                            self.results['total_retries'] = retry_count + 1
                            return self.run(retry_count + 1)
                        
                        return False
                
                stage_result['status'] = 'passed'
                stage_result['duration'] = time.time() - stage_start
                logger.info(f"✓ Stage passed ({stage_result['duration']:.2f}s)")
                self.results['stages'].append(stage_result)
                
            except subprocess.TimeoutExpired:
                stage_result['status'] = 'timeout'
                stage_result['error'] = f"Stage timed out after {self.config.timeout}s"
                stage_result['duration'] = time.time() - stage_start
                logger.error(f"✗ Stage timed out: {stage_result['error']}")
                self.results['stages'].append(stage_result)
                self.results['status'] = 'failed'
                return False
            except Exception as e:
                stage_result['status'] = 'error'
                stage_result['error'] = str(e)
                stage_result['duration'] = time.time() - stage_start
                logger.error(f"✗ Stage error: {e}")
                self.results['stages'].append(stage_result)
                self.results['status'] = 'failed'
                return False
        
        self.results['end_time'] = datetime.now().isoformat()
        self.results['status'] = 'passed'
        
        logger.info("\n" + "=" * 70)
        logger.info(f"✓ Pipeline PASSED: {self.config.name}")
        logger.info("=" * 70)
        return True
    
    def get_summary(self) -> Dict[str, Any]:
        """Get execution summary."""
        return self.results
