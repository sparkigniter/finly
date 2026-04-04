class PortfolioAnalysisError(Exception):
    """Base exception for portfolio analysis failures."""

    def __init__(self, message="A failure occurred during portfolio analysis"):
        self.message = message
        super().__init__(self.message)


class RateLimitError(PortfolioAnalysisError):
    """Raised when the AI Provider returns RESOURCE_EXHAUSTED (429)."""

    def __init__(self, message="AI Provider rate limit reached"):
        super().__init__(message)


class DataValidationError(PortfolioAnalysisError):
    """Raised when agent returns malformed or invalid JSON."""

    def __init__(self, message="Invalid data structure returned by agent"):
        super().__init__(message)
