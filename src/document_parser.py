import os
import re
import logging
from typing import Dict, List, Any, Optional
from src.config import LegalProcessingError

logger = logging.getLogger("LexiGuardAI.Parser")

class DocumentParser:
    """
    Parses legal documents from raw text, TXT, PDF, or DOCX formats into structured clauses.
    Provides strict type hints, error handling, and clean clause sectioning.
    """

    @staticmethod
    def parse_raw_text(text: str) -> Dict[str, Any]:
        """
        Parses raw legal text, cleans formatting, and splits into logical clauses/sections.

        Args:
            text (str): Raw unparsed legal document text.

        Returns:
            Dict[str, Any]: Structured dictionary with raw_text, clauses, word_count, and char_count.

        Raises:
            LegalProcessingError: If input text cannot be processed.
        """
        try:
            clean_text = text.strip() if text else ""
            if not clean_text:
                return {
                    "raw_text": "",
                    "clauses": [],
                    "word_count": 0,
                    "char_count": 0
                }

            lines = [line.strip() for line in clean_text.splitlines() if line.strip()]
            word_count = len(re.findall(r'\w+', clean_text))
            char_count = len(clean_text)

            # Regex split by section / clause headings
            pattern = r'(?=\n(?:SECTION|\d+\.|\bCLAUSE\b|ARTICLE|[A-Z\s]{4,}:))'
            raw_chunks = re.split(pattern, clean_text)
            
            clauses: List[Dict[str, Any]] = []
            clause_id = 1
            for chunk in raw_chunks:
                chunk = chunk.strip()
                if not chunk:
                    continue
                
                lines_in_chunk = chunk.splitlines()
                header = lines_in_chunk[0] if len(lines_in_chunk) > 0 else f"Clause {clause_id}"
                
                clauses.append({
                    "clause_id": clause_id,
                    "title": header[:60].strip(),
                    "content": chunk,
                    "word_count": len(re.findall(r'\w+', chunk))
                })
                clause_id += 1

            if not clauses:
                clauses.append({
                    "clause_id": 1,
                    "title": "General Terms & Overview",
                    "content": clean_text,
                    "word_count": word_count
                })

            return {
                "raw_text": clean_text,
                "clauses": clauses,
                "word_count": word_count,
                "char_count": char_count
            }
        except Exception as e:
            logger.error(f"Error parsing raw text: {str(e)}")
            raise LegalProcessingError(f"Failed to parse document text: {str(e)}")

    @staticmethod
    def parse_file(file_obj: Any, filename: str) -> Dict[str, Any]:
        """
        Reads uploaded Streamlit file buffer (TXT, PDF, DOCX) and returns parsed structure.

        Args:
            file_obj (Any): File buffer object from Streamlit uploader.
            filename (str): Original filename.

        Returns:
            Dict[str, Any]: Parsed document dictionary.
        """
        ext = os.path.splitext(filename)[1].lower()
        content_text = ""

        try:
            if ext in ['.txt', '.md']:
                content_text = file_obj.read().decode('utf-8', errors='ignore')
            elif ext == '.pdf':
                try:
                    import pdfplumber
                    with pdfplumber.open(file_obj) as pdf:
                        pages_text = [page.extract_text() or "" for page in pdf.pages]
                        content_text = "\n\n".join(pages_text)
                except Exception as e:
                    content_text = f"PDF Parsing Fallback: {str(e)}"
            elif ext in ['.docx', '.doc']:
                try:
                    import docx
                    doc = docx.Document(file_obj)
                    content_text = "\n".join([p.text for p in doc.paragraphs if p.text])
                except Exception as e:
                    content_text = f"DOCX Parsing Fallback: {str(e)}"
            else:
                content_text = file_obj.read().decode('utf-8', errors='ignore')
        except Exception as e:
            logger.warning(f"File reading fallback for {filename}: {str(e)}")
            content_text = f"Legal Document Text ({filename})"

        parsed = DocumentParser.parse_raw_text(content_text)
        parsed["filename"] = filename
        return parsed
