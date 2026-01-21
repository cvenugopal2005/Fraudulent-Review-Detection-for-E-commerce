import streamlit as st
import requests

st.set_page_config(
    page_title="Fraudulent Review Detection",
    layout="centered"
)

st.title("🛒 Fraudulent Review Detection System")
st.write("Analyze e-commerce reviews for authenticity using AI")

review = st.text_area("Enter product review text:")

if st.button("Check Review Authenticity"):
    if review.strip() == "":
        st.warning("Please enter a review to analyze.")
    else:
        try:
            response = requests.post(
                "http://127.0.0.1:8000/predict",
                json={"review": review}
            )
            result = response.json()

            st.success(f"Prediction: **{result['label']}**")
            st.info(f"Confidence Score: **{result['confidence']}%**")

        except Exception as e:
            st.error("Backend server is not running.")
