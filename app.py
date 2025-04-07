import streamlit as st
import numpy as np
import time
from PIL import Image
import io
import requests

# 🔹 Page Config
st.set_page_config(page_title="Waste Classification App", page_icon="♻️", layout="wide")

# 🔹 Custom CSS Styling
st.markdown("""
    <style>
    body, .stApp { background-color: #121212 !important; color: #e0e0e0 !important; }
    .header { text-align: center; font-size: 32px; font-weight: bold; padding: 20px; }
    .header-subtext { text-align: center; font-size: 16px; color: #aaa; margin-bottom: 20px; }
    .prediction-box { background-color: #2c2c2c; padding: 20px; border-radius: 10px; border: 2px solid #4CAF50; }
    .prediction-text { font-size: 26px; font-weight: bold; color: #4CAF50; margin-bottom: 5px; }
    .confidence-text { font-size: 18px; color: #b0b0b0; margin-top: -5px; }
    h1, h2 { color: #e0e0e0 !important; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# 🔹 Header
st.markdown('<h1 class="header">♻️ Waste Classification App</h1>', unsafe_allow_html=True)
st.markdown('<p class="header-subtext">Upload an image, capture from camera, or paste a public image URL to classify waste.</p>', unsafe_allow_html=True)

# 🔹 Options
tabs = ["📂 Upload Image", "📸 Use Camera", "🌐 Paste Image URL"]
selected_tab = st.radio("", tabs, horizontal=True)

image = None

# 🔹 Upload Image
if selected_tab == "📂 Upload Image":
    uploaded_file = st.file_uploader("Upload or drop an image", type=["png", "jpg", "jpeg"])
    if uploaded_file:
        try:
            image = Image.open(uploaded_file).convert("RGB")
            st.image(image, caption="Uploaded Image")
        except Exception as e:
            st.error(f"Error reading image: {e}")

# 🔹 Camera
elif selected_tab == "📸 Use Camera":
    captured_image = st.camera_input("Capture an image")
    if captured_image:
        try:
            image = Image.open(captured_image).convert("RGB")
            st.image(image, caption="Captured Image")
        except Exception as e:
            st.error(f"Error reading image: {e}")

# 🔹 URL Image
elif selected_tab == "🌐 Paste Image URL":
    url = st.text_input("Paste an image URL (JPEG/PNG)")
    if url:
        try:
            response = requests.get(url)
            image = Image.open(io.BytesIO(response.content)).convert("RGB")
            st.image(image, caption="Image from URL")
        except Exception as e:
            st.error(f"Could not load image from URL: {e}")

# 🔹 Dummy Prediction Function
def predict_image(image):
    classes = ["Recyclable", "Non-Recyclable"]
    prediction = np.random.choice(classes)
    confidence = np.random.uniform(50, 95)
    return prediction, confidence

# 🔹 Show Result
if image:
    with st.container():
        st.markdown('<div class="prediction-box">', unsafe_allow_html=True)
        with st.spinner("Classifying..."):
            time.sleep(1)
            prediction, confidence = predict_image(image)
        icon = "♻️" if prediction == "Recyclable" else "🗑️"
        st.markdown(f'<p class="prediction-text">{icon} {prediction}</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="confidence-text">Confidence: {confidence:.2f}%</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
