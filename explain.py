import joblib
from lime.lime_text import LimeTextExplainer


# Load model and vectorizer
model = joblib.load("saved_model/fake_news_model.pkl")
vectorizer = joblib.load("saved_model/tfidf_vectorizer.pkl")


# LIME explainer
explainer = LimeTextExplainer(
    class_names=["Fake News", "Real News"]
)


def predict_proba(texts):
    """
    Return calibrated probabilities for LIME.
    """

    vectors = vectorizer.transform(texts)

    return model.predict_proba(vectors)


def explain_prediction(text):
    """
    Generate a LIME explanation for the prediction.
    """

    explanation = explainer.explain_instance(
        text,
        predict_proba,
        num_features=10
    )

    return [
        {
            "word": word,
            "weight": round(weight, 4)
        }
        for word, weight in explanation.as_list()
    ]