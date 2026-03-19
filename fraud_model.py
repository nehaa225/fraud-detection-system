import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

df = pd.read_csv("dataset.csv")

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df["message"])
y = df["label"]

model = LogisticRegression()
model.fit(X, y)

def predict_message(msg):
    msg_vec = vectorizer.transform([msg])
    result = model.predict(msg_vec)
    return "⚠ Fraud Detected" if result[0] == 1 else "✅ Safe Message"