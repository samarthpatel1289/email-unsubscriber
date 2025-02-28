# Email Unsubscriber

A Python application that automatically detects and processes unsubscribe options in emails from Apple Mail.

## Features

- Reads emails from Apple Mail using AppleScript
- Detects unsubscribe options in email headers and body
- Processes both HTTP and mailto unsubscribe links
- Runs continuously, checking for new emails every 5 minutes
- Marks processed emails as read

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Grant the application access to your Mail app through System Preferences > Security & Privacy > Privacy > Automation

## Usage

Run the application:
```bash
python main.py
```

The application will run continuously, checking for new emails every 5 minutes. Press Ctrl+C to stop.

## Configuration

Edit `config/settings.json` to configure:
- Email account to monitor
- Processing frequency
- Logging preferences

## Requirements

- Python 3.8+
- macOS with Apple Mail
- Internet connection for processing HTTP unsubscribe links
