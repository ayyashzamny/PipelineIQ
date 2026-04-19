"""AI Agent integration with Ollama."""
import requests
import json
import logging
from typing import Optional

from src.config import Config

logger = logging.getLogger(__name__)


class OllamaAgent:
    """AI Agent powered by Ollama for error analysis."""
    
    def __init__(self):
        self.api_url = Config.OLLAMA_API_URL.rstrip("/")
        self.native_api_url = self._resolve_native_api_url(self.api_url)
        self.model = Config.OLLAMA_MODEL
        self.timeout = 60

    @staticmethod
    def _resolve_native_api_url(api_url: str) -> str:
        """Support either Ollama root URLs or OpenAI-compatible `/v1` URLs."""
        if api_url.endswith("/v1"):
            return api_url[:-3]
        return api_url
    
    def check_connection(self) -> bool:
        """Check if Ollama is running."""
        try:
            response = requests.get(f"{self.native_api_url}/api/tags", timeout=5)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Cannot connect to Ollama: {e}")
            return False
    
    def analyze_error(self, error_message: str, stage_name: str, 
                      output: str) -> dict:
        """
        Analyze error using Ollama and provide recommendations.
        
        Returns:
            dict with 'analysis' and 'recommendations' keys
        """
        if not self.check_connection():
            return {
                "analysis": "Ollama is not running",
                "recommendations": [
                    "Make sure Ollama is installed: https://ollama.ai",
                    "Run 'ollama serve' in a terminal",
                    "Try again after Ollama is running"
                ]
            }
        
        prompt = self._build_prompt(error_message, stage_name, output)
        
        try:
            response = requests.post(
                f"{self.native_api_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "temperature": 0.3,
                },
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                analysis_text = result.get("response", "")
                recommendations = self._parse_recommendations(analysis_text)
                
                return {
                    "analysis": analysis_text[:500],  # First 500 chars
                    "recommendations": recommendations,
                    "model": self.model
                }
            else:
                return {
                    "analysis": f"Error from Ollama: {response.status_code}",
                    "recommendations": ["Check Ollama server status"]
                }
        except requests.Timeout:
            return {
                "analysis": "Ollama request timed out",
                "recommendations": ["Ollama is taking too long, check logs for issues"]
            }
        except Exception as e:
            return {
                "analysis": f"Error communicating with Ollama: {str(e)}",
                "recommendations": ["Restart Ollama and try again"]
            }
    
    def _build_prompt(self, error_message: str, stage_name: str, 
                      output: str) -> str:
        """Build prompt for Ollama."""
        return f"""You are a DevOps expert. Analyze this pipeline failure and provide specific fix recommendations.

        Pipeline Stage: {stage_name}
        Error Message: {error_message}
        Stage Output (last 500 chars): {output[-500:] if output else "N/A"}

        Provide:
        1. Root cause analysis (2-3 sentences)
        2. Specific steps to fix (numbered list)
        3. Prevention tips

        Keep response concise and actionable."""
    
    def _parse_recommendations(self, text: str) -> list:
        """Parse recommendations from AI response."""
        recommendations = []
        lines = text.split("\n")
        
        for line in lines:
            # Look for numbered items or bullet points
            if any(line.strip().startswith(f"{i}.") for i in range(1, 10)):
                rec = line.split(".", 1)[-1].strip()
                if rec:
                    recommendations.append(rec)
            elif line.strip().startswith("-"):
                rec = line.strip()[1:].strip()
                if rec:
                    recommendations.append(rec)
        
        # If no recommendations found, create default ones
        if not recommendations:
            recommendations = [
                "Review the error message carefully",
                "Check stage dependencies and environment",
                "Run stage manually to debug"
            ]
        
        return recommendations[:5]  # Return top 5
