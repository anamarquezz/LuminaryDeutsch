# German Language Learning App

A Streamlit-based application for learning German, featuring translation and grammatical gender visualization.

## Features

### Translation
- Translate German text to **English** or **Spanish**
- Preserves speaker names in dialog format (e.g., `Michael: Guten Tag` → `Michael: Good day`)
- Powered by Google Translate API

### Gender Color-Coding
Highlights German articles and pronouns by grammatical gender:

| Gender | Color | Examples |
|--------|-------|----------|
| Masculine | 🔵 Blue | der, ein, er, ihn, ihm |
| Feminine | 🩷 Pink | die, eine, sie, ihr |
| Neuter | 🟢 Green | das, ein, es |
| Plural | 🟠 Orange | die, wir, ihr, uns |

## Requirements

- Python 3.8+
- Internet connection (for Google Translate API)

## Installation

1. **Clone or download** this repository

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Download the German spaCy model**:
   ```bash
   python -m spacy download de_core_news_sm
   ```

## Running the App

Start the Streamlit server:

```bash
streamlit run main.py
```

The app will open in your default browser at `http://localhost:8501`

## Project Structure

```
Language_app/
├── main.py                 # Entry point
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── src/
    ├── __init__.py        # Package exports
    ├── ui.py              # Streamlit UI components
    ├── translator.py      # Translation logic
    └── gender_detector.py # Gender detection & color-coding
```

## Dependencies

| Package | Purpose |
|---------|---------|
| `streamlit` | Web UI framework |
| `deep-translator` | Google Translate API wrapper |
| `spacy` | NLP for gender detection |

## License

MIT

