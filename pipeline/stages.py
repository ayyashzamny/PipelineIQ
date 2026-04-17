"""Pipeline stages definition."""
import subprocess
import time
from enum import Enum
from typing import Tuple


class StageStatus(Enum):
    """Pipeline stage status."""
    SUCCESS = "success"
    FAILED = "failed"
    RUNNING = "running"


class PipelineStage:
    """Represents a pipeline stage."""
    
    def __init__(self, name: str, commands: list, timeout: int = 30):
        self.name = name
        self.commands = commands
        self.timeout = timeout
        self.status = None
        self.output = ""
        self.error = ""
        self.start_time = None
        self.end_time = None
    
    def run(self) -> Tuple[bool, str, str]:
        """
        Run the stage.
        
        Returns:
            (success: bool, output: str, error: str)
        """
        self.start_time = time.time()
        self.status = StageStatus.RUNNING
        
        try:
            for command in self.commands:
                result = subprocess.run(
                    command,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=self.timeout
                )
                
                self.output += result.stdout
                
                if result.returncode != 0:
                    self.error = result.stderr
                    self.status = StageStatus.FAILED
                    self.end_time = time.time()
                    return False, self.output, self.error
            
            self.status = StageStatus.SUCCESS
            self.end_time = time.time()
            return True, self.output, ""
            
        except subprocess.TimeoutExpired:
            self.error = f"Stage '{self.name}' timed out after {self.timeout}s"
            self.status = StageStatus.FAILED
            self.end_time = time.time()
            return False, self.output, self.error
        except Exception as e:
            self.error = str(e)
            self.status = StageStatus.FAILED
            self.end_time = time.time()
            return False, self.output, self.error
    
    def get_duration(self) -> float:
        """Get stage execution duration."""
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return 0.0


# Define default pipeline stages
DEFAULT_STAGES = [
    PipelineStage(
        "Build",
        [
            "echo Building application...",
            "dir",  # List directory on Windows
            "echo Build completed successfully!"
        ]
    ),
    PipelineStage(
        "Lint",
        [
            "echo Running linter...",
            "echo Checking code style...",
            "echo Linting passed!"
        ]
    ),
    PipelineStage(
        "Test",
        [
            "echo Running tests...",
            "echo Test suite passed with 100% coverage!"
        ]
    ),
]
