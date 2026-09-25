import re
from typing import Dict, List, Any

class LegalQAAssistant:
    """
    Grounded Legal Document QA & Attorney Briefing Assistant.
    Answers user queries strictly grounded in document text with clause citations.
    """

    @staticmethod
    def answer_question(query: str, parsed_doc: Dict[str, Any], genai_engine=None) -> Dict[str, Any]:
        raw_text = parsed_doc.get("raw_text", "")
        clauses = parsed_doc.get("clauses", [])
        query_lower = query.lower()

        # If Gemini LLM engine connected, generate grounded response
        if genai_engine and genai_engine.is_connected:
            prompt = f"""
You are LexiGuard AI, a Legal Assistant. Answer the user's question grounded STRICTLY in the provided legal document text below.
Cite specific clause titles or numbers where relevant.

DOCUMENT:
\"\"\"
{raw_text[:6000]}
\"\"\"

USER QUESTION: "{query}"

Provide your answer in structured Markdown format:
1. **Direct Answer**: Concise plain English answer.
2. **Relevant Clause Citation**: Quote or reference the exact section.
3. **Actionable Next Steps / Options**: What the user should do next.
"""
            try:
                res = genai_engine.model.generate_content(prompt)
                return {
                    "query": query,
                    "answer_markdown": res.text,
                    "source": "Google Gemini 1.5 Flash (Grounded RAG)"
                }
            except Exception:
                pass

        # Contextual Search Fallback
        matched_clause = None
        matched_text = ""

        # Search clauses for keyword matches
        keywords = re.findall(r'\w+', query_lower)
        keywords = [k for k in keywords if len(k) > 3 and k not in ['what', 'where', 'when', 'how', 'does', 'this', 'that', 'with', 'from', 'have', 'been']]

        best_clause = None
        max_matches = 0

        for c in clauses:
            content_lower = c["content"].lower()
            match_count = sum(1 for kw in keywords if kw in content_lower)
            if match_count > max_matches:
                max_matches = match_count
                best_clause = c

        if best_clause:
            answer_text = f"**Direct Answer based on {best_clause['title']}**:\n\n{best_clause['content']}\n\n**Actionable Advice**: Review this section with legal counsel if you require an amendment or exemption before signing."
            citation = best_clause['title']
        else:
            answer_text = f"**Direct Answer**: Based on a scan of the uploaded document, there is no explicit section directly addressing '{query}'.\n\n**Recommendation**: Request an explicit addendum from the counterparty to clarify this term."
            citation = "Full Document Scan"

        return {
            "query": query,
            "answer_markdown": answer_text,
            "citation": citation,
            "source": "LexiGuard Grounded Context Search"
        }

    @staticmethod
    def generate_attorney_checklist(parsed_doc: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        Generates structured negotiation questions and checklist for consulting a lawyer.
        """
        raw_text = parsed_doc.get("raw_text", "").lower()
        checklist = []

        if "indemnify" in raw_text or "unlimited" in raw_text:
            checklist.append({
                "topic": "Liability Cap Negotiation",
                "question": "Can we cap our indemnity obligation to the total contract value or insurance coverage limits?"
            })
        if "non-compete" in raw_text:
            checklist.append({
                "topic": "Non-Compete Scope Reduction",
                "question": "Is the 24-36 month non-compete duration legally enforceable in our jurisdiction, and can we narrow the geographic scope?"
            })
        if "work for hire" in raw_text or "inventions" in raw_text:
            checklist.append({
                "topic": "Intellectual Property Ownership",
                "question": "How do we draft an explicit Schedule A carve-out for pre-existing IP and personal projects?"
            })
        if "arbitration" in raw_text:
            checklist.append({
                "topic": "Dispute Resolution Venue",
                "question": "Should we request court litigation options for emergency injunctive relief instead of binding arbitration?"
            })

        if not checklist:
            checklist.append({
                "topic": "General Legal Review",
                "question": "Are there any ambiguous obligations or hidden recurring auto-renewal commitments in this agreement?"
            })

        return checklist
