"""
Translation module for German to English and Spanish translations.
Uses deep-translator library with Google Translate API.
"""

from deep_translator import GoogleTranslator


def translate_to_english(german_text: str) -> str:
    """
    Translate German text to English.
    
    Args:
        german_text: The German text to translate
        
    Returns:
        English translation or error message
    """
    if not german_text or not german_text.strip():
        return ""
    
    try:
        translator = GoogleTranslator(source='de', target='en')
        translation = translator.translate(german_text)
        return translation
    except Exception as e:
        return f"Translation error: {str(e)}"


def translate_to_spanish(german_text: str) -> str:
    """
    Translate German text to Spanish.
    
    Args:
        german_text: The German text to translate
        
    Returns:
        Spanish translation or error message
    """
    if not german_text or not german_text.strip():
        return ""
    
    try:
        translator = GoogleTranslator(source='de', target='es')
        translation = translator.translate(german_text)
        return translation
    except Exception as e:
        return f"Translation error: {str(e)}"


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

