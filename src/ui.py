"""
Streamlit UI for German Translator with Gender-Colored Articles.
Grid layout with sidebar for Color Legend and Examples.
"""

import streamlit as st
from src.translator import translate_to_english, translate_to_spanish
from src.gender_detector import colorize_text_html, get_color_legend, GENDER_COLORS

# Color Palette
COLORS = {
    "sage_light": "#BFC3BA",      # Light sage - text, accents
    "gray_medium": "#A9ACA9",     # Medium gray - secondary text
    "purple_muted": "#60495A",    # Muted purple - borders, accents
    "purple_dark": "#2F2235",     # Dark purple - cards, sidebar
    "purple_darker": "#1A1520",   # Darkest purple - main background
    "black": "#0D0B0E",           # Near black - outer frame
}


def render_sidebar():
    """Render sidebar with Color Legend and Examples."""
    # ─────────────────────────────────────────
    # COLOR LEGEND BOX
    # ─────────────────────────────────────────
    legend = get_color_legend()
    legend_items = ""
    for label, color in legend.items():
        legend_items += f'<div style="display: flex; align-items: center; gap: 10px; padding: 6px 0;"><span style="width: 14px; height: 14px; background: {color}; border-radius: 50%; display: inline-block; flex-shrink: 0;"></span><span style="color: {COLORS["sage_light"]}; font-size: 14px;">{label}</span></div>'
    
    st.sidebar.markdown(
        f'<div style="background: {COLORS["purple_dark"]}; border: 2px solid {COLORS["purple_muted"]}; border-radius: 8px; padding: 20px; margin-bottom: 20px;"><h3 style="color: {COLORS["sage_light"]}; margin: 0 0 15px 0; font-size: 16px; font-weight: 600;">🎨 Color Legend</h3>{legend_items}</div>',
        unsafe_allow_html=True
    )
    
    # ─────────────────────────────────────────
    # EXAMPLES BOX
    # ─────────────────────────────────────────
    st.sidebar.markdown(
        f'<h3 style="color: {COLORS["sage_light"]}; margin: 0 0 10px 0; font-size: 16px; font-weight: 600;">📝 Examples</h3>',
        unsafe_allow_html=True
    )
    
    examples = [
        "Der Hund spielt mit der Katze.",
        "Die Frau liest das Buch.",
        "Das Kind isst einen Apfel.",
        "Die Kinder spielen im Garten.",
    ]
    
    for example in examples:
        if st.sidebar.button(example, key=example):
            st.session_state.example_text = example
            st.rerun()


def main():
    """Main function to run the Streamlit app."""
    # Page configuration
    st.set_page_config(
        page_title="German Translator",
        page_icon="🇩🇪",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS
    st.markdown(
        f"""
        <style>
        /* Main app background */
        .stApp {{
            background-color: {COLORS["black"]};
        }}
        
        /* Main content padding */
        .main .block-container {{
            padding: 20px 30px;
            max-width: 1400px;
        }}
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {{
            background-color: {COLORS["purple_darker"]};
            border-right: 2px solid {COLORS["purple_muted"]};
        }}
        
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {{
            color: {COLORS["sage_light"]};
        }}
        
        /* Text area styling */
        .stTextArea textarea {{
            font-size: 16px;
            background-color: {COLORS["purple_dark"]} !important;
            color: {COLORS["sage_light"]} !important;
            border: 2px solid {COLORS["purple_muted"]};
            border-radius: 8px;
            -webkit-text-fill-color: {COLORS["sage_light"]} !important;
            opacity: 1 !important;
        }}
        
        .stTextArea textarea:focus {{
            border-color: {COLORS["sage_light"]};
            box-shadow: none;
        }}
        
        .stTextArea textarea::placeholder {{
            color: {COLORS["gray_medium"]} !important;
            -webkit-text-fill-color: {COLORS["gray_medium"]} !important;
        }}
        
        /* Disabled text area - ensure text is visible */
        .stTextArea textarea:disabled {{
            background-color: {COLORS["purple_dark"]} !important;
            color: {COLORS["sage_light"]} !important;
            -webkit-text-fill-color: {COLORS["sage_light"]} !important;
            opacity: 1 !important;
        }}
        
        /* Text area labels */
        .stTextArea label {{
            color: {COLORS["sage_light"]} !important;
            font-size: 14px !important;
            font-weight: 600 !important;
        }}
        
        /* Fix label color for all text inputs */
        .stTextArea label p {{
            color: {COLORS["sage_light"]} !important;
        }}
        
        /* Sidebar buttons */
        [data-testid="stSidebar"] .stButton button {{
            background-color: {COLORS["purple_darker"]};
            color: {COLORS["sage_light"]};
            border: 1px solid {COLORS["purple_muted"]};
            font-size: 12px;
            padding: 8px 12px;
            text-align: left;
            width: 100%;
            margin-bottom: 5px;
            border-radius: 6px;
        }}
        
        [data-testid="stSidebar"] .stButton button:hover {{
            background-color: {COLORS["purple_muted"]};
            border-color: {COLORS["sage_light"]};
        }}
        
        /* Hide default Streamlit elements */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden;}}
        
        /* Card styling */
        .card {{
            background: {COLORS["purple_dark"]};
            border: 2px solid {COLORS["purple_muted"]};
            border-radius: 8px;
            padding: 20px;
            height: 100%;
        }}
        
        .card-title {{
            color: {COLORS["sage_light"]};
            font-size: 14px;
            font-weight: 600;
            margin-bottom: 15px;
            letter-spacing: 0.5px;
        }}
        
        .card-content {{
            color: {COLORS["sage_light"]};
            font-size: 16px;
            line-height: 1.9;
            font-family: 'Georgia', 'Times New Roman', serif;
        }}
        
        /* Dialog styling - speaker names */
        .card-content strong {{
            color: {COLORS["sage_light"]};
            font-weight: 700;
        }}
        
        /* Dialog paragraphs */
        .card-content div {{
            margin-bottom: 10px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # Render sidebar
    render_sidebar()
    
    # Get example text if clicked
    if "example_text" in st.session_state:
        default_text = st.session_state.example_text
        del st.session_state.example_text
    else:
        default_text = ""
    
    # ═══════════════════════════════════════════════════════════════
    # MAIN CONTENT - GRID LAYOUT
    # ═══════════════════════════════════════════════════════════════
    
    # Create two main columns: Left (input + german) | Right (translations)
    col_left, col_right = st.columns([1, 1], gap="medium")
    
    with col_left:
        # ─────────────────────────────────────────
        # ENTER GERMAN TEXT (Simple label + text area)
        # ─────────────────────────────────────────
        german_text = st.text_area(
            label="✍️ Enter German Text (supports dialogs with multiple speakers)",
            value=default_text,
            placeholder="Paste your German dialog here...\n\nExample:\nMichael: Guten Tag, wie geht es Ihnen?\nHr. Schmidt: Mir geht es gut, danke!",
            height=200,
        )
        
        # ─────────────────────────────────────────
        # GERMAN WITH GENDER COLORS
        # ─────────────────────────────────────────
        if german_text:
            colorized_html = colorize_text_html(german_text)
            st.markdown(
                f'''
                <div class="card" style="margin-top: 20px; max-height: 500px; overflow-y: auto;">
                    <div class="card-title">🇩🇪 German with Gender Colors</div>
                    <div class="card-content">{colorized_html}</div>
                </div>
                ''',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'''
                <div class="card" style="min-height: 200px; margin-top: 20px;">
                    <div class="card-title">🇩🇪 German with Gender Colors</div>
                    <div style="color: {COLORS["gray_medium"]}; font-size: 14px;">
                        Enter text above to see gender-colored output
                    </div>
                </div>
                ''',
                unsafe_allow_html=True
            )
    
    with col_right:
        # ─────────────────────────────────────────
        # ENGLISH TRANSLATION (Text area - expandable)
        # ─────────────────────────────────────────
        if german_text:
            english_text = translate_to_english(german_text)
        else:
            english_text = ""
        
        st.markdown(f'<p style="color: {COLORS["sage_light"]}; font-size: 14px; font-weight: 600; margin-bottom: 5px;">🇬🇧 English Translation</p>', unsafe_allow_html=True)
        st.text_area(
            label="English Translation",
            value=english_text,
            placeholder="Translation will appear here...",
            height=200,
            label_visibility="collapsed",
            key=f"english_{hash(german_text)}"
        )
        
        # ─────────────────────────────────────────
        # SPANISH TRANSLATION (Text area - expandable)
        # ─────────────────────────────────────────
        if german_text:
            spanish_text = translate_to_spanish(german_text)
        else:
            spanish_text = ""
        
        st.markdown(f'<p style="color: {COLORS["sage_light"]}; font-size: 14px; font-weight: 600; margin-bottom: 5px;">🇪🇸 Spanish Translation</p>', unsafe_allow_html=True)
        st.text_area(
            label="Spanish Translation",
            value=spanish_text,
            placeholder="Translation will appear here...",
            height=200,
            label_visibility="collapsed",
            key=f"spanish_{hash(german_text)}"
        )


if __name__ == "__main__":
    main()
