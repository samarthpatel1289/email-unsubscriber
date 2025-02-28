import subprocess
import json
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

def get_emails(max_emails: int = 50) -> List[Dict]:
    """Fetch emails from Apple Mail using AppleScript
    Args:
        max_emails: Maximum number of emails to fetch (default: 50)
    """
    try:
        script_path = '/Users/samarthpatel/Desktop/email-unsubscriber/src/mail_integration/mail_script.scpt'
        result = subprocess.run(
            ['osascript', script_path, str(max_emails)],
            capture_output=True,
            text=True
        )
        
        # Debugging output
        logger.debug(f"AppleScript stdout: {result.stdout}")
        logger.debug(f"AppleScript stderr: {result.stderr}")
        
        result.check_returncode()
        
        # Clean and validate JSON output
        json_str = result.stdout.strip()
        
        # Basic validation
        if not json_str or not json_str.startswith('{'):
            logger.error(f"Invalid JSON start: {json_str[:100]}")
            raise RuntimeError("AppleScript output is not valid JSON")
            
        # Try to parse JSON with error recovery
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            # Attempt to fix common AppleScript JSON issues
            try:
                # Remove trailing commas
                json_str = json_str.replace(',}', '}')
                json_str = json_str.replace(',]', ']')
                
                # Fix unescaped quotes
                json_str = json_str.replace('\\"', '"')
                json_str = json_str.replace('"', '\\"')
                
                # Try parsing again
                return json.loads(json_str)
            except json.JSONDecodeError as e2:
                logger.error(f"Failed to parse JSON after cleanup: {e2}")
                logger.error(f"Raw output: {json_str[:500]}")
                raise RuntimeError("Failed to parse AppleScript output as JSON after cleanup")
    except subprocess.CalledProcessError as e:
        logger.error(f"AppleScript execution failed: {e.stderr}")
        raise RuntimeError(f"Failed to execute AppleScript: {e.stderr}")
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON from AppleScript: {e}")
        logger.error(f"Raw output: {result.stdout[:500]}")
        raise RuntimeError("Invalid JSON response from AppleScript")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise RuntimeError(f"Unexpected error: {str(e)}")

def mark_email_as_read(email_id: str) -> bool:
    """Mark an email as read using AppleScript"""
    try:
        result = subprocess.run(
            ['osascript', 'src/mail_integration/mark_read.scpt', email_id],
            capture_output=True,
            text=True
        )
        result.check_returncode()
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to mark email as read: {e.stderr}")
        return False
