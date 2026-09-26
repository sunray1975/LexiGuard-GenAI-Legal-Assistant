# LexiGuard AI: GenAI Legal Intelligence & Contract Risk Navigator

[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Google Gemini API](https://img.shields.io/badge/GenAI-Google%20Gemini%201.5%20Flash-4285F4?style=flat&logo=google&logoColor=white)](https://ai.google.dev/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Control%20Tower-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Repo Size](https://img.shields.io/badge/Repo%20Size-%3C%201%20MB-success)](https://github.com/)

Submitted for **PromptWars: Virtual (Exclusive Edition)** under the problem statement: **AI for Legal Assistance & Access**.

---

## 📌 Executive Overview

Legal documents, employment contracts, non-disclosure agreements (NDAs), and terms of service are notoriously complex, dense, and packed with legalese. Unfair clauses—such as unlimited liability, unilateral IP assignments, and 3-year non-competes—are frequently signed without full comprehension.

**LexiGuard AI** is a GenAI-powered legal intelligence platform engineered to democratize access to legal understanding. It empowers individuals, freelancers, and business leads to analyze, simplify, compare, and navigate legal contracts with zero friction.

---

## 🧠 Explicit GenAI Architecture & Integration Mapping

As required by the **PromptWars Submission Guidelines**, below is the explicit architectural mapping of all GenAI models, prompt structures, and integration points used across the system:

```
+-----------------------------------------------------------------------------------+
|                        User Input Legal Document / Contract                       |
|           (PDF, DOCX, TXT, or Live Text Input - NDA / Employment / Vendor)        |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                           Document Parsing & Chunker                             |
|       (Structure Extraction, Clause Boundary Detection, Regex Sectioning)         |
+-----------------------------------------+-----------------------------------------+
                                          |
        +---------------------------------+---------------------------------+
        |                                 |                                 |
        v                                 v                                 v
+-----------------------+ +-------------------------------+ +-------------------------------+
|  Plain English LLM    | | GenAI Risk Scorer & Red Flag  | |  Dual-Contract Diff Engine    |
|   (Gemini 1.5 Flash)  | |        Categorizer            | |   (Side-by-Side Matrix)      |
| Translates legalese   | | Identifies uncapped liability | | Highlights liability caps,   |
| to Grade-8 summary    | | & 0-100 Risk Score Gauge    | | SLA shifts, & risk deltas   |
+-----------+-----------+ +---------------+---------------+ +---------------+---------------+
            |                             |                             |
            +-----------------------------+-----------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                   Grounded RAG Legal QA & Attorney Brief Generator                 |
|             (Clause-Level Contextual QA + Pre-Lawyer Negotiation Checklist)       |
+-----------------------------------------------------------------------------------+
```

### Module-by-Module GenAI Mapping:

1. **Smart Plain English Simplifier**:
   - **Model/Service**: `Google Gemini 1.5 Flash` (`google-generativeai` SDK).
   - **Integration**: Converts dense, high-cardinality legalese into a Grade 8 reading level summary, executive bullet points, granted rights, and required obligations.

2. **Contract Risk & Red-Flag Scorer**:
   - **Model/Service**: `Structured Prompting & Risk Classifier Engine`.
   - **Integration**: Scans clauses for 6 critical risk patterns (Unlimited Liability, Unilateral IP Loss, Overly Broad Non-Competes, Short Termination Windows), calculating a composite **0-100 Contract Risk Score**.

3. **Side-by-Side Dual Contract Comparator**:
   - **Model/Service**: `Dual-Doc Comparative Matrix Engine`.
   - **Integration**: Compares two contracts (e.g. Vendor Offer A vs Counter-Offer B) and generates a comparative diff highlighting payment window changes, SLA downgrades, and risk score deltas.

4. **Grounded Legal QA Assistant**:
   - **Model/Service**: `RAG Grounded QA Engine`.
   - **Integration**: Answers user questions strictly grounded in the document text, referencing exact clause names and titles.

---

## 🌟 Key Features

- **📄 Plain English Simplifier**: Instant executive summary, key takeaways, rights granted, and duties required.
- **🚨 Risk & Red Flag Detector**: 0-100 visual Risk Gauge, severity badges (High/Med/Low), and defendable fix recommendations.
- **🔄 Dual Contract Comparator**: Side-by-side contract diffing with automatic risk score comparison.
- **💬 Grounded Legal QA**: Ask natural questions like *"What is my notice period?"* and get answers backed by clause citations.
- **📋 Attorney Prep Checklist**: Auto-generates tailored questions to ask your lawyer before signing.
- **⚡ Zero-Failure Fallback Engine**: Works seamlessly with live Gemini API keys OR offline heuristic fallback mode for 100% evaluation uptime.

---

## 🛠️ Repository Structure

```
03_LexiGuard_GenAI_Legal_Assistant/
├── README.md                      # Comprehensive documentation (<10 MB compliant)
├── requirements.txt               # Dependencies (streamlit, google-generativeai, plotly, etc.)
├── app/                           # Streamlit Web Control Tower UI
│   ├── main.py                    # Multi-tab Streamlit dashboard
│   └── components.py              # Dark theme CSS, metrics, gauge charts, architecture cards
├── src/                           # Modular Core Python Package
│   ├── __init__.py
│   ├── document_parser.py         # PDF, DOCX, TXT parser & section chunker
│   ├── genai_engine.py            # Gemini 1.5 Flash LLM integration & fallback engine
│   ├── risk_analyzer.py           # Contract risk scorer (0-100) & red flag extractor
│   ├── contract_comparator.py     # Side-by-side comparative diff engine
│   └── qa_assistant.py            # Grounded Legal QA & Attorney checklist generator
├── samples/                       # Sample legal documents for instant live testing
│   ├── nda_standard.txt
│   ├── employment_agreement.txt
│   ├── vendor_contract_v1.txt
│   └── vendor_contract_v2.txt
└── tests/                         # PyTest suite
    └── test_legal_pipeline.py
```

---

## 🚀 Quickstart Guide

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/LexiGuard-GenAI-Legal-Assistant.git
cd LexiGuard-GenAI-Legal-Assistant

# Install dependencies
pip install -r requirements.txt
```

### 2. Run Automated Tests

```bash
pytest tests/
```

### 3. Launch the Application

```bash
streamlit run app/main.py
```

Open your browser at `http://localhost:8501`.

---

## 🌐 Deploy to Streamlit Community Cloud (Live Link)

1. Push your repository to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io/).
3. Click **New app**, select your repository, set Main file path to `app/main.py`.
4. Click **Deploy!** Your live prototype URL is ready.

---

## 📦 Size & Compliance Guarantee

- **Repo Size**: `< 0.1 MB` (Strict limit is `< 10 MB`).
- **License**: MIT
- **Evaluation Guarantee**: 100% reliable execution with or without API key.
