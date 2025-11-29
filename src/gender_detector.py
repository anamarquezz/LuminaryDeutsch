"""
Gender detection module for German text.
Uses spaCy to analyze articles and nouns, detecting grammatical gender.
"""

import spacy
from typing import List, Dict, Tuple

# Load German language model
nlp = spacy.load("de_core_news_sm")

# Color mapping for genders
GENDER_COLORS = {
    "masculine": "#3B82F6",   # Blue
    "feminine": "#EC4899",    # Pink
    "neuter": "#22C55E",      # Green
    "plural": "#F97316",      # Orange
    "default": "#1F2937",     # Dark gray (for non-gendered words)
}

# German definite articles
DEFINITE_ARTICLES = {"der", "die", "das"}

# German indefinite articles
INDEFINITE_ARTICLES = {"ein", "eine", "einen", "einem", "einer", "eines"}


def get_gender_from_article(token) -> str:
    """
    Determine the gender of an article based on its morphological features.
    
    Args:
        token: spaCy token object
        
    Returns:
        Gender string: 'masculine', 'feminine', 'neuter', 'plural', or 'default'
    """
    text_lower = token.text.lower()
    morph = token.morph
    
    # Get morphological features
    gender = morph.get("Gender")
    number = morph.get("Number")
    
    # Check for plural first (die + plural)
    if "Plur" in number:
        return "plural"
    
    # Check definite articles
    if text_lower == "der":
        # "der" can be masculine nominative or feminine dative/genitive
        if "Masc" in gender:
            return "masculine"
        elif "Fem" in gender:
            return "feminine"
        return "masculine"  # Default for "der"
    
    elif text_lower == "die":
        # "die" is feminine singular or plural
        if "Plur" in number:
            return "plural"
        return "feminine"
    
    elif text_lower == "das":
        return "neuter"
    
    # Check indefinite articles
    elif text_lower in {"ein", "einen", "einem", "eines"}:
        if "Neut" in gender:
            return "neuter"
        return "masculine"
    
    elif text_lower == "eine":
        return "feminine"
    
    elif text_lower == "einer":
        if "Fem" in gender:
            return "feminine"
        return "masculine"
    
    return "default"


def analyze_text(german_text: str) -> List[Dict]:
    """
    Analyze German text and return word-by-word gender information.
    
    Args:
        german_text: The German text to analyze
        
    Returns:
        List of dictionaries with word info:
        [{'word': str, 'gender': str, 'color': str, 'is_article': bool}, ...]
    """
    if not german_text or not german_text.strip():
        return []
    
    doc = nlp(german_text)
    result = []
    
    # Track the gender of articles to apply to following nouns
    current_gender = None
    
    for token in doc:
        word_info = {
            "word": token.text,
            "gender": "default",
            "color": GENDER_COLORS["default"],
            "is_article": False,
            "is_noun": False,
        }
        
        text_lower = token.text.lower()
        
        # Check if it's an article
        if text_lower in DEFINITE_ARTICLES or text_lower in INDEFINITE_ARTICLES:
            gender = get_gender_from_article(token)
            word_info["gender"] = gender
            word_info["color"] = GENDER_COLORS.get(gender, GENDER_COLORS["default"])
            word_info["is_article"] = True
            current_gender = gender
        
        # Check if it's a noun (apply the article's gender)
        elif token.pos_ == "NOUN":
            word_info["is_noun"] = True
            if current_gender:
                word_info["gender"] = current_gender
                word_info["color"] = GENDER_COLORS.get(current_gender, GENDER_COLORS["default"])
            else:
                # Try to get gender from noun's morphology
                morph_gender = token.morph.get("Gender")
                morph_number = token.morph.get("Number")
                
                if "Plur" in morph_number:
                    word_info["gender"] = "plural"
                    word_info["color"] = GENDER_COLORS["plural"]
                elif "Masc" in morph_gender:
                    word_info["gender"] = "masculine"
                    word_info["color"] = GENDER_COLORS["masculine"]
                elif "Fem" in morph_gender:
                    word_info["gender"] = "feminine"
                    word_info["color"] = GENDER_COLORS["feminine"]
                elif "Neut" in morph_gender:
                    word_info["gender"] = "neuter"
                    word_info["color"] = GENDER_COLORS["neuter"]
        
        # Reset gender tracking after noun or punctuation
        if token.pos_ in {"NOUN", "PUNCT"} or token.text in {",", ".", "!", "?", ";", ":"}:
            current_gender = None
        
        result.append(word_info)
    
    return result


def colorize_text_html(german_text: str) -> str:
    """
    Return German text with HTML color spans for articles and nouns.
    
    Args:
        german_text: The German text to colorize
        
    Returns:
        HTML string with colored spans
    """
    if not german_text or not german_text.strip():
        return ""
    
    analyzed = analyze_text(german_text)
    html_parts = []
    
    for i, word_info in enumerate(analyzed):
        word = word_info["word"]
        color = word_info["color"]
        is_colored = word_info["is_article"] or word_info["is_noun"]
        
        if is_colored:
            # Bold for articles, regular weight for nouns
            weight = "700" if word_info["is_article"] else "600"
            html_parts.append(
                f'<span style="color: {color}; font-weight: {weight};">{word}</span>'
            )
        else:
            html_parts.append(word)
        
        # Add space after word (except before punctuation)
        if i < len(analyzed) - 1:
            next_word = analyzed[i + 1]["word"]
            if next_word not in {",", ".", "!", "?", ";", ":", "'", '"'}:
                html_parts.append(" ")
    
    return "".join(html_parts)


def get_color_legend() -> Dict[str, str]:
    """
    Return the color legend for the UI.
    
    Returns:
        Dictionary mapping gender names to their colors
    """
    return {
        "Masculine (der)": GENDER_COLORS["masculine"],
        "Feminine (die)": GENDER_COLORS["feminine"],
        "Neuter (das)": GENDER_COLORS["neuter"],
        "Plural (die)": GENDER_COLORS["plural"],
    }

