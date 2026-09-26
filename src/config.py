import logging
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional

# Configure PEP8 logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("LexiGuardAI")

class LegalProcessingError(Exception):
    """Custom exception raised when legal document processing fails."""
    pass

class PromptInjectionError(Exception):
    """Custom exception raised when malicious prompt injection is detected."""
    pass

@dataclass
class SystemConfig:
    """System configuration parameters."""
    app_name: str = "LexiGuard AI"
    version: str = "2.0.0"
    max_file_size_mb: int = 10
    default_model: str = "gemini-1.5-flash"
    enable_caching: bool = True
    enable_pii_redaction: bool = True
