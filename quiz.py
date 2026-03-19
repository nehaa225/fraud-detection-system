import random

def get_quiz():
    questions = [
        {
            "question": "Should you share OTP with bank officials?",
            "options": ["Yes", "No"],
            "answer": "No"
        },
        {
            "question": "Is it safe to click unknown links?",
            "options": ["Yes", "No"],
            "answer": "No"
        },
        {
            "question": "What should you do if you win a lottery you didn’t enter?",
            "options": ["Claim it", "Ignore it"],
            "answer": "Ignore it"
        },
        {
            "question": "Should you verify bank details on unknown websites?",
            "options": ["Yes", "No"],
            "answer": "No"
        },
        {
            "question": "Is sharing your password safe?",
            "options": ["Yes", "No"],
            "answer": "No"
        }
    ]

    return random.choice(questions)