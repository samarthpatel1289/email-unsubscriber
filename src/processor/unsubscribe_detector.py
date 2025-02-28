import requests
import re
from typing import Dict, Optional, List
from urllib.parse import urlparse
from ..mail_integration.mail_handler import Email

class UnsubscribeDetector:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "EmailUnsubscriber/1.0"
        })
        
    def process_email(self, email: Email, unsubscribe_info: Dict) -> bool:
        """Process unsubscribe options for an email"""
        if unsubscribe_info["list_unsubscribe"]:
            return self._process_list_unsubscribe(unsubscribe_info["list_unsubscribe"])
            
        if unsubscribe_info["mailto_links"]:
            return self._process_mailto_links(unsubscribe_info["mailto_links"])
            
        if unsubscribe_info["unsubscribe_links"]:
            return self._process_unsubscribe_links(unsubscribe_info["unsubscribe_links"])
            
        return False
        
    def _process_list_unsubscribe(self, links: List[str]) -> bool:
        """Process List-Unsubscribe header links"""
        success = False
        for link in links:
            if link.startswith("mailto:"):
                success = self._process_mailto_link(link) or success
            else:
                success = self._process_http_link(link) or success
        return success
        
    def _process_mailto_links(self, links: List[str]) -> bool:
        """Process mailto unsubscribe links"""
        return any(self._process_mailto_link(link) for link in links)
        
    def _process_unsubscribe_links(self, links: List[str]) -> bool:
        """Process unsubscribe links in email body"""
        return any(self._process_http_link(link) for link in links)
        
    def _process_mailto_link(self, mailto: str) -> bool:
        """Handle mailto unsubscribe links"""
        # Extract email address from mailto link
        email_match = re.search(r"mailto:([^\?]+)", mailto)
        if not email_match:
            return False
            
        # TODO: Implement actual mailto handling
        print(f"Would send unsubscribe email to: {email_match.group(1)}")
        return True
        
    def _process_http_link(self, url: str) -> bool:
        """Handle HTTP unsubscribe links"""
        try:
            response = self.session.get(url)
            if response.status_code == 200:
                print(f"Successfully processed unsubscribe link: {url}")
                return True
            print(f"Failed to process unsubscribe link: {url} (Status: {response.status_code})")
            return False
        except requests.RequestException as e:
            print(f"Error processing unsubscribe link {url}: {str(e)}")
            return False
