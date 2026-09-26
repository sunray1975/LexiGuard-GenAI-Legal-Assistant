import base64
from typing import Dict, Any, List

class LegalAccessibilityManager:
    """
    Accessibility & Universal Inclusion Manager (WCAG 2.1 AA Compliant).
    Provides ARIA metadata, text-to-speech audio rendering, dyslexia-friendly layout, and multi-language translation.
    """

    TRANSLATIONS = {
        "hi": {  # Hindi
            "summary_title": "सरल हिंदी सारांश",
            "risk_title": "अनुबंध जोखिम स्कोर",
            "takeaways_title": "मुख्य बिंदु",
            "rights_title": "आपके अधिकार",
            "obligations_title": "आपकी जिम्मेदारियां"
        },
        "es": {  # Spanish
            "summary_title": "Resumen en Español Simple",
            "risk_title": "Puntuación de Riesgo del Contrato",
            "takeaways_title": "Puntos Clave",
            "rights_title": "Sus Derechos",
            "obligations_title": "Sus Obligaciones"
        },
        "fr": {  # French
            "summary_title": "Résumé en Français Simple",
            "risk_title": "Score de Risque du Contrat",
            "takeaways_title": "Points Clés",
            "rights_title": "Vos Droits",
            "obligations_title": "Vos Obligations"
        },
        "en": {
            "summary_title": "Plain English Summary",
            "risk_title": "Contract Risk Score",
            "takeaways_title": "Key Takeaways",
            "rights_title": "Your Rights",
            "obligations_title": "Your Obligations"
        }
    }

    @staticmethod
    def get_wcag_css(high_contrast: bool = False, dyslexia_friendly: bool = False) -> str:
        """Generates WCAG 2.1 AA compliant accessible CSS rules."""
        font_family = "'OpenDyslexic', 'Segoe UI', Arial, sans-serif" if dyslexia_friendly else "'Inter', sans-serif"
        
        if high_contrast:
            bg_color = "#000000"
            text_color = "#FFFF00"  # High visibility yellow on black
            card_bg = "#111111"
            border_color = "#FFFF00"
        else:
            bg_color = "#0F172A"
            text_color = "#F8FAFC"
            card_bg = "rgba(30, 41, 59, 0.7)"
            border_color = "rgba(255, 255, 255, 0.1)"

        return f"""
        <style>
        .stApp {{
            background-color: {bg_color} !important;
            color: {text_color} !important;
            font-family: {font_family} !important;
        }}
        .glass-card {{
            background: {card_bg} !important;
            border: 1px solid {border_color} !important;
            color: {text_color} !important;
        }}
        /* High contrast focus rings for keyboard accessibility */
        button:focus, input:focus, select:focus, textarea:focus {{
            outline: 3px solid #38BDF8 !important;
            outline-offset: 2px !important;
        }}
        </style>
        """

    @staticmethod
    def generate_speech_player_html(text: str) -> str:
        """
        Generates a native Web Speech API HTML5 Audio Player button for screen readers & visual impairment accessibility.
        """
        safe_text = text.replace('"', '&quot;').replace('\n', ' ')
        return f"""
        <div style="margin: 10px 0;">
            <button onclick="speakText('{safe_text[:500]}')" 
                    aria-label="Read legal summary aloud"
                    style="background-color: #0EA5E9; color: white; border: none; padding: 8px 16px; border-radius: 20px; cursor: pointer; font-weight: 600;">
                🔊 Listen to Summary (Screen Reader Audio)
            </button>
            <script>
            function speakText(text) {{
                if ('speechSynthesis' in window) {{
                    window.speechSynthesis.cancel();
                    var msg = new SpeechSynthesisUtterance(text);
                    msg.rate = 0.9;
                    window.speechSynthesis.speak(msg);
                }} else {{
                    alert('Text-to-speech is not supported in this browser.');
                }}
            }}
            </script>
        </div>
        """
