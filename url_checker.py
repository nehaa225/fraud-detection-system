import re

def check_url(url):

    suspicious_keywords = [
        "login", "verify", "bank", "secure",
        "account", "update", "free", "offer",
        "bonus", "win", "prize", "urgent"
    ]

    score = 0

    # Keyword check
    for word in suspicious_keywords:
        if word in url.lower():
            score += 1

    # Check for numbers in domain
    if re.search(r'\d', url):
        score += 1

    # Check for long URL
    if len(url) > 30:
        score += 1

    # Check for multiple dots
    if url.count('.') > 2:
        score += 1

    # Final decision
    if score >= 3:
        return f"⚠ High Risk URL (Score: {score})"
    elif score == 2:
        return f"⚠ Medium Risk URL (Score: {score})"
    else:
        return f"✅ Safe URL (Score: {score})"