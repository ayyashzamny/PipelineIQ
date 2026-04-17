"""Email notification service."""
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

from src.config import Config

logger = logging.getLogger(__name__)


class EmailService:
    """Sends email notifications with error details and recommendations."""
    
    def __init__(self):
        self.sender = Config.EMAIL_SENDER
        self.password = Config.EMAIL_PASSWORD
        self.recipient = Config.EMAIL_RECIPIENT
        self.smtp_server = Config.SMTP_SERVER
        self.smtp_port = Config.SMTP_PORT
    
    def send_failure_report(self, pipeline_id: str, failed_stage: str, 
                           error_message: str, ai_analysis: dict) -> bool:
        """
        Send failure report email.
        
        Args:
            pipeline_id: Execution ID
            failed_stage: Name of failed stage
            error_message: Error details
            ai_analysis: Dictionary with 'analysis' and 'recommendations'
        
        Returns:
            bool: True if sent successfully
        """
        if not self._validate_config():
            logger.error("Email not configured. Update .env file.")
            return False
        
        try:
            subject = f"🚨 Pipeline Failed: {failed_stage} [{pipeline_id}]"
            body = self._build_email_body(
                pipeline_id, failed_stage, error_message, ai_analysis
            )
            
            # Create email
            msg = MIMEMultipart()
            msg["From"] = self.sender
            msg["To"] = self.recipient
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "html"))
            
            # Send email
            logger.info(f"Sending email to {self.recipient}...")
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender, self.password)
                server.send_message(msg)
            
            logger.info(f"✅ EMAIL SENT SUCCESSFULLY to {self.recipient}")
            return True
            
        except smtplib.SMTPAuthenticationError as e:
            logger.error(f"❌ EMAIL FAILED - Authentication error: {e}")
            logger.error("Check EMAIL_SENDER and EMAIL_PASSWORD in .env")
            return False
        except smtplib.SMTPException as e:
            logger.error(f"❌ EMAIL FAILED - SMTP error: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ EMAIL FAILED - Error: {e}")
            return False
    
    def _validate_config(self) -> bool:
        """Check if email config is set."""
        return bool(self.sender and self.password and self.recipient)
    
    def test_email_connection(self) -> bool:
        """Test if email configuration works."""
        logger.info("Testing email connection...")
        logger.info(f"Sender: {self.sender}")
        logger.info(f"Recipient: {self.recipient}")
        logger.info(f"SMTP Server: {self.smtp_server}:{self.smtp_port}")
        
        if not self._validate_config():
            logger.error("❌ Email configuration incomplete!")
            return False
        
        try:
            # Test SMTP connection
            logger.info("Connecting to SMTP server...")
            with smtplib.SMTP(self.smtp_server, self.smtp_port, timeout=10) as server:
                logger.info("✅ Connected to SMTP server")
                
                server.starttls()
                logger.info("✅ TLS enabled")
                
                server.login(self.sender, self.password)
                logger.info("✅ Authentication successful!")
                
            return True
            
        except smtplib.SMTPAuthenticationError as e:
            logger.error(f"❌ Authentication failed: {e}")
            logger.error("Check EMAIL_SENDER and EMAIL_PASSWORD in .env")
            return False
        except smtplib.SMTPException as e:
            logger.error(f"❌ SMTP error: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ Connection error: {e}")
            return False
    
    def _build_email_body(self, pipeline_id: str, failed_stage: str,
                         error_message: str, ai_analysis: dict) -> str:
        """Build HTML email body."""
        recommendations_html = ""
        if ai_analysis.get("recommendations"):
            recommendations_html = "<ol>"
            for rec in ai_analysis["recommendations"]:
                recommendations_html += f"<li>{rec}</li>"
            recommendations_html += "</ol>"
        
        analysis_text = ai_analysis.get("analysis", "No analysis available")
        model_info = ai_analysis.get("model", "Unknown")
        
        html = f"""
        <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; }}
                    .container {{ max-width: 600px; margin: 0 auto; }}
                    .header {{ background-color: #d32f2f; color: white; padding: 20px; }}
                    .section {{ padding: 15px; border: 1px solid #ddd; margin: 10px 0; }}
                    .stage-name {{ font-weight: bold; color: #d32f2f; }}
                    .recommendations {{ background-color: #e8f5e9; }}
                    .analysis {{ background-color: #f5f5f5; }}
                    .footer {{ font-size: 12px; color: #999; margin-top: 20px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h2>⚠️ Pipeline Failure Alert</h2>
                    </div>
                    
                    <div class="section">
                        <p><strong>Pipeline ID:</strong> {pipeline_id}</p>
                        <p><strong>Failed Stage:</strong> 
                           <span class="stage-name">{failed_stage}</span></p>
                        <p><strong>Time:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                    </div>
                    
                    <div class="section">
                        <h3>Error Details</h3>
                        <pre>{error_message}</pre>
                    </div>
                    
                    <div class="section analysis">
                        <h3>AI Analysis (via {model_info})</h3>
                        <p>{analysis_text}</p>
                    </div>
                    
                    <div class="section recommendations">
                        <h3>✅ Recommended Fixes</h3>
                        {recommendations_html}
                    </div>
                    
                    <div class="footer">
                        <p>This email was sent by DevOps Helper Agent</p>
                        <p>Check logs at: logs/pipeline_{pipeline_id}.log</p>
                    </div>
                </div>
            </body>
        </html>
        """
        return html
