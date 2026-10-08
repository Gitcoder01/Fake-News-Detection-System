import re
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import accuracy_score, classification_report

# 1. LOAD DATASETS
print("Loading datasets...")

true = pd.read_csv("dataset/True.csv")
# Randomly sample the fake dataset to match the true dataset size exactly
fake = pd.read_csv("dataset/Fake.csv").sample(n=len(true), random_state=42)

print(f"Fake news articles: {len(fake)}")
print(f"Real news articles: {len(true)}")

# 2. ADD LABELS
fake["label"] = 0
true["label"] = 1

# 3. COMBINE DATASETS
data = pd.concat([fake, true], ignore_index=True)

# Shuffle
data = data.sample(frac=1, random_state=42).reset_index(drop=True)

print(f"Total articles: {len(data)}")

# 4. CLEAN TEXT


def clean_text(text):
    text = str(text).lower()

    # Remove URLs
    text = re.sub(r"http\S+|www\S+", "", text)

    # Keep letters and spaces
    text = re.sub(r"[^a-zA-Z\s]", " ", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text

# 5. CREATE CONTENT COLUMN
# Handle missing value


data["title"] = data["title"].fillna("")
data["text"] = data["text"].fillna("")

# Combine title + article body
data["content"] = data["title"] + " " + data["text"]

# Clean combined text
data["content"] = data["content"].apply(clean_text)

# 6. REMOVE EMPTY ARTICLES
data = data[
    data["content"].str.len() > 50
].reset_index(drop=True)

print(f"Articles after cleaning: {len(data)}")

# 7. SPLIT DATA
X = data["content"]
y = data["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print(f"Training samples: {len(X_train)}")
print(f"Testing samples: {len(X_test)}")

# 8. TF-IDF VECTORIZATION
print("\nCreating TF-IDF vectorizer...")

vectorizer = TfidfVectorizer(
    max_features=100000,
    ngram_range=(1, 2),
    min_df=2,
    max_df=0.95,
    sublinear_tf=True
)

X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

print("TF-IDF vectorization complete.")

# 9. TRAIN LINEAR SVM
print("\nTraining Linear SVM model...")

svm_model = LinearSVC(
    C=1.0,
    random_state=42
)

svm_model.fit(X_train_tfidf, y_train)

print("Linear SVM training complete.")

# 10. CALIBRATE MODEL
print("\nCalibrating model probabilities...")

model = CalibratedClassifierCV(
    estimator=svm_model,
    method="sigmoid",
    cv=3
)

model.fit(X_train_tfidf, y_train)

print("Probability calibration complete.")

# 11. EVALUATE MODEL
y_pred = model.predict(X_test_tfidf)

accuracy = accuracy_score(y_test, y_pred)

print("\n==========================================")
print("MODEL EVALUATION")
print("==========================================")

print(f"\nAccuracy: {accuracy:.4f}")

print("\nClassification Report:")

print(
    classification_report(
        y_test,
        y_pred,
        target_names=["Fake News", "Real News"]
    )
)

# 12. TEST PROBABILITIES
probabilities = model.predict_proba(X_test_tfidf[:5])

print("\nSample calibrated probabilities:")

for i, probability in enumerate(probabilities):
    print(
        f"Article {i + 1}: "
        f"Fake={probability[0] * 100:.2f}% | "
        f"Real={probability[1] * 100:.2f}%"
    )

# 13. SAVE MODEL AND VECTORIZER
print("\nSaving model...")

joblib.dump(
    model,
    "saved_model/fake_news_model.pkl"
)

joblib.dump(
    vectorizer,
    "saved_model/tfidf_vectorizer.pkl"
)

print("\n==========================================")
print("SUCCESS!")
print("==========================================")

print("Model saved to:")
print("saved_model/fake_news_model.pkl")

print("\nVectorizer saved to:")
print("saved_model/tfidf_vectorizer.pkl")
