from app.config import settings
from app.core.exceptions import GuardrailViolationError


class GuardrailService:
    def __init__(self):
        self.max_question_length = settings.MAX_QUESTION_LENGTH
        self.blocked_terms = [
            term.strip().lower()
            for term in settings.BLOCKED_TERMS.split(",")
            if term.strip()
        ]

    def validate_question(self, question: str) -> None:
        if not question or not question.strip():
            raise GuardrailViolationError("Question cannot be empty.")

        if len(question) > self.max_question_length:
            raise GuardrailViolationError(
                f"Question is too long. Maximum allowed length is {self.max_question_length} characters."
            )

        lower_question = question.lower()
        for term in self.blocked_terms:
            if term in lower_question:
                raise GuardrailViolationError(
                    f"Question contains blocked content: '{term}'"
                )

    def validate_answer(self, answer: str) -> str:
        if not answer or not answer.strip():
            raise GuardrailViolationError("Generated answer is empty.")

        cleaned_answer = answer.strip()

        if len(cleaned_answer) > 5000:
            cleaned_answer = cleaned_answer[:5000].strip()

        return cleaned_answer
