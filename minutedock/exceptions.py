"""MinuteDock API Wrapper exception classes"""


class MinuteDockException(Exception):
    """Base MinuteDock API Wrapper Exception that all other exception classes extend."""


class ClientException(MinuteDockException):
    """Indicate exceptions not involving an interaction with MinuteDock's API"""
