from explain import explain_prediction
from flask import Flask, request, jsonify
import joblib
import re

app = Flask(__name__)

# Load saved model and vectorizer
model = joblib.load("saved_model/fake_news_model.pkl")
vectorizer = joblib.load("saved_model/tfidf_vectorizer.pkl")


# Text cleaning function
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


@app.route("/")
def home():
    return "Fake News Detection API is running!"


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    text = data.get("text", "")

    cleaned_text = clean_text(text)

    vectorized_text = vectorizer.transform([cleaned_text])

    prediction = model.predict(vectorized_text)[0]

    probabilities = model.predict_proba(vectorized_text)[0]

    confidence = max(probabilities) * 100

    explanation = explain_prediction(text)

    important_words = []

    for word, weight in explanation:
        important_words.append({
            "word": word,
            "weight": round(weight, 4)
        })

    result = "Real News" if prediction == 1 else "Fake News"

    return jsonify({
        "prediction": result,
        "confidence": round(confidence, 2),
        "important_words": important_words
    })

if __name__ == "__main__":
    app.run(debug=True)