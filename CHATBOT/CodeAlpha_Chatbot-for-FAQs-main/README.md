# FAQ ChatBot (Internship Project)

A retrieval-based chatbot that answers FAQs about a product (sample topic:
"EduLearn", an online course platform) by matching a user's question to the
most similar entry in an FAQ knowledge base.

## How it works

```
faq_data.py       -> the FAQ knowledge base (questions + answers + optional tags)
preprocess.py      -> NLP cleaning: lowercase, tokenize, remove stopwords, lemmatize (NLTK)
chatbot.py          -> TF-IDF vectorization + cosine similarity matching (scikit-learn)
cli_chat.py          -> terminal chat interface
app.py + templates/  -> Flask web chat UI
streamlit_app.py     -> alternative Streamlit chat UI
```

Pipeline for each user message:
1. **Preprocess** the text (`preprocess.py`): lowercase -> strip punctuation ->
   tokenize -> remove stopwords -> lemmatize.
2. **Vectorize** every FAQ question (+ optional alternate phrasings) with
   `TfidfVectorizer` (unigrams + bigrams).
3. **Compare** the user's (also preprocessed) question against all FAQ
   vectors using **cosine similarity**.
4. **Respond** with the answer for the highest-scoring FAQ, if its score
   clears a confidence `threshold` (default `0.2`). Otherwise the bot
   admits it isn't sure and points to a human support contact.

## Setup

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

The first run downloads a few small NLTK data packages automatically
(punkt, stopwords, wordnet). If NLTK or its data can't be downloaded
(e.g. no internet), `preprocess.py` automatically falls back to a
lightweight built-in tokenizer/stopword list so the bot still works -
you'll just lose lemmatization.

## Run it

**Terminal chat:**
```bash
python cli_chat.py
```

**Web UI (Flask):**
```bash
python app.py
# open http://127.0.0.1:5000
```

**Web UI (Streamlit - simpler, optional):**
```bash
streamlit run streamlit_app.py
```

## Customizing for your own product

Edit `faq_data.py` - each entry is:

```python
{
    "question": "How do I do X?",
    "answer": "Here's how...",
    "tags": ["alternate phrasing 1", "keyword 2"],   # optional, improves matching
}
```

`tags` are never shown to the user; they just give the similarity matcher
more ways of recognizing the same question (e.g. "diploma" as a paraphrase
of "certificate").

## Tuning match quality

`FAQChatBot(threshold=0.2)` in `chatbot.py` controls how confident the bot
must be before it answers:
- **Lower it** (e.g. `0.15`) if the bot too often says "I'm not sure".
- **Raise it** (e.g. `0.3`) if it confidently gives wrong answers.

Run `python chatbot.py` to see example matches and scores, or use
`FAQChatBot.top_matches(question, k=3)` to debug a specific query.

## Notes / limitations

- This is a **retrieval-based** bot (it picks the closest existing FAQ), not
  a generative one - it will never invent a new answer.
- TF-IDF + cosine similarity is keyword-based, so questions that don't share
  any words/synonyms with an FAQ (and its tags) won't match. Adding more
  `tags` per FAQ is the easiest way to improve coverage.
- For semantic (meaning-based) matching instead of keyword overlap, this
  could be swapped for sentence embeddings (e.g. `sentence-transformers`)
  while keeping the same cosine-similarity matching logic.