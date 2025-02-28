# Email Unsubscriber

A Python application that automatically detects and processes unsubscribe options in emails using the Gmail API.

## Features

- Reads emails from Gmail using the official API
- Detects unsubscribe options in email headers and body
- Processes both HTTP and mailto unsubscribe links
- Runs on demand or can be scheduled via cron

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up Gmail API credentials:
   - Go to the [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project and enable the Gmail API
   - Create OAuth 2.0 credentials and download the credentials.json file
   - Place credentials.json in the project root

## Usage

Run the application:
```bash
python fetch_emails.py
```

The application will process your most recent emails and display any unsubscribe links found.

## Configuration

Edit `config/settings.json` to configure:
- Number of emails to process
- Logging preferences

## Requirements

- Python 3.8+
- Gmail account
- Internet connection
