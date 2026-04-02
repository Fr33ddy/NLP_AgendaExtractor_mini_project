import re

def clean_text(text):
    
    
    # Remove page numbers
    text = re.sub(r'Page \d+ of \d+', '', text, flags=re.IGNORECASE)

    # Replace multiple newlines with a single newline
    text = re.sub(r'\n+', '\n', text)

    # Replace multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text)

    # Strip leading/trailing spaces
    text = text.strip()

    return text