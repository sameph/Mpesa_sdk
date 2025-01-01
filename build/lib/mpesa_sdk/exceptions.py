class MPesaError(Exception):
    """Base class for MPesa SDK errors."""
    pass

class AuthenticationError(MPesaError):
    """Raised when authentication fails."""
    pass

class APIRequestError(MPesaError):
    """Raised when an API request fails."""
    pass
