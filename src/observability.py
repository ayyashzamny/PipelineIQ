"""
Observability and logging system for agent execution.
Tracks all agent decisions, tool calls, and outputs.
"""
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, Optional
from enum import Enum


class EventType(Enum):
    """Types of events to log."""
    AGENT_START = "agent_start"
    AGENT_END = "agent_end"
    TOOL_CALL = "tool_call"
    TOOL_RESULT = "tool_result"
    DECISION = "decision"
    ERROR = "error"
    STATE_TRANSITION = "state_transition"


class ObservabilityLogger:
    """Logs all agent operations for debugging and analysis."""
    
    def __init__(self, log_dir: Optional[Path] = None):
        self.log_dir = log_dir or Path("logs/observability")
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Create file handler for JSON logs
        self.log_file = self.log_dir / f"execution_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl"
        
        # Standard logger
        self.logger = logging.getLogger("observability")
        self.logger.setLevel(logging.DEBUG)
        
        # Add file handler
        handler = logging.FileHandler(self.log_dir / f"execution_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    
    def log_event(self, event_type: EventType, agent_name: str, 
                  details: Dict[str, Any]) -> None:
        """Log an event in JSON format."""
        event = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type.value,
            "agent_name": agent_name,
            "details": details
        }
        
        # Write to JSONL file
        with open(self.log_file, "a") as f:
            f.write(json.dumps(event) + "\n")
        
        # Also log to standard logger
        self.logger.info(f"[{event_type.value}] {agent_name}: {json.dumps(details)}")
    
    def log_agent_start(self, agent_name: str, task: str) -> None:
        """Log agent start."""
        self.log_event(EventType.AGENT_START, agent_name, {
            "task": task,
            "status": "started"
        })
    
    def log_agent_end(self, agent_name: str, result: str, success: bool) -> None:
        """Log agent completion."""
        self.log_event(EventType.AGENT_END, agent_name, {
            "result": result,
            "success": success,
            "status": "completed"
        })
    
    def log_tool_call(self, agent_name: str, tool_name: str, 
                      inputs: Dict[str, Any]) -> None:
        """Log tool invocation."""
        self.log_event(EventType.TOOL_CALL, agent_name, {
            "tool_name": tool_name,
            "inputs": inputs,
            "status": "called"
        })
    
    def log_tool_result(self, agent_name: str, tool_name: str, 
                       output: str, error: Optional[str] = None) -> None:
        """Log tool result."""
        self.log_event(EventType.TOOL_RESULT, agent_name, {
            "tool_name": tool_name,
            "output": output,
            "error": error,
            "status": "completed"
        })
    
    def log_decision(self, agent_name: str, decision: str, 
                    reasoning: str) -> None:
        """Log agent decision."""
        self.log_event(EventType.DECISION, agent_name, {
            "decision": decision,
            "reasoning": reasoning
        })
    
    def log_error(self, agent_name: str, error_message: str, 
                 error_type: str) -> None:
        """Log error."""
        self.log_event(EventType.ERROR, agent_name, {
            "error_message": error_message,
            "error_type": error_type
        })
    
    def log_state_transition(self, from_state: str, to_state: str, 
                            context: Dict[str, Any]) -> None:
        """Log state transition."""
        self.log_event(EventType.STATE_TRANSITION, "system", {
            "from_state": from_state,
            "to_state": to_state,
            "context": context
        })
    
    def log_event_start(self, system: str, event_name: str) -> None:
        """Log event start."""
        self.log_event(EventType.AGENT_START, system, {
            "event": event_name,
            "status": "started"
        })
    
    def get_execution_trace(self) -> list:
        """Get all logged events."""
        events = []
        try:
            with open(self.log_file, "r") as f:
                for line in f:
                    if line.strip():
                        events.append(json.loads(line))
        except FileNotFoundError:
            pass
        return events


# Global observability logger
observability_logger = None


def get_observability_logger() -> ObservabilityLogger:
    """Get or create global observability logger."""
    global observability_logger
    if observability_logger is None:
        observability_logger = ObservabilityLogger()
    return observability_logger
