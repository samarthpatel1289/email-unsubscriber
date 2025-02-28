import sys
import time
import logging
import os
from src.mail_integration.mail_handler import MailHandler
from src.processor.email_parser import EmailParser
from src.processor.unsubscribe_detector import UnsubscribeDetector

def setup_logging():
    os.makedirs("logs", exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("logs/app.log"),
            logging.StreamHandler()
        ]
    )

def main():
    setup_logging()
    logging.info("Starting email unsubscriber...")
    
    mail_handler = MailHandler()
    email_parser = EmailParser()
    unsubscribe_detector = UnsubscribeDetector()
    
    try:
        while True:
            print("\nChecking for new emails...")
            emails = mail_handler.get_emails()
            
            for email in emails:
                print(f"\nProcessing email: {email.subject}")
                unsubscribe_info = email_parser.parse_email(email)
                
                if unsubscribe_detector.process_email(email, unsubscribe_info):
                    print("Successfully processed unsubscribe request")
                    mail_handler.mark_as_read(email.id)
                else:
                    print("No unsubscribe options found")
                    
            print("\nSleeping for 5 minutes...")
            time.sleep(300)
            
    except KeyboardInterrupt:
        print("\nShutting down...")
        sys.exit(0)

if __name__ == "__main__":
    main()
