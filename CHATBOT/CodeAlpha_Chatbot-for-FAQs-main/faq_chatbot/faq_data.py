"""
faq_data.py
-----------
Sample FAQ knowledge base for the chatbot.

Replace/extend FAQS with questions & answers about YOUR own product or topic.
Each entry is a dict with:
    "question": the canonical way the question is usually asked
    "answer":   the answer to show the user

Optional "tags": a few alternate phrasings / keywords for the same question.
They are never shown to the user - they're merged in only to help the
similarity matcher recognize more ways of asking the same thing.
"""

FAQS = [
    {
        "question": "How do I create an account on EduLearn?",
        "answer": "Click 'Sign Up' on the top-right of the homepage, enter your email "
                  "and password, and verify your email address using the link we send you.",
        "tags": ["sign up", "register", "new account", "make an account"],
    },
    {
        "question": "How can I reset my password?",
        "answer": "Go to the login page and click 'Forgot Password'. Enter your registered "
                  "email and we'll send you a link to reset your password.",
        "tags": ["forgot password", "change password", "can't log in", "login issue"],
    },
    {
        "question": "What payment methods do you accept?",
        "answer": "We accept Visa, MasterCard, American Express, PayPal, and major mobile "
                  "wallets such as Apple Pay and Google Pay.",
        "tags": ["credit card", "debit card", "pay with", "payment options", "paypal"],
    },
    {
        "question": "How do I enroll in a course?",
        "answer": "Open the course page and click 'Enroll Now'. If it's a paid course you'll "
                  "be taken to checkout; free courses are added to 'My Courses' instantly.",
        "tags": ["sign up for a course", "join a course", "buy a course", "register for class"],
    },
    {
        "question": "Can I get a refund if I am not satisfied with a course?",
        "answer": "Yes, we offer a full refund within 14 days of purchase if you have "
                  "completed less than 20% of the course. Go to 'My Purchases' to request one.",
        "tags": ["money back", "return a course", "cancel purchase", "refund policy"],
    },
    {
        "question": "Do I get a certificate after completing a course?",
        "answer": "Yes, a downloadable certificate of completion is issued automatically once "
                  "you finish 100% of the course content and pass any required quizzes.",
        "tags": ["diploma", "certification", "proof of completion", "certificate of completion"],
    },
    {
        "question": "Can I access courses on my mobile phone?",
        "answer": "Yes, EduLearn is fully responsive and also has free iOS and Android apps "
                  "so you can learn on the go, including offline video downloads.",
        "tags": ["mobile app", "android", "iphone", "ios app", "phone access"],
    },
    {
        "question": "How long do I have access to a purchased course?",
        "answer": "Once purchased, you have lifetime access to the course, including all "
                  "future updates made by the instructor.",
        "tags": ["access duration", "expire", "lifetime access", "how long can i watch"],
    },
    {
        "question": "How do I contact customer support?",
        "answer": "You can reach us via the 'Help' chat bubble in the app, or email "
                  "support@edulearn.example.com. We typically reply within 24 hours.",
        "tags": ["customer service", "help desk", "get in touch", "talk to a human"],
    },
    {
        "question": "Is there a free trial available?",
        "answer": "Yes, new users get a 7-day free trial with access to select premium "
                  "courses. No credit card is required to start the trial.",
        "tags": ["trial period", "try for free", "free week"],
    },
    {
        "question": "How do I download a course video for offline viewing?",
        "answer": "Open the lesson in the mobile app and tap the download icon next to the "
                  "video. Downloaded videos appear under 'Downloads' in your profile.",
        "tags": ["offline mode", "save video", "watch without internet"],
    },
    {
        "question": "Can I switch or cancel my subscription plan?",
        "answer": "Yes, go to Account Settings > Subscription, where you can upgrade, "
                  "downgrade, or cancel at any time. Changes apply from the next billing cycle.",
        "tags": ["cancel subscription", "downgrade plan", "upgrade plan", "change plan"],
    },
    {
        "question": "Do you offer discounts for students?",
        "answer": "Yes, students with a valid .edu email address get 20% off all paid "
                  "courses and subscription plans. Verify your student status in Account Settings.",
        "tags": ["student discount", "edu discount", "cheaper for students"],
    },
    {
        "question": "How can I become an instructor on EduLearn?",
        "answer": "Click 'Teach on EduLearn' in the footer, fill out the instructor "
                  "application, and our team will review it within 3-5 business days.",
        "tags": ["become a teacher", "teach a course", "create a course", "instructor application"],
    },
    {
        "question": "Why can't I play a course video?",
        "answer": "Try refreshing the page, checking your internet connection, or clearing "
                  "your browser cache. If the problem continues, contact support with the "
                  "course name and a screenshot of the error.",
        "tags": ["video not playing", "video won't load", "buffering", "playback error"],
    },
]