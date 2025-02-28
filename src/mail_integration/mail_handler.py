import subprocess
import json
from typing import List, Dict
from dataclasses import dataclass

@dataclass
class Email:
    id: str
    subject: str
    sender: str
    date: str
    content: str
    headers: Dict[str, str]
    read_status: bool

class MailHandler:
    def __init__(self):
        self.script_path = "email-unsubscriber/src/mail_integration/mail_script.scpt"
        
    def get_emails(self) -> List[Email]:
        """Fetch emails from Apple Mail using AppleScript"""
        try:
            result = subprocess.run(
                ["osascript", self.script_path],
                capture_output=True,
                text=True,
                check=True
            )
            raw_emails = json.loads(result.stdout)
            return [Email(**email) for email in raw_emails]
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to execute AppleScript: {e.stderr}")
        except json.JSONDecodeError:
            raise RuntimeError("Failed to parse AppleScript output as JSON")

    def mark_as_read(self, email_id: str):
        """Mark an email as read using AppleScript"""
        script = f'''
        tell application "Mail"
            set theMessage to first message of inbox whose id is "{email_id}"
            set read status of theMessage to true
        end tell
        '''
        subprocess.run(["osascript", "-e", script], check=True)
