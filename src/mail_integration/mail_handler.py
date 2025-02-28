from typing import Dict
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
