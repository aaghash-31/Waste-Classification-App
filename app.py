import streamlit as st
import numpy as np
import time
from PIL import Image, ImageGrab
import io

# 🔹 Set Page Configuration
st.set_page_config(page_title="Waste Classification App", page_icon="♻️", layout="wide")

# 🔹 Custom CSS Styling
st.markdown("""
    <style>
    body, .stApp { background-color: #121212 !important; color: #e0e0e0 !important; }
    .header { text-align: center; font-size: 32px; font-weight: bold; padding: 20px; }
    .header-subtext { text-align: center; font-size: 16px; color: #aaa; margin-bottom: 20px; }
    .prediction-box { background-color: #2c2c2c; padding: 20px; border-radius: 10px; border: none; }
    .prediction-text { font-size: 26px; font-weight: bold; color: #4CAF50; margin-bottom: 5px; }
    .confidence-text { font-size: 18px; color: #b0b0b0; margin-top: -5px; }
    .image-container { border-radius: 10px; overflow: hidden; background-color: #2c2c2c; border: 2px solid #444; }
    .footer { text-align: center; color: #888; margin-top: 30px; font-size: 14px; }
    h1, h2 { color: #e0e0e0 !important; text-align: center; }

    /* ✅ Hide any unwanted inputs */
    .stTextInput, .stTextArea, .stText, .css-1y4p8pa, .css-1x8cf1d { display: none !important; }
    </style>
""", unsafe_allow_html=True)

# 🔹 Header
st.markdown('<h1 class="header">♻️ Waste Classification App</h1>', unsafe_allow_html=True)
st.markdown('<p class="header-subtext">Upload an image, use your camera, or paste an image to classify waste.</p>', unsafe_allow_html=True)

# 🔹 Sidebar with Tabs
tabs = ["📂 Upload Image", "📸 Use Camera", "📋 Paste Image"]
selected_tab = st.radio("", tabs, horizontal=True)

# 🔹 Image Upload Function
def load_image(uploaded_file):
    image = Image.open(uploaded_file).convert("RGB")
    return image

# 🔹 Image Capture from Camera
if selected_tab == "📸 Use Camera":
    image = st.camera_input("Take a picture")
    if image:
        image = load_image(image)
        st.image(image, caption="Captured Image")

# 🔹 Image Upload
elif selected_tab == "📂 Upload Image":
    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    if uploaded_file:
        image = load_image(uploaded_file)
        st.image(image, caption="Uploaded Image")

# 🔹 Paste Image
elif selected_tab == "📋 Paste Image":
    if st.button("Paste Image"):
        try:
            image = ImageGrab.grabclipboard()
            if isinstance(image, Image.Image):
                st.success("Image pasted successfully!")
                st.image(image, caption="Pasted Image")
            else:
                st.error("No image found in clipboard. Please copy an image and try again.")
        except Exception as e:
            st.error(f"Error accessing clipboard: {e}")

# 🔹 Waste Classification Function (Simulated)
def predict_image(image):
    # Simulated classification
    classes = ["Recyclable", "Non-Recyclable"]
    prediction = np.random.choice(classes)
    confidence = np.random.uniform(50, 95)  # Simulated confidence
    return prediction, confidence

# 🔹 Display Classification Result
if "image" in locals():
    with st.container():
        st.markdown('<div class="prediction-box">', unsafe_allow_html=True)
        with st.spinner("Classifying..."):
            time.sleep(1)  # Simulated delay
            prediction, confidence = predict_image(image)

        icon = "♻️" if prediction == "Recyclable" else "🗑️"
        st.markdown(f'<p class="prediction-text">{icon} {prediction}</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="confidence-text">Confidence: {confidence:.2f}%</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
