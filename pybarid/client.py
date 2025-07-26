import requests
import time
import asyncio
from typing import List, Optional, Dict, Any
from .models import Email, Message, Domain

try:
    import httpx
    HTTPX_AVAILABLE = True
except ImportError:
    HTTPX_AVAILABLE = False


class BaridClient:
    def __init__(self, base_url: str = "https://api.barid.site", async_mode: bool = False):
        """
        Initialize the Barid client
        
        Args:
            base_url: Base URL for the Barid API
            async_mode: Use async HTTP client (requires httpx)
        """
        self.base_url = base_url.rstrip('/')
        self.async_mode = async_mode
        
        if async_mode and not HTTPX_AVAILABLE:
            raise ImportError("httpx is required for async mode. Install with: pip install httpx")
        
        if not async_mode:
            self.session = requests.Session()
            self.session.headers.update({
                'User-Agent': 'PyBarid/1.0.0',
                'Accept': 'application/json'
            })
        else:
            self.session = None
    
    def _make_request(self, endpoint: str, method: str = "GET", **kwargs) -> Dict[str, Any]:
        """Make a request to the Barid API"""
        if self.async_mode:
            raise RuntimeError("Use async methods when in async mode")
        
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json()
    
    async def _make_async_request(self, endpoint: str, method: str = "GET", **kwargs) -> Dict[str, Any]:
        """Make an async request to the Barid API"""
        if not self.async_mode:
            raise RuntimeError("Use sync methods when not in async mode")
        
        url = f"{self.base_url}{endpoint}"
        async with httpx.AsyncClient() as client:
            response = await client.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
    
    def get_domains(self) -> List[Domain]:
        """Get available email domains"""
        try:
            data = self._make_request("/domains")
            return [Domain(name=domain) for domain in data.get("result", [])]
        except requests.RequestException as e:
            raise Exception(f"Failed to get domains: {e}")
    
    async def get_domains_async(self) -> List[Domain]:
        """Get available email domains (async)"""
        try:
            data = await self._make_async_request("/domains")
            return [Domain(name=domain) for domain in data.get("result", [])]
        except httpx.RequestError as e:
            raise Exception(f"Failed to get domains: {e}")
    
    def generate_email(self, domain: Optional[str] = None) -> Email:
        """Generate a temporary email address"""
        import random
        import string
        
        # Get available domains
        domains = self.get_domains()
        if not domains:
            raise Exception("No domains available")
        
        # Use specified domain or random one
        if domain:
            if not any(d.name == domain for d in domains):
                raise Exception(f"Domain {domain} not supported")
            selected_domain = domain
        else:
            selected_domain = random.choice(domains).name
        
        # Generate random username
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        
        return Email(
            address=username,
            domain=selected_domain,
            created_at=time.time()
        )
    
    async def generate_email_async(self, domain: Optional[str] = None) -> Email:
        """Generate a temporary email address (async)"""
        import random
        import string
        
        # Get available domains
        domains = await self.get_domains_async()
        if not domains:
            raise Exception("No domains available")
        
        # Use specified domain or random one
        if domain:
            if not any(d.name == domain for d in domains):
                raise Exception(f"Domain {domain} not supported")
            selected_domain = domain
        else:
            selected_domain = random.choice(domains).name
        
        # Generate random username
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        
        return Email(
            address=username,
            domain=selected_domain,
            created_at=time.time()
        )
    
    def get_messages(self, email: str, domain: str) -> List[Message]:
        """Get messages for a specific email address"""
        try:
            endpoint = f"/emails/{email}@{domain}"
            data = self._make_request(endpoint)
            
            messages = []
            for msg_data in data.get("result", []):
                message = Message(
                    id=msg_data.get("id", ""),
                    from_address=msg_data.get("from_address", ""),
                    to_address=msg_data.get("to_address", ""),
                    subject=msg_data.get("subject", ""),
                    body=msg_data.get("text_content", ""),
                    html_body=msg_data.get("html_content"),
                    received_at=msg_data.get("received_at"),
                    attachments=[]
                )
                messages.append(message)
            
            return messages
        except requests.RequestException as e:
            raise Exception(f"Failed to get messages: {e}")
    
    async def get_messages_async(self, email: str, domain: str) -> List[Message]:
        """Get messages for a specific email address (async)"""
        try:
            endpoint = f"/emails/{email}@{domain}"
            data = await self._make_async_request(endpoint)
            
            messages = []
            for msg_data in data.get("result", []):
                message = Message(
                    id=msg_data.get("id", ""),
                    from_address=msg_data.get("from_address", ""),
                    to_address=msg_data.get("to_address", ""),
                    subject=msg_data.get("subject", ""),
                    body=msg_data.get("text_content", ""),
                    html_body=msg_data.get("html_content"),
                    received_at=msg_data.get("received_at"),
                    attachments=[]
                )
                messages.append(message)
            
            return messages
        except httpx.RequestError as e:
            raise Exception(f"Failed to get messages: {e}")
    
    def get_message(self, message_id: str) -> Optional[Message]:
        """Get a specific message by ID"""
        try:
            endpoint = f"/inbox/{message_id}"
            data = self._make_request(endpoint)
            
            if not data or not data.get("result"):
                return None
                
            msg_data = data.get("result", {})
            return Message(
                id=msg_data.get("id", ""),
                from_address=msg_data.get("from_address", ""),
                to_address=msg_data.get("to_address", ""),
                subject=msg_data.get("subject", ""),
                body=msg_data.get("text_content", ""),
                html_body=msg_data.get("html_content"),
                received_at=msg_data.get("received_at"),
                attachments=[]
            )
        except requests.RequestException as e:
            raise Exception(f"Failed to get message: {e}")
    
    async def get_message_async(self, message_id: str) -> Optional[Message]:
        """Get a specific message by ID (async)"""
        try:
            endpoint = f"/inbox/{message_id}"
            data = await self._make_async_request(endpoint)
            
            if not data or not data.get("result"):
                return None
                
            msg_data = data.get("result", {})
            return Message(
                id=msg_data.get("id", ""),
                from_address=msg_data.get("from_address", ""),
                to_address=msg_data.get("to_address", ""),
                subject=msg_data.get("subject", ""),
                body=msg_data.get("text_content", ""),
                html_body=msg_data.get("html_content"),
                received_at=msg_data.get("received_at"),
                attachments=[]
            )
        except httpx.RequestError as e:
            raise Exception(f"Failed to get message: {e}")
    
    def delete_message(self, message_id: str) -> bool:
        """Delete a specific message"""
        try:
            endpoint = f"/inbox/{message_id}"
            self._make_request(endpoint, method="DELETE")
            return True
        except requests.RequestException as e:
            raise Exception(f"Failed to delete message: {e}")
    
    async def delete_message_async(self, message_id: str) -> bool:
        """Delete a specific message (async)"""
        try:
            endpoint = f"/inbox/{message_id}"
            await self._make_async_request(endpoint, method="DELETE")
            return True
        except httpx.RequestError as e:
            raise Exception(f"Failed to delete message: {e}")
    
    def wait_for_message(self, email: str, domain: str, timeout: int = 60, check_interval: int = 5) -> Optional[Message]:
        """Wait for a message to arrive"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            messages = self.get_messages(email, domain)
            if messages:
                return messages[0]
            time.sleep(check_interval)
        
        return None
    
    async def wait_for_message_async(self, email: str, domain: str, timeout: int = 60, check_interval: int = 5) -> Optional[Message]:
        """Wait for a message to arrive (async)"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            messages = await self.get_messages_async(email, domain)
            if messages:
                return messages[0]
            await asyncio.sleep(check_interval)
        
        return None
    
    def get_inbox_url(self, email: str, domain: str) -> str:
        """Get the web inbox URL for an email address"""
        return f"https://web.barid.site/inbox/{email}@{domain}"
    
    # Batch operations for async mode
    async def get_messages_batch(self, emails: List[Email]) -> Dict[str, List[Message]]:
        """Get messages for multiple emails concurrently"""
        if not self.async_mode:
            raise RuntimeError("Batch operations require async mode")
        
        tasks = [self.get_messages_async(email.address, email.domain) for email in emails]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        batch_results = {}
        for email, result in zip(emails, results):
            if isinstance(result, Exception):
                batch_results[email.full_address] = []
            else:
                batch_results[email.full_address] = result
        
        return batch_results
    
    async def generate_emails_batch(self, count: int, domain: Optional[str] = None) -> List[Email]:
        """Generate multiple emails concurrently"""
        if not self.async_mode:
            raise RuntimeError("Batch operations require async mode")
        
        # Get domains once
        domains = await self.get_domains_async()
        if not domains:
            raise Exception("No domains available")
        
        # Use specified domain or random ones
        if domain:
            if not any(d.name == domain for d in domains):
                raise Exception(f"Domain {domain} not supported")
            selected_domains = [domain] * count
        else:
            import random
            selected_domains = [random.choice(domains).name for _ in range(count)]
        
        # Generate usernames
        import string
        import random
        usernames = [''.join(random.choices(string.ascii_lowercase + string.digits, k=10)) for _ in range(count)]
        
        # Create email objects
        emails = [
            Email(
                address=username,
                domain=selected_domain,
                created_at=time.time()
            )
            for username, selected_domain in zip(usernames, selected_domains)
        ]
        
        return emails 