"""
cli_chat.py
-----------
Simple terminal chat loop for the FAQ chatbot.

Run:
    python cli_chat.py
Type 'quit' or 'exit' to stop.
"""

from chatbot import FAQChatBot
from preprocess import using_nltk


def main():
    bot = FAQChatBot()
    print("=" * 60)
    print(" FAQ ChatBot  (type 'quit' to exit)")
    print(f" NLP backend: {'NLTK' if using_nltk() else 'fallback tokenizer (NLTK not installed)'}")
    print("=" * 60)
    print("Bot: Hi! Ask me anything about EduLearn - accounts, courses, "
          "payments, certificates, and more.\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBot: Goodbye!")
            break

        if not user_input:
            continue
        if user_input.lower() in {"quit", "exit", "bye"}:
            print("Bot: Goodbye! 👋")
            break

        result = bot.get_response(user_input)
        print(f"Bot: {result.answer}")
        # Uncomment the line below while testing to see the confidence score:
        # print(f"     (matched: {result.matched}, score: {result.score:.2f})")
        print()


if __name__ == "__main__":
    main()