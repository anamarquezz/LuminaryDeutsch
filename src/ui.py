"""
Streamlit UI for German Translator with Gender-Colored Articles.
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
    "purple_darker": "#3F3244",   # Darkest purple - main background
}


def render_color_legend():
    """Render the color legend in the sidebar."""
    st.sidebar.markdown(
        f'<h2 style="color: {COLORS["sage_light"]};">🎨 Color Legend</h2>',
        unsafe_allow_html=True
    )
    
    legend = get_color_legend()
    for label, color in legend.items():
        st.sidebar.markdown(
            f'<div style="padding: 5px 0;"><span style="color: {color}; font-size: 20px; font-weight: bold;">●</span> <span style="color: {COLORS["sage_light"]};">{label}</span></div>',
            unsafe_allow_html=True
        )


def render_header():
    """Render the app header."""
    st.markdown(
        f"""
        <div style="text-align: center; padding: 30px 0; margin-bottom: 20px;">
            <h1 style="color: {COLORS["sage_light"]}; margin-bottom: 10px; font-size: 2.8rem; font-weight: 700;">
                🇩🇪 German Translator
            </h1>
            <p style="color: {COLORS["gray_medium"]}; font-size: 1.2rem;">
                Translate German to English & Spanish with gender-colored articles
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_colorized_german(german_text: str):
    """Render the German text with colored articles and nouns."""
    if not german_text:
        return
    
    st.markdown(
        f'<h3 style="color: {COLORS["sage_light"]};">🇩🇪 German with Gender Colors</h3>',
        unsafe_allow_html=True
    )
    
    colorized_html = colorize_text_html(german_text)
    
    st.markdown(
        f"""
        <div style="
            background-color: {COLORS["purple_dark"]};
            border: 2px solid {COLORS["purple_muted"]};
            border-radius: 12px;
            padding: 25px;
            font-size: 22px;
            line-height: 2;
            color: {COLORS["sage_light"]};
        ">
            {colorized_html}
        </div>
        """,
        unsafe_allow_html=True
    )


def render_english_translation(german_text: str):
    """Render the English translation in a styled box."""
    if not german_text:
        return
    
    st.markdown(
        f'<h3 style="color: {COLORS["sage_light"]};">🇬🇧 English Translation</h3>',
        unsafe_allow_html=True
    )
    
    english_text = translate_to_english(german_text)
    
    st.markdown(
        f"""
        <div style="
            background-color: {COLORS["purple_dark"]};
            border: 2px solid {COLORS["purple_muted"]};
            border-radius: 12px;
            padding: 25px;
            font-size: 22px;
            line-height: 2;
            color: {COLORS["sage_light"]};
        ">
            {english_text}
        </div>
        """,
        unsafe_allow_html=True
    )


def render_spanish_translation(german_text: str):
    """Render the Spanish translation in a styled box."""
    if not german_text:
        return
    
    st.markdown(
        f'<h3 style="color: {COLORS["sage_light"]};">🇪🇸 Spanish Translation</h3>',
        unsafe_allow_html=True
    )
    
    spanish_text = translate_to_spanish(german_text)
    
    st.markdown(
        f"""
        <div style="
            background-color: {COLORS["purple_dark"]};
            border: 2px solid {COLORS["purple_muted"]};
            border-radius: 12px;
            padding: 25px;
            font-size: 22px;
            line-height: 2;
            color: {COLORS["sage_light"]};
        ">
            {spanish_text}
        </div>
        """,
        unsafe_allow_html=True
    )


def render_example_sentences():
    """Render example sentences in the sidebar."""
    st.sidebar.markdown(
        f'<hr style="border-color: {COLORS["purple_muted"]}; margin: 20px 0;">',
        unsafe_allow_html=True
    )
    st.sidebar.markdown(
        f'<h2 style="color: {COLORS["sage_light"]};">📝 Examples</h2>',
        unsafe_allow_html=True
    )
    
    examples = [
        "Der Hund spielt mit der Katze.",
        "Die Frau liest das Buch.",
        "Das Kind isst einen Apfel.",
        "Die Kinder spielen im Garten.",
        "Der Mann kauft eine Blume für die Frau.",
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
    
    # Custom CSS with new color palette
    st.markdown(
        f"""
        <style>
        /* Main app background */
        .stApp {{
            background-color: {COLORS["purple_darker"]};
        }}
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {{
            background-color: {COLORS["purple_dark"]};
        }}
        
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {{
            color: {COLORS["sage_light"]};
        }}
        
        /* Text area styling */
        .stTextArea textarea {{
            font-size: 18px;
            background-color: {COLORS["purple_dark"]};
            color: {COLORS["sage_light"]};
            border: 2px solid {COLORS["purple_muted"]};
            border-radius: 12px;
        }}
        
        .stTextArea textarea::placeholder {{
            color: {COLORS["gray_medium"]};
        }}
        
        /* Button styling */
        .stButton button {{
            font-size: 16px;
            padding: 12px 24px;
            background-color: {COLORS["purple_muted"]};
            color: {COLORS["sage_light"]};
            border: none;
            border-radius: 8px;
            transition: all 0.3s ease;
        }}
        
        .stButton button:hover {{
            background-color: {COLORS["sage_light"]};
            color: {COLORS["purple_darker"]};
        }}
        
        /* Sidebar buttons */
        [data-testid="stSidebar"] .stButton button {{
            background-color: {COLORS["purple_darker"]};
            color: {COLORS["sage_light"]};
            border: 1px solid {COLORS["purple_muted"]};
            font-size: 14px;
            text-align: left;
        }}
        
        [data-testid="stSidebar"] .stButton button:hover {{
            background-color: {COLORS["purple_muted"]};
            border-color: {COLORS["sage_light"]};
        }}
        
        /* Divider/hr styling */
        hr {{
            border-color: {COLORS["purple_muted"]};
        }}
        
        /* Spinner */
        .stSpinner > div {{
            border-top-color: {COLORS["sage_light"]} !important;
        }}
        
        /* Hide default Streamlit elements */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # Render sidebar
    render_color_legend()
    render_example_sentences()
    
    # Render main content
    render_header()
    
    # Check if example was clicked
    if "example_text" in st.session_state:
        german_text = st.session_state.example_text
        del st.session_state.example_text
    else:
        german_text = ""
    
    # Input section
    st.markdown(
        f'<h3 style="color: {COLORS["sage_light"]};">✍️ Enter German Text</h3>',
        unsafe_allow_html=True
    )
    
    german_text = st.text_area(
        label="German text input",
        value=german_text,
        placeholder="Type or paste German text here... (e.g., Der Hund spielt mit der Katze.)",
        height=120,
        label_visibility="collapsed"
    )
    
    if german_text:
        st.markdown(
            f'<hr style="border-color: {COLORS["purple_muted"]}; margin: 30px 0;">',
            unsafe_allow_html=True
        )
        
        # Colorized German
        render_colorized_german(german_text)
        
        st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)
        
        # English Translation
        render_english_translation(german_text)
        
        st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)
        
        # Spanish Translation
        render_spanish_translation(german_text)


if __name__ == "__main__":
    main()
