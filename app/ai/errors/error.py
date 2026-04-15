"""Errors related to AI"""


class PortfolioAnalysisError(Exception):
    """Base exception for portfolio analysis failures."""

    def __init__(self, message="A failure occurred during portfolio analysis"):
        """Initializes a new instance of the class."""
        self.message = message
        super().__init__(self.message)


class RateLimitError(PortfolioAnalysisError):
    """Raised when the AI Provider returns RESOURCE_EXHAUSTED (429)."""

    def __init__(self, message="AI Provider rate limit reached"):
        """Initializes a new instance of the class."""
        super().__init__(message)


class DataValidationError(PortfolioAnalysisError):
    """Raised when agent returns malformed or invalid JSON."""

    def __init__(self, message="Invalid data structure returned by agent"):
        """Initializes a new instance of the class."""
        super().__init__(message)
