"""
chatbot.py
----------
Core FAQ-matching logic.

Approach:
  1. Preprocess every FAQ question (see preprocess.py).
  2. Fit a TF-IDF vectorizer over all preprocessed FAQ questions.
  3. For a new user question: preprocess it the same way, vectorize it,
     and compute cosine similarity against every FAQ question.
  4. Return the FAQ with the highest similarity score, if it clears a
     minimum confidence threshold - otherwise return a fallback message.
"""

from dataclasses import dataclass
from typing import List, Optional

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from preprocess import preprocess
from faq_data import FAQS


@dataclass
class MatchResult:
    question: str
    answer: str
    score: float
    matched: bool


class FAQChatBot:
    """A simple retrieval-based FAQ chatbot using TF-IDF + cosine similarity."""

    def __init__(self, faqs: Optional[List[dict]] = None, threshold: float = 0.2):
        """
        faqs:      list of {"question": ..., "answer": ...} dicts.
        threshold: minimum cosine similarity (0-1) required to accept a match.
                   Lower it if the bot seems too "shy"; raise it if it gives
                   wrong answers too confidently.
        """
        self.faqs = faqs if faqs is not None else FAQS
        self.threshold = threshold

        self._raw_questions = [f["question"] for f in self.faqs]
        self._answers = [f["answer"] for f in self.faqs]

        # Combine each question with its optional tags (alternate phrasings)
        # before preprocessing, so the vectorizer learns more ways of asking
        # the same thing. Tags are never shown to the user.
        combined_texts = [
            f["question"] + " " + " ".join(f.get("tags", []))
            for f in self.faqs
        ]
        self._clean_questions = [preprocess(t) for t in combined_texts]

        # ngram_range=(1,2) lets the vectorizer also consider 2-word phrases
        # (e.g. "reset password"), which helps short FAQ-style questions.
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2))
        self._faq_matrix = self.vectorizer.fit_transform(self._clean_questions)

    def get_response(self, user_question: str) -> MatchResult:
        """Return the best-matching FAQ answer for a raw user question."""
        cleaned = preprocess(user_question)

        if not cleaned.strip():
            return MatchResult(
                question="",
                answer="Could you rephrase that? I didn't catch any keywords I recognize.",
                score=0.0,
                matched=False,
            )

        user_vec = self.vectorizer.transform([cleaned])
        similarities = cosine_similarity(user_vec, self._faq_matrix)[0]

        best_idx = similarities.argmax()
        best_score = float(similarities[best_idx])

        if best_score >= self.threshold:
            return MatchResult(
                question=self._raw_questions[best_idx],
                answer=self._answers[best_idx],
                score=best_score,
                matched=True,
            )

        return MatchResult(
            question="",
            answer=(
                "I'm not confident I have the right answer for that. "
                "Could you rephrase, or contact support@edulearn.example.com?"
            ),
            score=best_score,
            matched=False,
        )

    def top_matches(self, user_question: str, k: int = 3):
        """Return the top-k (question, answer, score) matches - useful for debugging."""
        cleaned = preprocess(user_question)
        user_vec = self.vectorizer.transform([cleaned])
        similarities = cosine_similarity(user_vec, self._faq_matrix)[0]
        ranked = similarities.argsort()[::-1][:k]
        return [
            (self._raw_questions[i], self._answers[i], float(similarities[i]))
            for i in ranked
        ]


if __name__ == "__main__":
    bot = FAQChatBot()
    test_questions = [
        "how do i make a new account",
        "i forgot my password, help!",
        "what cards can i pay with",
        "does the course give me a diploma",
        "what's the weather today",  # should NOT match anything
    ]
    for q in test_questions:
        result = bot.get_response(q)
        print(f"User: {q}")
        print(f"Bot ({result.score:.2f}): {result.answer}\n")