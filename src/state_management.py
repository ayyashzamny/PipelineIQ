"""
Shared state management for the multi-agent system.
Maintains context and data across all agents.
"""
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional
from datetime import datetime
import json


@dataclass
class PipelineExecutionState:
    """Shared state for pipeline execution."""
    execution_id: str
    pipeline_name: str
    start_time: datetime
    end_time: Optional[datetime] = None
    stages_executed: List[str] = field(default_factory=list)
    failed_stage: Optional[str] = None
    error_log: str = ""
    pipeline_output: str = ""
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        data = asdict(self)
        data['start_time'] = self.start_time.isoformat()
        data['end_time'] = self.end_time.isoformat() if self.end_time else None
        return data


@dataclass
class ErrorAnalysisState:
    """Shared state for error analysis."""
    failed_stage: str
    raw_error: str
    error_context: str
    root_cause: Optional[str] = None
    error_severity: str = "medium"  # low, medium, high, critical
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class SolutionState:
    """Shared state for solution generation."""
    error_analysis: str
    recommendations: List[str] = field(default_factory=list)
    implementation_steps: List[str] = field(default_factory=list)
    confidence_score: float = 0.0
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class NotificationState:
    """Shared state for notifications."""
    pipeline_id: str
    failed_stage: str
    error_message: str
    recommendations: List[str]
    email_sent: bool = False
    notification_timestamp: Optional[datetime] = None
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        data = asdict(self)
        data['notification_timestamp'] = self.notification_timestamp.isoformat() if self.notification_timestamp else None
        return data


class SharedContext:
    """Global context for all agents."""
    
    def __init__(self):
        self.pipeline_state: Optional[PipelineExecutionState] = None
        self.error_state: Optional[ErrorAnalysisState] = None
        self.solution_state: Optional[SolutionState] = None
        self.notification_state: Optional[NotificationState] = None
        self.execution_history: List[dict] = []
    
    def update_pipeline_state(self, state: PipelineExecutionState):
        """Update pipeline execution state."""
        self.pipeline_state = state
        self._log_transition(f"Pipeline state updated: {state.execution_id}")
    
    def update_error_state(self, state: ErrorAnalysisState):
        """Update error analysis state."""
        self.error_state = state
        self._log_transition(f"Error state updated: {state.failed_stage}")
    
    def update_solution_state(self, state: SolutionState):
        """Update solution generation state."""
        self.solution_state = state
        self._log_transition(f"Solution state updated with {len(state.recommendations)} recommendations")
    
    def update_notification_state(self, state: NotificationState):
        """Update notification state."""
        self.notification_state = state
        self._log_transition(f"Notification state updated for {state.pipeline_id}")
    
    def _log_transition(self, message: str):
        """Log state transitions."""
        self.execution_history.append({
            "timestamp": datetime.now().isoformat(),
            "message": message
        })
    
    def get_execution_summary(self) -> dict:
        """Get complete execution summary."""
        return {
            "pipeline": self.pipeline_state.to_dict() if self.pipeline_state else None,
            "error_analysis": self.error_state.to_dict() if self.error_state else None,
            "solution": self.solution_state.to_dict() if self.solution_state else None,
            "notification": self.notification_state.to_dict() if self.notification_state else None,
            "history": self.execution_history
        }


# Global context instance
global_context = SharedContext()
