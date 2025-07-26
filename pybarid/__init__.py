"""
PyBarid - Python library for Barid temporary email service

Author: oxno1
API: https://api.barid.site/
API Creator: vwh (https://vwh.sh/)
"""

__version__ = "1.0.0"
__author__ = "oxno1"

from .client import BaridClient
from .models import Email, Message, Domain

__all__ = ["BaridClient", "Email", "Message", "Domain"] 