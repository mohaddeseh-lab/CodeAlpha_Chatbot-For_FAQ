"""
preprocess.py
-------------
Text preprocessing for the FAQ chatbot: lowercasing, tokenization,
stopword removal, and lemmatization.

Primary path: NLTK (as required by the task).
Fallback path: if NLTK or its data files aren't available in the current
environment, a lightweight built-in tokenizer/stopword list is used instead,
so the rest of the pipeline keeps working. Install NLTK (see requirements.txt)
to get the full NLP pipeline.
"""

import re
import string

# ---------------------------------------------------------------------------
# Try to set up NLTK. If it's missing (or its data isn't downloaded yet),
# we download the data automatically; if that also fails (e.g. no internet),
# we transparently fall back to simple regex-based preprocessing.
# ---------------------------------------------------------------------------
_USE_NLTK = False
try:
    import nltk
    from nltk.tokenize import word_tokenize
    from nltk.corpus import stopwords
    from nltk.stem import WordNetLemmatizer

    def _ensure_nltk_data():
        packages = [
            ("tokenizers/punkt", "punkt"),
            ("tokenizers/punkt_tab", "punkt_tab"),
            ("corpora/stopwords", "stopwords"),
            ("corpora/wordnet", "wordnet"),
            ("corpora/omw-1.4", "omw-1.4"),
        ]
        for path, pkg in packages:
            try:
                nltk.data.find(path)
            except LookupError:
                nltk.download(pkg, quiet=True)

    _ensure_nltk_data()
    _STOPWORDS = set(stopwords.words("english"))
    _LEMMATIZER = WordNetLemmatizer()

    # Sanity check that punkt actually works end to end.
    word_tokenize("test sentence")
    _USE_NLTK = True
except Exception:
    _USE_NLTK = False

# ---------------------------------------------------------------------------
# Fallback stopword list / tokenizer (used only if NLTK isn't usable)
# ---------------------------------------------------------------------------
_FALLBACK_STOPWORDS = {
    "a", "an", "the", "is", "are", "was", "were", "be", "been", "being",
    "i", "you", "he", "she", "it", "we", "they", "me", "him", "her", "us",
    "them", "my", "your", "his", "its", "our", "their", "this", "that",
    "these", "those", "am", "do", "does", "did", "doing", "have", "has",
    "had", "having", "to", "of", "in", "on", "at", "for", "with", "about",
    "as", "by", "from", "and", "or", "but", "if", "so", "than", "too",
    "can", "could", "will", "would", "should", "shall", "may", "might",
    "not", "no", "nor", "up", "down", "out", "off", "over", "under",
    "again", "further", "then", "once", "here", "there", "when", "where",
    "why", "how", "all", "any", "both", "each", "few", "more", "most",
    "other", "some", "such", "only", "own", "same", "just", "what",
    "which", "who", "whom",
}


def _fallback_tokenize(text: str):
    text = text.translate(str.maketrans("", "", string.punctuation))
    return text.split()


def preprocess(text: str) -> str:
    """
    Clean and normalize a piece of text for similarity matching.

    Steps: lowercase -> remove punctuation/extra whitespace -> tokenize
    -> remove stopwords -> lemmatize -> rejoin into a single string.

    Returns a cleaned string (ready to be fed into TfidfVectorizer).
    """
    if not text:
        return ""

    text = text.lower().strip()
    # normalize whitespace, strip stray urls/numbers-only noise if needed
    text = re.sub(r"\s+", " ", text)

    if _USE_NLTK:
        text_no_punct = text.translate(str.maketrans("", "", string.punctuation))
        tokens = word_tokenize(text_no_punct)
        tokens = [t for t in tokens if t not in _STOPWORDS and t.isalpha()]
        tokens = [_LEMMATIZER.lemmatize(t) for t in tokens]
    else:
        tokens = _fallback_tokenize(text)
        tokens = [t for t in tokens if t not in _FALLBACK_STOPWORDS and t.isalpha()]

    return " ".join(tokens)


def using_nltk() -> bool:
    """Whether the real NLTK pipeline is active (vs. the fallback)."""
    return _USE_NLTK


if __name__ == "__main__":
    sample = "How can I RESET my password??"
    print("Using NLTK:", using_nltk())
    print("Original :", sample)
    print("Cleaned  :", preprocess(sample))