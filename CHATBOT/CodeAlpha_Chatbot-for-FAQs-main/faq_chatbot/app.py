"""
app.py
------
Flask web UI for the FAQ chatbot.
"""

from flask import Flask, render_template, request, jsonify

from chatbot import FAQChatBot
from faq_data import FAQS

app = Flask(__name__)
bot = FAQChatBot()


@app.route("/")
def index():
    # Show the list of sample questions as clickable suggestions.
    sample_questions = [f["question"] for f in FAQS[:6]]
    return render_template("index.html", sample_questions=sample_questions)


@app.route("/api/ask", methods=["POST"])
def ask():
    data = request.get_json(silent=True) or {}
    user_question = (data.get("message") or "").strip()

    if not user_question:
        return jsonify({"answer": "Please type a question.", "matched": False, "score": 0}), 400

    result = bot.get_response(user_question)
    return jsonify({
        "answer": result.answer,
        "matched": result.matched,
        "matched_question": result.question,
        "score": round(result.score, 3),
    })


if __name__ == "__main__":
    app.run(debug=True)