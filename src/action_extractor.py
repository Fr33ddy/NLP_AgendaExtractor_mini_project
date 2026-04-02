import re
import spacy

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

def _safe_sent_tokenize(text):
  
    try:
        doc = nlp(text)
        return [sent.text.strip() for sent in doc.sents]
    except Exception:
        # Fallback regex split
        return [s.strip() for s in re.split(r'(?<=[.!?])\s+', text) if s.strip()]

def extract_meeting_data(text):
   
    #Extracts motions, seconds, decisions, and action items from meeting text.
    
    sentences = _safe_sent_tokenize(text)

    motions = []
    seconds = []
    decisions = []
    actions = []

    seen_seconds = set()

    for sent in sentences:
        s = sent.lower()
        doc = nlp(sent)

        # SECONDS
        if "seconded the motion" in s or "formally seconded the motion" in s:
            # Extract person's name 
            names = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
            for name in names:
                if name not in seen_seconds:
                    seconds.append(sent.strip())
                    seen_seconds.add(name)
            continue

        # DECISIONS
        if re.search(r"motion passed|passed unanimously|proposal was approved|motion was approved|approved by", s):
            decisions.append(sent.strip())
            continue

        # MOTIONS
        if re.search(r"moved that|moved to|suggested that|proposed that", s):
            motions.append(sent.strip())
            continue

        # ACTION ITEMS using verbs and modal auxiliaries
        action_verbs = {"prepare", "finalize", "begin"}
        modals = {"will", "shall", "must"}

        for token in doc:
            if token.lemma_.lower() in action_verbs or token.text.lower() in modals:
                if "approved" not in s and "passed" not in s:
                    actions.append(sent.strip())
                    break  

    return motions, seconds, decisions, actions