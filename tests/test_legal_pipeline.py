import sys
import os
import pytest

# Ensure parent path is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.document_parser import DocumentParser
from src.genai_engine import GenAILegalEngine
from src.risk_analyzer import LegalRiskAnalyzer
from src.contract_comparator import ContractComparator
from src.qa_assistant import LegalQAAssistant

SAMPLE_NDA_TEXT = """
MUTUAL NON-DISCLOSURE AGREEMENT
1. CONFIDENTIAL INFORMATION
Receiving Party shall hold and maintain Confidential Information in strictest confidence.
2. INDEMNIFICATION AND UNLIMITED LIABILITY
Receiving Party agrees to indemnify Disclosing Party. Receiving Party liability shall be UNLIMITED.
3. GOVERNING LAW
This Agreement shall be governed by Delaware law.
"""

def test_document_parser():
    parsed = DocumentParser.parse_raw_text(SAMPLE_NDA_TEXT)
    assert parsed["word_count"] > 0
    assert len(parsed["clauses"]) >= 2

def test_genai_engine_fallback():
    engine = GenAILegalEngine(api_key=None)
    res = engine.simplify_and_summarize(SAMPLE_NDA_TEXT)
    assert "plain_english_summary" in res
    assert len(res["key_takeaways"]) > 0

def test_risk_analyzer():
    parsed = DocumentParser.parse_raw_text(SAMPLE_NDA_TEXT)
    risk = LegalRiskAnalyzer.analyze_contract(parsed)
    assert risk["overall_risk_score"] > 30
    assert len(risk["flagged_clauses"]) > 0
    assert any(c["category"] == "Unlimited Liability & Indemnity" for c in risk["flagged_clauses"])

def test_contract_comparator():
    doc_a = DocumentParser.parse_raw_text(SAMPLE_NDA_TEXT)
    doc_b = DocumentParser.parse_raw_text(SAMPLE_NDA_TEXT.replace("UNLIMITED", "Capped at $50,000"))
    comp = ContractComparator.compare_contracts(doc_a, doc_b)
    assert "score_delta" in comp
    assert len(comp["comparisons"]) > 0

def test_qa_assistant():
    parsed = DocumentParser.parse_raw_text(SAMPLE_NDA_TEXT)
    qa = LegalQAAssistant.answer_question("What is the governing law?", parsed)
    assert "Delaware" in qa["answer_markdown"] or "Direct Answer" in qa["answer_markdown"]
