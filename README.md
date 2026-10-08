# Real-Time Browser-Based Fake News Detection System

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-REST%20API-green.svg)](https://flask.palletsprojects.com/)
[![Chrome Extension](https://img.shields.io/badge/Chrome-Manifest%20V3-yellow.svg)](https://developer.chrome.com/docs/extensions/)
[![Machine Learning](https://img.shields.io/badge/ML-TF--IDF%20%7C%20SVM-orange.svg)]()
[![Explainable AI](https://img.shields.io/badge/XAI-LIME-red.svg)]()

## Overview

This project is a real-time, browser-based fake news detection system that operates as a Google Chrome extension. It evaluates news articles at the point of reading and provides users with an automated credibility assessment (Fake News or Real News).

To address the "black-box" nature of traditional machine learning models, this system integrates Local Interpretable Model-Agnostic Explanations (LIME) to provide word-level transparency. Every prediction highlights the specific words that influenced the classification, empowering users to understand the model's reasoning.

## Features

* Point-of-Reading Detection: Extracts and classifies news text seamlessly within the browser without requiring manual copy-pasting.
* Explainable AI (XAI): Generates top 10 word-level explanations using LIME to show exactly which terms drove the prediction.
* Lightweight & Efficient: Utilizes a classical Machine Learning pipeline (TF-IDF + Linear SVM) for ultra-fast, real-time inference on standard hardware.
* Context-Aware Visual Feedback: Clean Manifest V3 Chrome extension popup featuring a confidence percentage bar and color-coded results.

## System Architecture

The system follows a client-server architecture:

1. Client (Chrome Extension): Built with HTML, CSS, and JavaScript (Manifest V3). It extracts the article text from the active webpage and sends it to the backend.
2. Server (Flask REST API): Built with Python. It receives the text, preprocesses it, vectorizes it using a trained TF-IDF model, classifies it using a Calibrated Linear SVM, and generates a LIME explanation.

## Directory Structure

Based on the project's design, organize your files as follows:

```text
Fake-News-Detection-System/
│
├── dataset/
│   ├── Fake.csv
│   └── True.csv
│
├── saved_model/                 # Generated after running train_model.py
│   ├── fake_news_model.pkl
│   └── tfidf_vectorizer.pkl
│
├── chrome_extension/
│   ├── manifest.json
│   ├── content.js
│   ├── popup.html
│   ├── popup.css
│   ├── popup.js
│   └── icons/                   # (Add your extension icons here)
│
├── train_model.py               # Script to train the SVM model
├── app.py                       # Flask REST API server
├── requirements.txt
└── README.md
```

## Installation & Setup

### Prerequisites

* Python 3.11 or higher
* Google Chrome Browser

### 1. Backend Setup (Machine Learning & Flask API)

1. Clone the repository and navigate to the project directory:
   ```bash
   cd Fake-News-Detection-System ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate ```
3. Install the required dependencies:
   (Ensure you have `pandas`, `numpy`, `scikit-learn`, `joblib`, `lime`, and `flask` installed).
   ```bash
   pip install pandas numpy scikit-learn joblib lime flask ```
4. Download the Dataset:
   Place the ISOT Fake News Dataset files (`Fake.csv` and `True.csv`) into the `dataset/` folder.
5. Train the Model:
   Run the training script to clean the data, train the TF-IDF vectorizer and SVM model, and save them to the `saved_model/` directory.
   ```bash
   python train_model.py ```
6. Start the Flask API:
   ```bash
   python app.py ```
   *The server will start running at `http://127.0.0.1:5000/`.*

### 2. Frontend Setup (Chrome Extension)

1. Open Google Chrome and navigate to `chrome://extensions/`.
2. Enable "Developer mode" by toggling the switch in the top right corner.
3. Click the "Load unpacked" button in the top left.
4. Select the `chrome_extension/` folder from this project repository.
5. The "Fake News Detector" extension should now appear in your browser toolbar.

## Usage

1. Ensure the Flask API is actively running in your terminal.
2. Open an English-language news article in Google Chrome (e.g., BBC, CNN, etc.).
3. Click on the "Fake News Detector" extension icon in your toolbar.
4. Click "Analyze Current Page".
5. Wait a moment for the system to process the text. The popup will display the predicted class (Real or Fake), a confidence score, and a list of the top words that influenced the decision.

## Performance Metrics

Evaluated on the held-out ISOT test set (8,562 articles):

* Accuracy: 99.78%
* Precision: 1.00
* Recall: 1.00
* F1-Score: 1.00

*Note: Real-world testing on live news webpages may yield different confidence intervals due to linguistic variations and data distribution shifts outside the foundational training corpus.*

## Limitations

* Language: Supports English-language text only. It cannot currently process Hausa, Yoruba, Igbo, or other Nigerian languages.
* Media: Analyzes text only. It does not evaluate manipulated images, audio, or video.
* Nature of the Tool: This system acts as an automated credibility signal based on learned stylistic deception markers. It does not replace human fact-checking or cross-referencing against live databases.

## References & Documentation

For full details regarding the research methodology, system design, and literature review, please refer to the primary project documentation file: "A Real-Time Browser-Based Fake News Detection System".
