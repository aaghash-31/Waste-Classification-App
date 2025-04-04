import streamlit as st
import torch
import torch.nn as nn
from efficientnet_pytorch import EfficientNet
from PIL import Image, ImageGrab
import torchvision.transforms as transforms
import time

# Set device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load the trained EfficientNet model
model = EfficientNet.from_name('efficientnet-b0')  
num_ftrs = model._fc.in_features
model._fc = nn.Linear(num_ftrs, 2)  # Modify final layer for binary classification
model.load_state_dict(torch.load('waste_classification_model.pth', map_location=device))
model = model.to(device)
model.eval()

# Define class names
class_names = ['Non-Recyclable ', 'Recyclable ']

# Define image transformation
transform = transforms.Compose([
    transforms.Resize((224, 224)),  
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])  
])

# Function to predict class
def predict_image(image):
    image = transform(image).unsqueeze(0)  
    image = image.to(device)
    
    with torch.no_grad():
        outputs = model(image)
        probabilities = torch.softmax(outputs, dim=1)
        confidence, predicted = torch.max(probabilities, 1)
        return class_names[predicted.item()], confidence.item() * 100

# Streamlit App UI
st.markdown('<h1 style="text-align: center;">♻️ Waste Classification App</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Upload, capture, or paste an image to classify waste.</p>", unsafe_allow_html=True)

# Tabs for input methods
tab1, tab2, tab3 = st.tabs(["📤 Upload Image", "📸 Use Camera", "📋 Paste from Clipboard"])

image = None  # Placeholder for input image

# Upload Image Tab
with tab1:
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        image = Image.open(uploaded_file).convert('RGB')

# Camera Capture Tab
with tab2:
    camera_image = st.camera_input("Take a picture")
    if camera_image:
        image = Image.open(camera_image).convert('RGB')

# Paste from Clipboard Tab
with tab3:
    st.write("Press **Ctrl+V** (Cmd+V on Mac) to paste an image.")
    if st.button("Paste Image"):
        try:
            image = ImageGrab.grabclipboard()
            if image is None:
                st.error("No image found in clipboard. Copy an image and try again.")
        except Exception as e:
            st.error(f"Error accessing clipboard: {e}")

# Display and classify the image
if image:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.image(image, caption='Selected Image', use_column_width=True)
    
    with col2:
        st.markdown('<div style="text-align: center;">', unsafe_allow_html=True)
        with st.spinner("Classifying..."):
            time.sleep(1)  
            prediction, confidence = predict_image(image)
        icon = "♻️" if prediction == "Recyclable " else "🗑️"
        st.markdown(f'<h2>{icon} {prediction}</h2>', unsafe_allow_html=True)
        st.write(f"**Confidence:** {confidence:.2f}%")
        st.markdown('</div>', unsafe_allow_html=True)
