import joblib
import re

from lime.lime_text import LimeTextExplainer

# Load the trained model and vectorizer
model = joblib.load("saved_model/fake_news_model.pkl")
vectorizer = joblib.load("saved_model/tfidf_vectorizer.pkl")


# Clean text
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


# Function required by LIME
def predict_proba(texts):
    cleaned = [clean_text(text) for text in texts]
    vectors = vectorizer.transform(cleaned)
    return model.predict_proba(vectors)


# Create the explainer
explainer = LimeTextExplainer(
    class_names=["Fake News", "Real News"]
)


def explain_prediction(text):
    explanation = explainer.explain_instance(
        text,
        predict_proba,
        num_features=10
    )

    return explanation.as_list()