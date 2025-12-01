"""
Translation module for German to English and Spanish translations.
Uses deep-translator library with Google Translate API.
Preserves character names in dialogs without translating them.
"""

import re
from deep_translator import GoogleTranslator


def extract_dialog_parts(text: str) -> list:
    """
    Extract dialog lines, separating speaker names from their speech.
    
    Args:
        text: The text to parse
        
    Returns:
        List of tuples: (speaker_name or None, content, is_empty_line)
    """
    lines = text.split('\n')
    parts = []
    
    for line in lines:
        if not line.strip():
            parts.append((None, '', True))
            continue
        
        # Check if line starts with a speaker name (e.g., "Michael:", "Hr. Schmidt:")
        speaker_match = re.match(r'^([A-Za-zÄÖÜäöüß\.\s]+):\s*', line)
        
        if speaker_match:
            speaker = speaker_match.group(1).strip()
            content = line[speaker_match.end():]
            parts.append((speaker, content, False))
        else:
            parts.append((None, line, False))
    
    return parts


def translate_preserving_names(german_text: str, target_lang: str) -> str:
    """
    Translate German text while preserving character names.
    
    Args:
        german_text: The German text to translate
        target_lang: Target language code ('en' or 'es')
        
    Returns:
        Translation with original character names preserved
    """
    if not german_text or not german_text.strip():
        return ""
    
    try:
        translator = GoogleTranslator(source='de', target=target_lang)
        parts = extract_dialog_parts(german_text)
        translated_lines = []
        
        for speaker, content, is_empty in parts:
            if is_empty:
                translated_lines.append('')
                continue
            
            if speaker:
                # Translate only the dialog content, keep speaker name
                if content.strip():
                    translated_content = translator.translate(content)
                    translated_lines.append(f"{speaker}: {translated_content}")
                else:
                    translated_lines.append(f"{speaker}:")
            else:
                # No speaker, translate the whole line
                translated_lines.append(translator.translate(content))
        
        return '\n'.join(translated_lines)
    except Exception as e:
        return f"Translation error: {str(e)}"


def translate_to_english(german_text: str) -> str:
    """
    Translate German text to English, preserving character names.
    
    Args:
        german_text: The German text to translate
        
    Returns:
        English translation or error message
    """
    return translate_preserving_names(german_text, 'en')


def translate_to_spanish(german_text: str) -> str:
    """
    Translate German text to Spanish, preserving character names.
    
    Args:
        german_text: The German text to translate
        
    Returns:
        Spanish translation or error message
    """
    return translate_preserving_names(german_text, 'es')


def translate_german(german_text: str, target_language: str) -> str:
    """
    Translate German text to specified target language.
    
    Args:
        german_text: The German text to translate
        target_language: Target language code ('en' or 'es')
        
    Returns:
        Translation or error message
    """
    if target_language == 'en':
        return translate_to_english(german_text)
    elif target_language == 'es':
        return translate_to_spanish(german_text)
    else:
        return f"Unsupported language: {target_language}"

