from src.pdf_processor import extract_text_from_pdf
from src.action_extractor import extract_actions

text = extract_text_from_pdf("data/sample_meeting.pdf")

actions = extract_actions(text)

print("Extracted Actions:")
for action in actions:
    print("-", action)