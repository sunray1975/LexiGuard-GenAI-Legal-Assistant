import re
import html
from typing import Dict, Any, Tuple

class LegalSecurityManager:
    """
    Enterprise Security Manager for Legal Document Processing.
    Handles PII Redaction, Prompt Injection Prevention, and XSS Sanitization.
    """

    # Regex patterns for sensitive PII
    EMAIL_PATTERN = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    PHONE_PATTERN = r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    SSN_PATTERN = r'\b\d{3}-\d{2}-\d{4}\b'
    CREDIT_CARD_PATTERN = r'\b(?:\d[ -]*?){13,16}\b'

    # Known prompt injection payloads
    INJECTION_PATTERNS = [
        r'ignore previous instructions',
        r'system prompt',
        r'override instructions',
        r'you are now DAN',
        r'reveal api key',
        r'print environment variables'
    ]

    @staticmethod
    def sanitize_input_text(text: str) -> str:
        """Sanitizes raw text to prevent XSS attacks."""
        if not text:
            return ""
        return html.escape(text.strip())

    @classmethod
    def redact_pii(cls, text: str) -> Tuple[str, Dict[str, int]]:
        """
        Redacts Personally Identifiable Information (PII) before LLM submission.
        Returns redacted text and count of redacted elements.
        """
        redacted = text
        counts = {"emails": 0, "phones": 0, "ssns": 0, "cards": 0}

        emails = re.findall(cls.EMAIL_PATTERN, redacted)
        counts["emails"] = len(emails)
        redacted = re.sub(cls.EMAIL_PATTERN, "[REDACTED_EMAIL]", redacted)

        phones = re.findall(cls.PHONE_PATTERN, redacted)
        counts["phones"] = len(phones)
        redacted = re.sub(cls.PHONE_PATTERN, "[REDACTED_PHONE]", redacted)

        ssns = re.findall(cls.SSN_PATTERN, redacted)
        counts["ssns"] = len(ssns)
        redacted = re.sub(cls.SSN_PATTERN, "[REDACTED_SSN]", redacted)

        cards = re.findall(cls.CREDIT_CARD_PATTERN, redacted)
        counts["cards"] = len(cards)
        redacted = re.sub(cls.CREDIT_CARD_PATTERN, "[REDACTED_CARD]", redacted)

        return redacted, counts

    @classmethod
    def validate_prompt_safety(cls, prompt_text: str) -> Tuple[bool, str]:
        """
        Scans input for malicious prompt injection attempts.
        Returns (is_safe, message).
        """
        lower = prompt_text.lower()
        for pattern in cls.INJECTION_PATTERNS:
            if re.search(pattern, lower):
                return False, f"Potential prompt injection detected: matching pattern '{pattern}'"
        return True, "Safe"
