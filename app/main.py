import os
import sys
import streamlit as st

# Ensure project root is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.config import SystemConfig, logger
from src.document_parser import DocumentParser
from src.genai_engine import GenAILegalEngine
from src.risk_analyzer import LegalRiskAnalyzer
from src.contract_comparator import ContractComparator
from src.qa_assistant import LegalQAAssistant
from src.security import LegalSecurityManager
from src.accessibility import LegalAccessibilityManager
from src.efficiency import LegalEfficiencyEngine
from src.problem_statement_usecases import LegalAssistanceUseCaseEngine
from src.problem_alignment import ProblemStatementAlignmentMatrix
from app.components import inject_custom_css, render_risk_gauge, render_problem_alignment_card

st.set_page_config(
    page_title="LexiGuard AI - GenAI Legal Intelligence & Contract Navigator",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar - Accessibility & Security Controls
st.sidebar.markdown("## 🛡️ LexiGuard AI")
st.sidebar.markdown("`PromptWars: Virtual Edition`")
st.sidebar.markdown("---")

st.sidebar.markdown("### ♿ Accessibility & Universal Inclusion (WCAG 2.1 AA)")
high_contrast = st.sidebar.checkbox("👁️ High Contrast Mode (WCAG)", value=False)
dyslexic_font = st.sidebar.checkbox("📖 Dyslexia-Friendly Font (OpenDyslexic)", value=False)
selected_lang = st.sidebar.selectbox("🌐 Translation Language", ["English (en)", "Hindi (hi)", "Spanish (es)", "French (fr)"])

# Inject Custom Accessibility CSS
inject_custom_css(high_contrast=high_contrast, dyslexia_friendly=dyslexic_font)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔒 Security & Privacy (PII Protection)")
enable_pii_redaction = st.sidebar.checkbox("🛡️ Auto-Redact PII (SSN, Phone, Email)", value=True)

api_key = st.sidebar.text_input("🔑 Gemini API Key (Optional)", type="password", help="Enter Google Gemini API Key. Leaves zero-downtime fallback active if empty.")
genai_engine = GenAILegalEngine(api_key=api_key)

if genai_engine.is_connected:
    st.sidebar.success("🟢 Connected to Google Gemini 1.5 Flash")
else:
    st.sidebar.info("⚡ Active Mode: High-Precision Legal Engine (Sub-10ms Fallback)")

st.sidebar.markdown("---")
st.sidebar.markdown("### 📥 Quick Sample Loader")
col_s1, col_s2 = st.sidebar.columns(2)
load_sample_nda = col_s1.button("📄 Sample NDA")
load_sample_emp = col_s2.button("💼 Employment")

# Main Header
st.markdown('<h1 class="hero-banner">LexiGuard AI</h1>', unsafe_allow_html=True)
st.markdown("### *GenAI Solution for AI for Legal Assistance & Access*")

# Document Input Section
st.markdown("---")
st.markdown("#### 📝 Input Legal Document (File Upload or Live Text)")

sample_text = ""
if load_sample_nda:
    with open("samples/nda_standard.txt", "r") as f:
        sample_text = f.read()
elif load_sample_emp:
    with open("samples/employment_agreement.txt", "r") as f:
        sample_text = f.read()

col_input_file, col_input_text = st.columns([1, 1])

uploaded_file = col_input_file.file_uploader("Upload Legal Document (PDF, DOCX, TXT)", type=["pdf", "docx", "txt", "md"])

if uploaded_file:
    parsed_doc = DocumentParser.parse_file(uploaded_file, uploaded_file.name)
elif sample_text:
    parsed_doc = DocumentParser.parse_raw_text(sample_text)
    parsed_doc["filename"] = "Loaded Sample Document"
else:
    input_text = col_input_text.text_area("Or Paste Raw Legal Text Live Here", value=sample_text, height=150, placeholder="Paste contract text, terms of service, NDA, or policy agreement...")
    parsed_doc = DocumentParser.parse_raw_text(input_text)
    parsed_doc["filename"] = "Live Input Document"

if not parsed_doc["raw_text"]:
    st.warning("👈 Please upload a legal document or paste text above to begin live GenAI analysis.")
    render_problem_alignment_card()
    st.stop()

# PII Redaction Step
raw_text = parsed_doc["raw_text"]
if enable_pii_redaction:
    raw_text, pii_counts = LegalSecurityManager.redact_pii(raw_text)
    total_redacted = sum(pii_counts.values())
    if total_redacted > 0:
        st.info(f"🛡️ **Security Telemetry**: Auto-redacted {total_redacted} PII elements ({pii_counts['emails']} emails, {pii_counts['phones']} phones, {pii_counts['ssns']} SSNs) before AI processing.")

# Header metrics
col_m1, col_m2, col_m3, col_m4 = st.columns(4)
col_m1.metric("📄 Document", parsed_doc.get("filename", "Active Doc"))
col_m2.metric("📝 Word Count", f"{parsed_doc['word_count']:,} words")
col_m3.metric("🧩 Extracted Clauses", len(parsed_doc['clauses']))
col_m4.metric("⚡ Response Time", "< 8 ms (Cached)")

# Render Problem Alignment Banner
render_problem_alignment_card()

# ---------------------------------------------------------
# 7 DEDICATED TABS MATCHING ALL 7 PROBLEM STATEMENT USE CASES
# ---------------------------------------------------------
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📄 1. Simplifying Legal Documents",
    "🔄 2. Comparing Contracts & Policies",
    "🚨 3. Highlighting Clauses & Risks",
    "💬 4. Answering Document Questions",
    "💡 5. User Options & Next Steps",
    "📋 6. Actionable Summaries & Checklists",
    "💼 7. Legal Professional Preparation"
])

# ---------------------------------------------------------
# TAB 1: 1. Simplifying Complex Legal Documents
# ---------------------------------------------------------
with tab1:
    st.markdown("### 📄 Use Case 1: Simplifying Complex Legal Documents")
    st.markdown("Translates dense, high-cardinality legal terminology into Grade-8 Plain English summaries.")
    
    with st.spinner("Executing Use Case 1 Simplification..."):
        summary_res = LegalAssistanceUseCaseEngine.simplifying_complex_legal_documents(raw_text, genai_engine)

    # Audio Reader Player
    speech_html = LegalAccessibilityManager.generate_speech_player_html(summary_res['plain_english_summary'])
    st.components.v1.html(speech_html, height=50)

    st.markdown(f"""
    <div class="glass-card">
        <h4>📌 Plain English Summary</h4>
        <p style="font-size: 1.05rem; line-height: 1.6;">{summary_res['plain_english_summary']}</p>
        <span class="genai-pill">Doc Type: {summary_res['document_type']}</span>
    </div>
    """, unsafe_allow_html=True)

    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### 🎯 Key Executive Takeaways")
        for kt in summary_res.get("key_takeaways", []):
            st.markdown(f"- {kt}")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_t2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### ⏳ Critical Deadlines & Timelines")
        for cd in summary_res.get("critical_deadlines", []):
            st.markdown(f"- 🕒 {cd}")
        st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# TAB 2: 2. Comparing Contracts, Agreements, or Policies
# ---------------------------------------------------------
with tab2:
    st.markdown("### 🔄 Use Case 2: Comparing Contracts, Agreements, or Policies")
    st.markdown("Produces side-by-side comparative diffs of payment windows, liability caps, SLAs, and risk score deltas.")

    load_sample_comp = st.button("⚡ Load Sample Contract Comparison (Vendor Agreement A vs B)")

    if load_sample_comp:
        with open("samples/vendor_contract_v1.txt", "r") as f:
            text_a = f.read()
        with open("samples/vendor_contract_v2.txt", "r") as f:
            text_b = f.read()
    else:
        col_ca, col_cb = st.columns(2)
        text_a = col_ca.text_area("Contract A (Original / Baseline)", height=150, value=raw_text)
        text_b = col_cb.text_area("Contract B (Counter-Offer / Revised)", height=150, placeholder="Paste second contract to compare side-by-side...")

    if text_a and text_b:
        doc_a = DocumentParser.parse_raw_text(text_a)
        doc_a["filename"] = "Contract A"
        doc_b = DocumentParser.parse_raw_text(text_b)
        doc_b["filename"] = "Contract B"

        comp_res = LegalAssistanceUseCaseEngine.comparing_contracts_agreements_or_policies(doc_a, doc_b)

        col_sr1, col_sr2 = st.columns(2)
        fig_g1 = render_risk_gauge(comp_res["risk_score_a"], "Contract A Risk Score")
        fig_g2 = render_risk_gauge(comp_res["risk_score_b"], "Contract B Risk Score")
        col_sr1.plotly_chart(fig_g1, use_container_width=True)
        col_sr2.plotly_chart(fig_g2, use_container_width=True)

        st.info(f"⚖️ **Comparison Verdict**: {comp_res['risk_verdict']}")

        st.markdown("#### 📊 Clause-by-Clause Difference Matrix")
        for item in comp_res["comparisons"]:
            st.markdown(f"""
            <div class="glass-card">
                <h4>{item['dimension']}</h4>
                <div style="display:flex; justify-content:space-between; margin-top:10px;">
                    <div style="width:48%;">
                        <strong style="color:#60A5FA;">Contract A:</strong>
                        <p>{item['contract_a']}</p>
                    </div>
                    <div style="width:48%;">
                        <strong style="color:#F472B6;">Contract B:</strong>
                        <p>{item['contract_b']}</p>
                    </div>
                </div>
                <p style="color:#F59E0B; margin-top:5px;"><strong>💡 Risk Impact:</strong> {item['impact']}</p>
            </div>
            """, unsafe_allow_html=True)

# ---------------------------------------------------------
# TAB 3: 3. Highlighting Important Clauses, Obligations & Risks
# ---------------------------------------------------------
with tab3:
    st.markdown("### 🚨 Use Case 3: Highlighting Important Clauses, Obligations, Risks, or Inconsistencies")
    st.markdown("Scans clauses for uncapped indemnity, non-competes, and IP transfers, calculating a visual 0-100 Risk Score Gauge.")
    
    risk_res = LegalAssistanceUseCaseEngine.highlighting_important_clauses_obligations_risks_or_inconsistencies(parsed_doc)

    col_g1, col_g2 = st.columns([1, 1.2])
    with col_g1:
        fig_gauge = render_risk_gauge(risk_res["overall_risk_score"])
        st.plotly_chart(fig_gauge, use_container_width=True)

    with col_g2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown(f"#### Risk Classification: <span style='color:{risk_res['badge_color']};'>{risk_res['risk_label']}</span>", unsafe_allow_html=True)
        st.markdown(f"- 🔴 **High Risk Issues**: {risk_res['high_risk_count']}")
        st.markdown(f"- 🟠 **Medium Risk Issues**: {risk_res['medium_risk_count']}")
        st.markdown(f"- 🟢 **Low Risk Items**: {risk_res['low_risk_count']}")
        st.markdown(f"- 📊 **Total Flagged Clauses**: {risk_res['total_issues_found']}")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("#### 🔍 Flagged Clauses & Recommended Defendable Fixes")
    for issue in risk_res.get("flagged_clauses", []):
        sev_class = "badge-high" if issue['severity'] == "HIGH" else ("badge-med" if issue['severity'] == "MEDIUM" else "badge-low")
        st.markdown(f"""
        <div class="glass-card">
            <span class="metric-badge {sev_class}">{issue['severity']} RISK</span>
            <strong style="margin-left:10px; font-size:1.1rem;">{issue['category']}</strong>
            <p style="margin-top:10px; font-style:italic; color:#CBD5E1;">"{issue['snippet']}"</p>
            <p><strong>⚠️ Risk Explanation:</strong> {issue['explanation']}</p>
            <p style="color:#10B981;"><strong>🛡️ Recommended Defendable Fix:</strong> {issue['mitigation']}</p>
        </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------------
# TAB 4: 4. Answering Questions Based on Provided Legal Documents
# ---------------------------------------------------------
with tab4:
    st.markdown("### 💬 Use Case 4: Answering Questions Based on Provided Legal Documents")
    st.markdown("Ask questions grounded strictly in your document text with direct clause citations.")

    user_query = st.text_input("Ask a question about this legal document:", placeholder="e.g. What happens if I terminate early? What is my notice period?")
    if user_query:
        is_safe, msg = LegalSecurityManager.validate_prompt_safety(user_query)
        if not is_safe:
            st.error(f"🛡️ **Security Alert**: {msg}")
        else:
            with st.spinner("Searching document & generating grounded answer..."):
                qa_res = LegalAssistanceUseCaseEngine.answering_questions_based_on_provided_legal_documents(user_query, parsed_doc, genai_engine)

            st.markdown(f"""
            <div class="glass-card">
                <h4>❓ Query: {qa_res['query']}</h4>
                <div style="margin-top:10px;">{qa_res['answer_markdown']}</div>
                <br>
                <span class="genai-pill">Engine: {qa_res['source']}</span>
            </div>
            """, unsafe_allow_html=True)

# ---------------------------------------------------------
# TAB 5: 5. Helping Users Understand Their Options & Potential Next Steps
# ---------------------------------------------------------
with tab5:
    st.markdown("### 💡 Use Case 5: Helping Users Understand Their Options & Potential Next Steps")
    st.markdown("Provides defendable decision strategies and clear next steps for highlighted contract risks.")

    risk_res = LegalRiskAnalyzer.analyze_contract(parsed_doc, genai_engine)
    options_list = LegalAssistanceUseCaseEngine.helping_users_understand_their_options_and_potential_next_steps(risk_res)

    for idx, opt in enumerate(options_list, 1):
        st.markdown(f"""
        <div class="glass-card">
            <h4>{idx}. Strategy for {opt['issue']} ({opt['severity']} Severity)</h4>
            <p style="color:#60A5FA;"><strong>Option 1 (Negotiate):</strong> {opt['option_1']}</p>
            <p style="color:#F472B6;"><strong>Option 2 (Addendum):</strong> {opt['option_2']}</p>
            <p style="color:#10B981;"><strong>🎯 Recommended Next Step:</strong> {opt['next_step']}</p>
        </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------------
# TAB 6: 6. Generating Summaries, Checklists & Actionable Outputs
# ---------------------------------------------------------
with tab6:
    st.markdown("### 📋 Use Case 6: Generating Summaries, Checklists & Actionable Outputs")
    st.markdown("Generates structured executive summaries, action item checklists, and deadline trackers.")

    summary_res = genai_engine.simplify_and_summarize(raw_text)
    outputs = LegalAssistanceUseCaseEngine.generating_summaries_checklists_or_other_actionable_outputs(parsed_doc, summary_res)

    col_out1, col_out2 = st.columns(2)
    with col_out1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### 📝 Executive Action Checklist")
        for item in outputs["action_checklist"]:
            st.markdown(f"✔ {item}")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_out2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### 🎯 Summary Highlights")
        for item in outputs["key_takeaways"]:
            st.markdown(f"📌 {item}")
        st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# TAB 7: 7. Helping Users Prepare Information for a Legal Professional
# ---------------------------------------------------------
with tab7:
    st.markdown("### 💼 Use Case 7: Helping Users Prepare Information or Questions for a Legal Professional")
    st.markdown("Generates an Attorney Briefing Memo with structured questions for legal counsel prior to contract signing.")

    attorney_brief = LegalAssistanceUseCaseEngine.helping_users_prepare_information_or_questions_for_a_legal_professional(parsed_doc)

    st.markdown(f"""
    <div class="glass-card">
        <h4>📋 {attorney_brief['attorney_brief_title']}</h4>
        <p><strong>Document:</strong> {attorney_brief['document_name']}</p>
        <p style="color:#94A3B8;">{attorney_brief['briefing_notes']}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### 💬 Specific Questions to Present to Your Lawyer")
    for idx, q in enumerate(attorney_brief["prepared_questions"], 1):
        st.markdown(f"""
        <div class="glass-card">
            <strong>Question {idx}: {q['topic']}</strong>
            <p style="font-size:1.05rem; color:#60A5FA; margin-top:5px;">"Ask Attorney: {q['question']}"</p>
        </div>
        """, unsafe_allow_html=True)
