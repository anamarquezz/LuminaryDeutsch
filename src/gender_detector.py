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
    "default": "#eecc25",     # Dark gray (for non-gendered words)
}

# German definite articles
DEFINITE_ARTICLES = {"der", "die", "das"}

# German indefinite articles
INDEFINITE_ARTICLES = {"ein", "eine", "einen", "einem", "einer", "eines"}

# German negative articles (kein)
NEGATIVE_ARTICLES = {"kein", "keine", "keinen", "keinem", "keiner", "keines"}

# German possessive articles
POSSESSIVE_ARTICLES = {
    "mein", "meine", "meinen", "meinem", "meiner", "meines",
    "dein", "deine", "deinen", "deinem", "deiner", "deines",
    "sein", "seine", "seinen", "seinem", "seiner", "seines",
    "ihr", "ihre", "ihren", "ihrem", "ihrer", "ihres",
    "unser", "unsere", "unseren", "unserem", "unserer", "unseres",
    "euer", "eure", "euren", "eurem", "eurer", "eures",
}

# German personal pronouns with their gender/number
PERSONAL_PRONOUNS = {
    # Nominative
    "ich": "default",      # 1st person singular
    "du": "default",       # 2nd person singular
    "er": "masculine",     # 3rd person singular masculine
    "sie": "feminine",     # 3rd person singular feminine (or plural/formal)
    "es": "neuter",        # 3rd person singular neuter
    "wir": "plural",       # 1st person plural
    "ihr": "plural",       # 2nd person plural
    # Accusative
    "mich": "default",
    "dich": "default",
    "ihn": "masculine",
    "uns": "plural",
    "euch": "plural",
    # Dative
    "mir": "default",
    "dir": "default",
    "ihm": "masculine",
}


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
        
        # Check if it's a definite or indefinite article
        if text_lower in DEFINITE_ARTICLES or text_lower in INDEFINITE_ARTICLES:
            gender = get_gender_from_article(token)
            word_info["gender"] = gender
            word_info["color"] = GENDER_COLORS.get(gender, GENDER_COLORS["default"])
            word_info["is_article"] = True
            current_gender = gender
        
        # Check if it's a negative article (kein)
        elif text_lower in NEGATIVE_ARTICLES:
            gender = get_gender_from_article(token)
            word_info["gender"] = gender
            word_info["color"] = GENDER_COLORS.get(gender, GENDER_COLORS["default"])
            word_info["is_article"] = True
            current_gender = gender
        
        # Check if it's a possessive article (mein, dein, sein, etc.)
        elif text_lower in POSSESSIVE_ARTICLES:
            gender = get_gender_from_article(token)
            word_info["gender"] = gender
            word_info["color"] = GENDER_COLORS.get(gender, GENDER_COLORS["default"])
            word_info["is_article"] = True
            current_gender = gender
        
        # Check if it's a personal pronoun
        elif text_lower in PERSONAL_PRONOUNS:
            gender = PERSONAL_PRONOUNS[text_lower]
            word_info["gender"] = gender
            word_info["color"] = GENDER_COLORS.get(gender, GENDER_COLORS["default"])
            word_info["is_article"] = True  # Treat as article for coloring
        
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


def colorize_line(line: str) -> str:
    """
    Colorize a single line of German text.
    
    Args:
        line: A single line of German text
        
    Returns:
        HTML string with colored spans
    """
    if not line or not line.strip():
        return ""
    
    analyzed = analyze_text(line)
    html_parts = []
    
    for i, word_info in enumerate(analyzed):
        word = word_info["word"]
        color = word_info["color"]
        
        # Only color articles, not nouns
        if word_info["is_article"]:
            html_parts.append(
                f'<span style="color: {color}; font-weight: 700;">{word}</span>'
            )
        else:
            html_parts.append(word)
        
        # Add space after word (except before punctuation)
        if i < len(analyzed) - 1:
            next_word = analyzed[i + 1]["word"]
            if next_word not in {",", ".", "!", "?", ";", ":", "'", '"'}:
                html_parts.append(" ")
    
    return "".join(html_parts)


def colorize_text_html(german_text: str, speaker_color_map: Dict[str, str] = None) -> str:
    """
    Return German text with HTML color spans for articles and nouns.
    Preserves line breaks and formats dialog with speaker names in colors.
    
    Args:
        german_text: The German text to colorize
        speaker_color_map: Optional mapping of speaker names to colors
        
    Returns:
        HTML string with colored spans and proper formatting
    """
    if not german_text or not german_text.strip():
        return ""
    
    # Split by line breaks to preserve dialog structure
    lines = german_text.split('\n')
    html_lines = []
    
    import re
    
    for line in lines:
        if not line.strip():
            html_lines.append('<br>')
            continue
        
        # Check if line starts with a speaker name (e.g., "Michael:", "Hr. Scheibe:")
        # Pattern: text followed by colon at the start
        speaker_match = re.match(r'^([A-Za-zÄÖÜäöüß\.\s]+):\s*', line)
        
        if speaker_match:
            speaker = speaker_match.group(1).strip()
            rest_of_line = line[speaker_match.end():]
            # Style the speaker name in bold with color
            colorized_rest = colorize_line(rest_of_line)
            
            # Get speaker color from map or use default
            speaker_color = speaker_color_map.get(speaker, "#BFC3BA") if speaker_color_map else "#BFC3BA"
            
            html_lines.append(
                f'<div style="margin-bottom: 12px;"><strong style="color: {speaker_color};">{speaker}:</strong> {colorized_rest}</div>'
            )
        else:
            # Regular line without speaker
            colorized = colorize_line(line)
            html_lines.append(f'<div style="margin-bottom: 12px;">{colorized}</div>')
    
    return "".join(html_lines)


def get_color_legend() -> Dict[str, str]:
    """
    Return the color legend for the UI.
    
    Returns:
        Dictionary mapping gender names to their colors
    """
    return {
        "Masculine (der, ein, er, ihn...)": GENDER_COLORS["masculine"],
        "Feminine (die, eine, sie...)": GENDER_COLORS["feminine"],
        "Neuter (das, ein, es...)": GENDER_COLORS["neuter"],
        "Plural (die, wir, ihr...)": GENDER_COLORS["plural"],
    }

