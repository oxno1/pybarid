from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime


@dataclass
class Domain:
    """Email domain"""
    name: str
    is_active: bool = True


@dataclass
class Email:
    """Temporary email address"""
    address: str
    domain: str
    created_at: Optional[datetime] = None
    
    @property
    def username(self) -> str:
        """Email username"""
        return self.address.split('@')[0]
    
    @property
    def full_address(self) -> str:
        """Full email address"""
        return f"{self.address}@{self.domain}"


@dataclass
class Message:
    """Email message"""
    id: str
    from_address: str
    to_address: str
    subject: str
    body: str
    html_body: Optional[str] = None
    received_at: Optional[datetime] = None
    attachments: Optional[List[str]] = None
    
    def __post_init__(self):
        if isinstance(self.received_at, str):
            try:
                self.received_at = datetime.fromisoformat(self.received_at.replace('Z', '+00:00'))
            except ValueError:
                self.received_at = None 