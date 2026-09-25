import re
from typing import Dict, List, Any

class LegalRiskAnalyzer:
    """
    Contract Risk Scorer & Red Flag Extraction Engine.
    Categorizes clauses by risk severity (High / Medium / Low) and provides actionable fix recommendations.
    """

    @staticmethod
    def analyze_contract(parsed_doc: Dict[str, Any], genai_engine=None) -> Dict[str, Any]:
        raw_text = parsed_doc.get("raw_text", "")
        clauses = parsed_doc.get("clauses", [])
        lower_text = raw_text.lower()

        flagged_clauses = []
        high_risk_count = 0
        med_risk_count = 0
        low_risk_count = 0

        # Pattern detectors for key risk vectors
        risk_patterns = [
            {
                "category": "Unlimited Liability & Indemnity",
                "severity": "HIGH",
                "keywords": ["unlimited liability", "indemnify", "hold harmless", "all claims", "attorneys' fees"],
                "explanation": "One-sided indemnity clause exposing you to potentially uncapped financial liabilities for third-party claims.",
                "mitigation": "Insert a mutual liability cap tied to 12 months of contract fees or $50,000 max liability."
            },
            {
                "category": "Broad Non-Compete / Non-Solicit",
                "severity": "HIGH",
                "keywords": ["non-compete", "competing business", "3 years", "24 months", "worldwide"],
                "explanation": "Overly broad non-compete restriction (2-3 years) limiting your professional or commercial freedom.",
                "mitigation": "Narrow non-compete duration to 6-12 months and limit geography strictly to active client territories."
            },
            {
                "category": "Unilateral IP Transfer / Work For Hire",
                "severity": "HIGH",
                "keywords": ["sole and exclusive property", "work for hire", "personal devices", "all inventions"],
                "explanation": "Assigns 100% of intellectual property including work done on personal time or devices to the company.",
                "mitigation": "Carve out pre-existing IP, personal projects, and open-source contributions created outside work hours."
            },
            {
                "category": "Strict Short Termination & Asset Return",
                "severity": "MEDIUM",
                "keywords": ["24 hours", "5 days' written notice", "immediately return"],
                "explanation": "5-day termination window with 24-hour asset destruction puts extreme operational pressure on your team.",
                "mitigation": "Negotiate a 30-day cure period and 14 business days for asset transition."
            },
            {
                "category": "Dispute Arbitration & Class Waiver",
                "severity": "MEDIUM",
                "keywords": ["arbitration", "waives any right to a trial", "class-action"],
                "explanation": "Mandatory binding arbitration strips court litigation rights and class-action participation.",
                "mitigation": "Ensure arbitration cost-splitting and retain rights to seek injunctive relief in local courts."
            },
            {
                "category": "Governing Law & Jurisdiction",
                "severity": "LOW",
                "keywords": ["governing law", "jurisdiction", "delaware", "courts"],
                "explanation": "Standard choice of law clause establishing legal jurisdiction for disputes.",
                "mitigation": "Acceptable if neutral; prefer your home state/country jurisdiction if possible."
            }
        ]

        # Scan text against risk patterns
        for rule in risk_patterns:
            matched_keywords = [kw for kw in rule["keywords"] if kw in lower_text]
            if matched_keywords:
                sev = rule["severity"]
                if sev == "HIGH":
                    high_risk_count += 1
                elif sev == "MEDIUM":
                    med_risk_count += 1
                else:
                    low_risk_count += 1

                # Locate snippet
                snippet = "Clause matching " + ", ".join(matched_keywords)
                for c in clauses:
                    if any(kw in c["content"].lower() for kw in matched_keywords):
                        snippet = c["content"][:300] + "..."
                        break

                flagged_clauses.append({
                    "category": rule["category"],
                    "severity": sev,
                    "matched_keywords": matched_keywords,
                    "snippet": snippet,
                    "explanation": rule["explanation"],
                    "mitigation": rule["mitigation"]
                })

        # Calculate composite Risk Score (0 = Clean/Safe, 100 = Hazardous)
        base_score = (high_risk_count * 28) + (med_risk_count * 15) + (low_risk_count * 5)
        overall_risk_score = min(100, max(15, base_score))

        if overall_risk_score >= 65:
            risk_label = "HIGH RISK (Action Required)"
            badge_color = "red"
        elif overall_risk_score >= 40:
            risk_label = "MEDIUM RISK (Review Needed)"
            badge_color = "orange"
        else:
            risk_label = "LOW RISK (Standard Terms)"
            badge_color = "green"

        return {
            "overall_risk_score": overall_risk_score,
            "risk_label": risk_label,
            "badge_color": badge_color,
            "high_risk_count": high_risk_count,
            "medium_risk_count": med_risk_count,
            "low_risk_count": low_risk_count,
            "flagged_clauses": flagged_clauses,
            "total_issues_found": len(flagged_clauses)
        }
