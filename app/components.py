import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, Any, List

def inject_custom_css():
    """Injects high-end glassmorphism dark theme CSS."""
    st.markdown("""
        <style>
        /* Main background & typography */
        .stApp {
            background: linear-gradient(135deg, #0F172A 0%, #1E293B 50%, #0F172A 100%);
            color: #F8FAFC;
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
        }
        
        /* Glassmorphism cards */
        .glass-card {
            background: rgba(30, 41, 59, 0.7);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        }

        /* Metric badge styles */
        .metric-badge {
            display: inline-block;
            padding: 6px 14px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .badge-high {
            background-color: rgba(239, 68, 68, 0.2);
            color: #EF4444;
            border: 1px solid #EF4444;
        }
        .badge-med {
            background-color: rgba(245, 158, 11, 0.2);
            color: #F59E0B;
            border: 1px solid #F59E0B;
        }
        .badge-low {
            background-color: rgba(16, 185, 129, 0.2);
            color: #10B981;
            border: 1px solid #10B981;
        }

        /* Hero Header banner */
        .hero-banner {
            background: linear-gradient(90deg, #3B82F6 0%, #8B5CF6 50%, #EC4899 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
            font-size: 2.6rem;
            margin-bottom: 0.2rem;
        }

        .genai-pill {
            background: rgba(139, 92, 246, 0.2);
            border: 1px solid #8B5CF6;
            color: #DDD6FE;
            padding: 4px 12px;
            border-radius: 16px;
            font-size: 0.8rem;
            font-weight: 600;
        }
        </style>
    """, unsafe_allow_html=True)

def render_risk_gauge(score: int, title: str = "Overall Contract Risk Score"):
    """Renders Plotly gauge chart for contract risk score."""
    if score >= 65:
        color = "#EF4444"
    elif score >= 40:
        color = "#F59E0B"
    else:
        color = "#10B981"

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title, 'font': {'size': 18, 'color': '#F8FAFC'}},
        number={'suffix': "/100", 'font': {'size': 32, 'color': color}},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "#94A3B8"},
            'bar': {'color': color},
            'bgcolor': "rgba(30, 41, 59, 0.5)",
            'bordercolor': "rgba(255, 255, 255, 0.2)",
            'steps': [
                {'range': [0, 40], 'color': "rgba(16, 185, 129, 0.15)"},
                {'range': [40, 65], 'color': "rgba(245, 158, 11, 0.15)"},
                {'range': [65, 100], 'color': "rgba(239, 68, 68, 0.15)"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': score
            }
        }
    ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=50, b=20),
        height=220
    )
    return fig

def render_genai_mapping_card():
    """Renders GenAI Integration Architecture breakdown as required by PromptWars guidelines."""
    st.markdown("""
        <div class="glass-card">
            <h4>🧠 Explicit GenAI Architecture & Integration Mapping</h4>
            <table style="width:100%; border-collapse: collapse; margin-top: 10px; font-size: 0.9rem;">
                <thead>
                    <tr style="border-bottom: 1px solid rgba(255,255,255,0.2); text-align: left; color: #94A3B8;">
                        <th style="padding: 8px;">Feature Module</th>
                        <th style="padding: 8px;">GenAI Model & Service</th>
                        <th style="padding: 8px;">Exact Integration Point</th>
                    </tr>
                </thead>
                <tbody>
                    <tr style="border-bottom: 1px solid rgba(255,255,255,0.1);">
                        <td style="padding: 8px; font-weight:600;">Plain English Simplifier</td>
                        <td style="padding: 8px;"><span class="genai-pill">Google Gemini 1.5 Flash</span></td>
                        <td style="padding: 8px;">Translates dense legalese into Grade-8 reading level summary & key takeaways.</td>
                    </tr>
                    <tr style="border-bottom: 1px solid rgba(255,255,255,0.1);">
                        <td style="padding: 8px; font-weight:600;">Red Flag & Risk Detector</td>
                        <td style="padding: 8px;"><span class="genai-pill">Structured Prompting & Risk Classifier</span></td>
                        <td style="padding: 8px;">Parses clauses, extracts unfair terms (unlimited liability, non-competes), assigns 0-100 risk score.</td>
                    </tr>
                    <tr style="border-bottom: 1px solid rgba(255,255,255,0.1);">
                        <td style="padding: 8px; font-weight:600;">Contract Comparator</td>
                        <td style="padding: 8px;"><span class="genai-pill">Dual-Doc Comparative Diff Engine</span></td>
                        <td style="padding: 8px;">Side-by-side contract diffing highlighting liability cap shifts, SLA changes, and risk deltas.</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px; font-weight:600;">Grounded Legal QA Assistant</td>
                        <td style="padding: 8px;"><span class="genai-pill">RAG Grounded QA Engine</span></td>
                        <td style="padding: 8px;">Answers natural questions strictly grounded in document text with direct clause citations.</td>
                    </tr>
                </tbody>
            </table>
        </div>
    """, unsafe_allow_html=True)
