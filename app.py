
import streamlit as st
import joblib
import pandas as pd

st.set_page_config(
    page_title="Phishing Detection",
    page_icon="🛡️",
    layout="wide"
)

m = joblib.load("models.pkl")

st.title("🛡️ Phishing Detection System")
st.write("Naive Bayes Machine Learning Classifier")

tab1, tab2, tab3 = st.tabs([
    "URL Scanner",
    "Email Scanner",
    "Accuracy Comparison"
])

with tab1:
    st.subheader("Website URL Scanner")
    url = st.text_input("Enter URL")

    if st.button("Scan URL"):
        if url.strip():
            x = m["url_vectorizer"].transform([url])
            score = m["url_model"].predict_proba(x)[0][1] * 100

            st.metric("Phishing Risk Score", f"{score:.2f}%")

            if m["url_model"].predict(x)[0] == 1:
                st.error("PHISHING URL DETECTED!")
            else:
                st.success("LEGITIMATE URL")
        else:
            st.warning("Enter a URL first.")

with tab2:
    st.subheader("Email Scanner")
    email = st.text_area("Paste email content")

    if st.button("Scan Email"):
        if email.strip():
            x = m["email_vectorizer"].transform([email])
            score = m["email_model"].predict_proba(x)[0][1] * 100

            st.metric("Phishing Risk Score", f"{score:.2f}%")

            if m["email_model"].predict(x)[0] == 1:
                st.error("PHISHING EMAIL DETECTED!")
            else:
                st.success("SAFE EMAIL")
        else:
            st.warning("Paste email content first.")

with tab3:
    st.subheader("Model Accuracy Comparison")

    df = pd.DataFrame({
        "Accuracy (%)": [
            m["url_accuracy"],
            m["email_accuracy"]
        ]
    }, index=["URL Detection", "Email Detection"])

    st.bar_chart(df)
    st.table(df.round(2))

st.caption("Machine Learning Phishing Detection Project")
