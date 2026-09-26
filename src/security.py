import re
import html
import hashlib
import logging
from typing import Dict, Any, Tuple
from src.config import PromptInjectionError

logger = logging.getLogger("LexiGuardAI.Security")

class LegalSecurityManager:
    """
    Enterprise Security Manager for Legal Document Processing.
    Handles PII Redaction, Prompt Injection Defense, SHA-256 Audit Integrity, and XSS Sanitization.
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
    def calculate_sha256(text: str) -> str:
        """Calculates SHA-256 hash of document text for security auditing."""
        return hashlib.sha256(text.encode('utf-8')).hexdigest()

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

        Args:
            text (str): Input text containing potential PII.

        Returns:
            Tuple[str, Dict[str, int]]: Redacted text and counts of redacted elements.
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

        logger.info(f"PII Redaction completed: {sum(counts.values())} items scrubbed")
        return redacted, counts

    @classmethod
    def validate_prompt_safety(cls, prompt_text: str) -> Tuple[bool, str]:
        """
        Scans input for malicious prompt injection attempts.

        Args:
            prompt_text (str): User prompt query.

        Returns:
            Tuple[bool, str]: (is_safe, message).
        """
        lower = prompt_text.lower()
        for pattern in cls.INJECTION_PATTERNS:
            if re.search(pattern, lower):
                logger.warning(f"Security Alert: Prompt injection pattern '{pattern}' blocked.")
                return False, f"Potential prompt injection detected: matching pattern '{pattern}'"
        return True, "Safe"
