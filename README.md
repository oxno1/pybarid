# PyBarid

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Python library for [Barid](https://api.barid.site/) temporary email service.

## Install

```bash
pip install pybarid
```

## Usage

### Sync Mode (Default)

```python
from pybarid import BaridClient

client = BaridClient()

# Generate email
email = client.generate_email()
print(email.full_address)

# Check messages
messages = client.get_messages(email.address, email.domain)
for msg in messages:
    print(f"{msg.from_address}: {msg.subject}")

# Wait for message
message = client.wait_for_message(email.address, email.domain, timeout=60)
if message:
    print(f"New: {message.subject}")
```

### Async Mode (Faster for multiple requests)

```python
import asyncio
from pybarid import BaridClient

async def main():
    client = BaridClient(async_mode=True)
    
    # Generate multiple emails
    emails = await client.generate_emails_batch(5)
    
    # Check messages for all emails concurrently
    all_messages = await client.get_messages_batch(emails)
    
    for email, messages in all_messages.items():
        print(f"{email}: {len(messages)} messages")

asyncio.run(main())
```

## API

### Sync Methods

```python
# Generate email
email = client.generate_email()
email = client.generate_email(domain="example.com")

# Get messages
messages = client.get_messages(email.address, email.domain)

# Wait for message
message = client.wait_for_message(email.address, email.domain, timeout=60)

# Get web inbox
url = client.get_inbox_url(email.address, email.domain)
```

### Async Methods

```python
# Generate email
email = await client.generate_email_async()
email = await client.generate_email_async(domain="example.com")

# Get messages
messages = await client.get_messages_async(email.address, email.domain)

# Wait for message
message = await client.wait_for_message_async(email.address, email.domain, timeout=60)

# Batch operations
emails = await client.generate_emails_batch(5)
all_messages = await client.get_messages_batch(emails)
```

## Credits

Uses [Barid API](https://api.barid.site/) by [vwh]([https://vwh.sh/](https://github.com/vwh)).

---

Made by [oxno1](https://github.com/oxno1) 
