"""Custom exceptions for PyBarid"""


class BaridException(Exception):
    """Base exception for PyBarid"""
    pass


class BaridAPIError(BaridException):
    """API error"""
    pass


class BaridTimeoutError(BaridException):
    """Operation timeout"""
    pass


class BaridInvalidEmailError(BaridException):
    """Invalid email address"""
    pass


class BaridMessageNotFoundError(BaridException):
    """Message not found"""
    pass 