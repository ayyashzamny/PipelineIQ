"""Error analysis module."""
import json
from pathlib import Path


class ErrorAnalyzer:
    """Analyzes pipeline errors from logs."""
    
    def __init__(self, log_file: Path):
        self.log_file = log_file
        self.content = self._read_log()
    
    def _read_log(self) -> str:
        """Read log file content."""
        try:
            with open(self.log_file, "r") as f:
                return f.read()
        except FileNotFoundError:
            return ""
    
    def extract_error_context(self) -> dict:
        """Extract error context from logs."""
        lines = self.content.split("\n")
        
        # Find failed stage
        failed_stage = None
        error_message = ""
        stage_output = ""
        
        in_error_section = False
        for i, line in enumerate(lines):
            if "STAGE:" in line:
                failed_stage = line.split("STAGE:")[1].strip()
            if "FAILED" in line:
                in_error_section = True
            if in_error_section and "ERROR:" in line:
                # Get next few lines as error
                error_message = "\n".join(lines[i:min(i+5, len(lines))])
                break
        
        return {
            "failed_stage": failed_stage,
            "error_message": error_message,
            "full_context": self.content[-2000:] if len(self.content) > 2000 else self.content
        }
    
    def get_summary(self) -> str:
        """Get one-line error summary."""
        if "ERROR:" in self.content:
            lines = self.content.split("\n")
            for line in lines:
                if "ERROR:" in line:
                    return line.strip()
        return "Unknown error"
