import joblib

MODEL_PATH = "models/fake_review_model.pkl"
VECTORIZER_PATH = "models/tfidf_vectorizer.pkl"

model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)

def predict_review(review_text: str):
    review_vec = vectorizer.transform([review_text])
    prediction = model.predict(review_vec)[0]
    probability = model.predict_proba(review_vec)[0].max()

    return {
        "label": "Fake Review" if prediction == 1 else "Genuine Review",
        "confidence": round(probability * 100, 2)
    }
