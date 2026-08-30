from flask import Flask, request, jsonify
import joblib
import re
from explain import explain_prediction


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

    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "error": "No JSON data received"
            }), 400

        text = data.get("text", "")

        if not text.strip():
            return jsonify({
                "error": "No text provided"
            }), 400


        # Clean article text
        cleaned_text = clean_text(text)


        # Convert text to TF-IDF
        vectorized_text = vectorizer.transform([cleaned_text])


        # Make prediction
        prediction = model.predict(vectorized_text)[0]


        # Get calibrated probabilities
        probabilities = model.predict_proba(vectorized_text)[0]


        # Get the probability of the predicted class
        confidence = probabilities[prediction] * 100


        # Generate LIME explanation
        explanation = explain_prediction(cleaned_text)


        # The explanation is already a list of dictionaries
        important_words = explanation


        # Convert prediction number to label
        result = "Real News" if prediction == 1 else "Fake News"


        return jsonify({
            "prediction": result,
            "confidence": round(float(confidence), 2),
            "important_words": important_words
        })


    except Exception as e:

        print("\nERROR IN /predict:")
        print(e)

        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)