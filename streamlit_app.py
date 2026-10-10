
import os
import streamlit as st
import requests

# Page configuration
st.set_page_config(
    page_title="CIFAR-10 AI Classifier",
    page_icon="🤖",
    layout="wide"
)

# Flask API URL:
# Local default: http://127.0.0.1:5000
# Docker: set FLASK_API_URL to the Flask service address
API_URL = os.getenv(
    "FLASK_API_URL",
    "http://127.0.0.1:5000"
).rstrip("/")

st.title("🤖 CIFAR-10 Image Classification")
st.write(
    "Upload an image and get a real-time prediction "
    "using the Flask API backend."
)

st.divider()
st.subheader("📤 Upload an Image")

uploaded_file = st.file_uploader(
    "Choose a JPG, JPEG or PNG image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
    st.success("Image uploaded successfully!")

    st.image(
        uploaded_file,
        caption="Uploaded Image",
        width=350
    )

    if st.button("🔍 Predict", type="primary"):
        with st.spinner("Sending image to Flask API..."):
            try:
                files = {
                    "image": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        uploaded_file.type
                    )
                }

                response = requests.post(
                    f"{API_URL}/predict",
                    files=files,
                    timeout=120
                )

                try:
                    result = response.json()
                except ValueError:
                    result = {}

                if response.status_code == 200:
                    prediction = result["prediction"]
                    confidence = float(result["confidence"])

                    st.success(f"Prediction: {prediction}")

                    col1, col2 = st.columns(2)

                    col1.metric(
                        "Predicted Class",
                        prediction
                    )

                    col2.metric(
                        "Confidence",
                        f"{confidence:.2f}%"
                    )

                    if "response_time_ms" in result:
                        st.caption(
                            "API response time: "
                            f"{result['response_time_ms']:.2f} ms"
                        )

                else:
                    st.error(
                        result.get(
                            "error",
                            f"API request failed: HTTP "
                            f"{response.status_code}"
                        )
                    )

            except requests.exceptions.Timeout:
                st.error(
                    "The prediction request timed out. "
                    "Please try again."
                )

            except requests.exceptions.ConnectionError:
                st.error(
                    f"Unable to connect to Flask API at {API_URL}. "
                    "Check that the Flask service is running "
                    "and the API URL is configured correctly."
                )

            except Exception as exc:
                st.error(f"An error occurred: {exc}")

else:
    st.info("👆 Please upload an image to get a prediction.")

st.divider()
st.caption("Task 15 — Deep Learning Production Deployment")
