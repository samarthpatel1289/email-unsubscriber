import re
from email import message_from_string
from typing import Optional, List, Dict
from bs4 import BeautifulSoup
from ..mail_integration.mail_handler import Email

class EmailParser:
    UNSUBSCRIBE_PATTERNS = [
        r"unsubscribe",
        r"opt[\s-]?out",
        r"remove[\s-]?me",
        r"stop[\s-]?notifications"
    ]
    
    def __init__(self):
        self.unsubscribe_regex = re.compile(
            "|".join(self.UNSUBSCRIBE_PATTERNS),
            re.IGNORECASE
        )
        
    def parse_email(self, email: Email) -> Dict:
        """Parse email content and headers for unsubscribe information"""
        result = {
            "list_unsubscribe": self._get_list_unsubscribe(email.headers),
            "mailto_links": self._get_mailto_links(email.content),
            "unsubscribe_links": self._get_unsubscribe_links(email.content)
        }
        return result
        
    def _get_list_unsubscribe(self, headers: Dict[str, str]) -> Optional[List[str]]:
        """Extract List-Unsubscribe header if present"""
        if "List-Unsubscribe" in headers:
            return [
                link.strip()
                for link in headers["List-Unsubscribe"].split(",")
                if link.strip()
            ]
        return None
        
    def _get_mailto_links(self, content: str) -> List[str]:
        """Find mailto unsubscribe links in email content"""
        mailto_pattern = r"mailto:[^\s\"']+"
        return re.findall(mailto_pattern, content)
        
    def _get_unsubscribe_links(self, content: str) -> List[str]:
        """Find unsubscribe links in email content"""
        links = []
        soup = BeautifulSoup(content, "html5lib")
        
        for a_tag in soup.find_all("a", href=True):
            if self.unsubscribe_regex.search(a_tag.text) or \
               self.unsubscribe_regex.search(a_tag.get("href", "")):
                links.append(a_tag["href"])
                
        return links
