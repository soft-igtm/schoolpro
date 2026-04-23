"""
chatbot.py
----------
Core NLP engine for the rule-based school chatbot.
Uses NLTK for tokenization/stemming when available; pure-Python fallback
ensures the bot works even without NLTK data files.
"""

import re
import random

from intents import INTENTS, get_fallback_responses, get_response

# ── NLTK bootstrap (optional) ─────────────────────────────────────────────────
_USE_NLTK = False
_stemmer  = None
_stop_words = set()

try:
    import nltk
    from nltk.corpus import stopwords
    from nltk.stem   import PorterStemmer

    nltk.data.find("tokenizers/punkt_tab")
    nltk.data.find("corpora/stopwords")

    _stemmer    = PorterStemmer()
    _stop_words = set(stopwords.words("english"))
    _KEEP_WORDS = {"how","when","where","what","who","which","why"}
    _stop_words -= _KEEP_WORDS
    _USE_NLTK   = True
except Exception:
    _stop_words = {
        "a","an","the","is","it","in","on","at","to","for","of","and","or","but",
        "not","be","am","are","was","were","do","does","did","have","has","had",
        "will","would","can","could","should","may","might","me","my","you","your",
        "we","our","i","this","that","there","about","with","from","by","up","down",
        "out","so","if","as","just","than","then","very","also","some","any","all",
        "more","into","tell","give","show","please","need","want","get","let",
    }
    _KEEP_WORDS = {"how","when","where","what","who","which","why"}
    _stop_words -= _KEEP_WORDS


# ── Stemmer ───────────────────────────────────────────────────────────────────

_SUFFIX_RULES = [
    ("ations",""),("ation",""),("ments",""),("ment",""),
    ("nesses",""),("ness",""),("tions",""),("tion",""),
    ("ings",""),("ing",""),("ies","y"),("ied","y"),
    ("ers",""),("er",""),("ed",""),("ly",""),
    ("ful",""),("ous",""),("ies",""),("es",""),("s",""),
]

def _simple_stem(word):
    if len(word) <= 3:
        return word
    for suffix, replacement in _SUFFIX_RULES:
        if word.endswith(suffix) and len(word)-len(suffix)+len(replacement) >= 3:
            return word[:len(word)-len(suffix)] + replacement
    return word

def _stem(word):
    if _USE_NLTK and _stemmer:
        return _stemmer.stem(word)
    return _simple_stem(word)


# ── Preprocessing ─────────────────────────────────────────────────────────────

def preprocess(text):
    """Lowercase → strip punctuation → split → remove stopwords → stem."""
    text   = re.sub(r"[^a-z0-9\s]", " ", text.lower())
    tokens = text.split()
    tokens = [t for t in tokens if t not in _stop_words and len(t) >= 2]
    return [_stem(t) for t in tokens]

def _stem_pattern(phrase):
    return [_stem(w) for w in phrase.lower().split()]


# ── Per-pattern scoring ───────────────────────────────────────────────────────

def _score_pattern(raw_lower, token_set, joined_stems, pattern):
    """
    Score one pattern vs user input. Returns (score: float, hits: int).
    score — match strength 0.0–1.0
    hits  — number of tokens in the pattern that matched (for tie-breaking)
    """
    pat_lower = pattern.lower()
    pat_stems = _stem_pattern(pattern)
    n         = len(pat_stems)

    if n > 1:
        if pat_lower in raw_lower:                  return 1.00, n
        if " ".join(pat_stems) in joined_stems:     return 0.85, n
        if all(w in token_set for w in pat_stems):  return 0.65, n
        hits = sum(1 for w in pat_stems if w in token_set)
        if hits >= max(1, n // 2):                  return 0.25, hits
        return 0.0, 0
    else:
        single = pat_stems[0]
        if re.search(r'\b' + re.escape(pat_lower) + r'\b', raw_lower):
            return 1.00, 1
        if single in token_set:
            return 0.60, 1
        return 0.0, 0


# ── Intent scoring ────────────────────────────────────────────────────────────

def _score_intent(raw, tokens, intent):
    """
    Returns (score, total_token_hits) for an intent.
    score            — best single-pattern score + small multi-pattern bonus
    total_token_hits — sum of all matched token counts (used for tie-breaking)
    """
    raw_lower    = raw.lower()
    token_set    = set(tokens)
    joined_stems = " ".join(tokens)

    pattern_scores = [
        _score_pattern(raw_lower, token_set, joined_stems, p)
        for p in intent["patterns"]
    ]

    if not pattern_scores:
        return 0.0, 0

    best_score   = max(s for s, _ in pattern_scores)
    total_hits   = sum(h for _, h in pattern_scores)
    match_count  = sum(1 for s, _ in pattern_scores if s >= 0.25)
    bonus        = min(match_count * 0.04, 0.12)

    return min(best_score + bonus, 1.0), total_hits


# ── Classification ────────────────────────────────────────────────────────────

def classify_intent(user_input):
    """
    Return the best-matching intent name (str) or None.
    Tie-breaking: when scores are within 0.01, prefer the intent
    with the most total matched token hits (more specific match).
    """
    if not user_input or not user_input.strip():
        return None

    tokens      = preprocess(user_input)
    best_intent = None
    best_score  = 0.0
    best_hits   = 0
    THRESHOLD   = 0.30

    for intent in INTENTS:
        score, hits = _score_intent(user_input, tokens, intent)
        if score > best_score + 0.01:
            best_score  = score
            best_hits   = hits
            best_intent = intent["intent"]
        elif abs(score - best_score) <= 0.01 and hits > best_hits:
            # Same score — prefer the intent with more matched tokens (more specific)
            best_hits   = hits
            best_intent = intent["intent"]

    return best_intent if best_score >= THRESHOLD else None


# ── Public API ────────────────────────────────────────────────────────────────

def get_bot_response(user_input):
    """Called by Flask routes. Returns dict: response, intent, confidence."""
    intent_name = classify_intent(user_input)
    if intent_name:
        return {
            "response":   get_response(intent_name),
            "intent":     intent_name,
            "confidence": "matched",
        }
    return {
        "response":   random.choice(get_fallback_responses()),
        "intent":     "unknown",
        "confidence": "fallback",
    }
