class GuardrailViolationError(Exception):
    """Raised when input or output violates guardrail rules."""
    pass


class RetrievalError(Exception):
    """Raised when document retrieval fails."""
    pass


class LLMServiceError(Exception):
    """Raised when LLM generation fails."""
    pass
