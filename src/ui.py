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


# Speaker color palette for dialog names
SPEAKER_COLORS = [
    "#F472B6",  # Pink
    "#60A5FA",  # Blue
    "#34D399",  # Emerald
    "#FBBF24",  # Amber
    "#A78BFA",  # Violet
    "#FB923C",  # Orange
    "#2DD4BF",  # Teal
    "#F87171",  # Red
]


def extract_speakers(text: str) -> dict:
    """
    Extract all speaker names from text and assign consistent colors.
    
    Args:
        text: The text to parse for speaker names
        
    Returns:
        Dictionary mapping speaker names to their assigned colors
    """
    import re
    
    if not text or not text.strip():
        return {}
    
    speaker_color_map = {}
    color_index = 0
    
    for line in text.split('\n'):
        speaker_match = re.match(r'^([A-Za-zÄÖÜäöüß\.\s]+):\s*', line)
        if speaker_match:
            speaker = speaker_match.group(1).strip()
            if speaker not in speaker_color_map:
                speaker_color_map[speaker] = SPEAKER_COLORS[color_index % len(SPEAKER_COLORS)]
                color_index += 1
    
    return speaker_color_map


def format_translation_html(text: str, speaker_color_map: dict = None) -> str:
    """
    Format translation text with proper HTML structure.
    Preserves line breaks and formats dialog with speaker names in different colors.
    
    Args:
        text: The translation text to format
        speaker_color_map: Optional pre-defined speaker-to-color mapping for consistency
        
    Returns:
        HTML string with proper formatting
    """
    import re
    
    if not text or not text.strip():
        return ""
    
    lines = text.split('\n')
    html_lines = []
    
    # Use provided map or create new one
    if speaker_color_map is None:
        speaker_color_map = {}
        color_index = 0
    
    for line in lines:
        if not line.strip():
            html_lines.append('<br>')
            continue
        
        # Check if line starts with a speaker name (e.g., "Michael:", "Hr. Schmidt:")
        speaker_match = re.match(r'^([A-Za-zÄÖÜäöüß\.\s]+):\s*', line)
        
        if speaker_match:
            speaker = speaker_match.group(1).strip()
            rest_of_line = line[speaker_match.end():]
            
            # Get color from map or assign default
            speaker_color = speaker_color_map.get(speaker, COLORS["sage_light"])
            
            html_lines.append(
                f'<div style="margin-bottom: 12px;"><strong style="color: {speaker_color};">{speaker}:</strong> {rest_of_line}</div>'
            )
        else:
            html_lines.append(f'<div style="margin-bottom: 12px;">{line}</div>')
    
    return "".join(html_lines)


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
    
    # ─────────────────────────────────────────
    # ROW 1: INPUT & GERMAN COLORS (Input | Gender Colors)
    # ─────────────────────────────────────────
    col_input, col_german = st.columns([1, 1], gap="medium")
    
    with col_input:
        german_text = st.text_area(
            label="✍️ Enter German Text (supports dialogs with multiple speakers)",
            value=default_text,
            placeholder="Paste your German dialog here...\n\nExample:\nMichael: Guten Tag, wie geht es Ihnen?\nHr. Schmidt: Mir geht es gut, danke!",
            height=120,
        )
        
        # Extract speaker colors from German text for consistent coloring across all panels
        speaker_color_map = extract_speakers(german_text) if german_text else {}
        
        # Show formatted preview with colored speaker names below input
        st.markdown(
            f'<p style="color: {COLORS["sage_light"]}; font-size: 14px; font-weight: 600; margin-top: 10px; margin-bottom: 5px;">📝 Input Preview</p>',
            unsafe_allow_html=True
        )
        if german_text:
            input_preview_html = format_translation_html(german_text, speaker_color_map)
            st.markdown(
                f'''
                <div class="card" style="height: 250px; overflow-y: auto;">
                    <div class="card-content">{input_preview_html}</div>
                </div>
                ''',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'''
                <div class="card" style="height: 250px;">
                    <div style="color: {COLORS["gray_medium"]}; font-size: 14px;">
                        Your formatted text will appear here...
                    </div>
                </div>
                ''',
                unsafe_allow_html=True
            )
    
    with col_german:
        st.markdown(
            f'<p style="color: {COLORS["sage_light"]}; font-size: 14px; font-weight: 600; margin-bottom: 5px;">🇩🇪 German with Gender Colors</p>',
            unsafe_allow_html=True
        )
        if german_text:
            colorized_html = colorize_text_html(german_text, speaker_color_map)
            st.markdown(
                f'''
                <div class="card" style="height: 400px; overflow-y: auto;">
                    <div class="card-content">{colorized_html}</div>
                </div>
                ''',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'''
                <div class="card" style="height: 400px;">
                    <div style="color: {COLORS["gray_medium"]}; font-size: 14px;">
                        Enter text to the left to see gender-colored output
                    </div>
                </div>
                ''',
                unsafe_allow_html=True
            )
    
    # ─────────────────────────────────────────
    # ROW 2: TRANSLATIONS (English | Spanish)
    # ─────────────────────────────────────────
    
    col_eng, col_esp = st.columns([1, 1], gap="medium")
    
    with col_eng:
        st.markdown(
            f'<p style="color: {COLORS["sage_light"]}; font-size: 14px; font-weight: 600; margin-bottom: 5px;">🇬🇧 English Translation</p>',
            unsafe_allow_html=True
        )
        if german_text:
            english_text = translate_to_english(german_text)
            english_html = format_translation_html(english_text, speaker_color_map)
            st.markdown(
                f'''
                <div class="card" style="height: 400px; overflow-y: auto;">
                    <div class="card-content">{english_html}</div>
                </div>
                ''',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'''
                <div class="card" style="height: 400px;">
                    <div style="color: {COLORS["gray_medium"]}; font-size: 14px;">
                        Translation will appear here...
                    </div>
                </div>
                ''',
                unsafe_allow_html=True
            )
    
    with col_esp:
        st.markdown(
            f'<p style="color: {COLORS["sage_light"]}; font-size: 14px; font-weight: 600; margin-bottom: 5px;">🇪🇸 Spanish Translation</p>',
            unsafe_allow_html=True
        )
        if german_text:
            spanish_text = translate_to_spanish(german_text)
            spanish_html = format_translation_html(spanish_text, speaker_color_map)
            st.markdown(
                f'''
                <div class="card" style="height: 400px; overflow-y: auto;">
                    <div class="card-content">{spanish_html}</div>
                </div>
                ''',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'''
                <div class="card" style="height: 400px;">
                    <div style="color: {COLORS["gray_medium"]}; font-size: 14px;">
                        Translation will appear here...
                    </div>
                </div>
                ''',
                unsafe_allow_html=True
            )


if __name__ == "__main__":
    main()
