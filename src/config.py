"""Configuration management for DevOps Agent."""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
env_file = Path(__file__).parent.parent / ".env"
load_dotenv(env_file)


class Config:
    """Configuration settings."""
    
    # Ollama
    OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama2")
    
    # Email
    EMAIL_SENDER = os.getenv("EMAIL_SENDER")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    EMAIL_RECIPIENT = os.getenv("EMAIL_RECIPIENT")
    SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    
    # Pipeline
    PIPELINE_NAME = os.getenv("PIPELINE_NAME", "DevOps-Local-Pipeline")
    PIPELINE_RETRY_ATTEMPTS = int(os.getenv("PIPELINE_RETRY_ATTEMPTS", "1"))
    FAILURE_THRESHOLD = int(os.getenv("FAILURE_THRESHOLD", "3"))
    
    # Paths
    LOG_DIR = Path(__file__).parent.parent / "logs"
    PIPELINE_DIR = Path(__file__).parent.parent / "pipeline"
    
    @classmethod
    def validate(cls):
        """Validate required configuration."""
        required = ["EMAIL_SENDER", "EMAIL_PASSWORD", "EMAIL_RECIPIENT"]
        missing = [var for var in required if not getattr(cls, var)]
        return missing
