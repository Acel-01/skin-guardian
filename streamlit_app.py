import streamlit as st
import requests
from PIL import Image
import io
import os

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="Skin Guardian AI", page_icon="🛡️")

st.title("🛡️ Skin Guardian AI")
st.write("Upload a photo of a skin condition for an instant AI screening.")

# 1. Image Uploader
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_container_width=True)
    
    if st.button("Analyze Skin Condition"):
        with st.spinner('Analyzing...'):
            # 2. Convert image to bytes for the API request
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='JPEG')
            img_bytes = img_byte_arr.getvalue()

            # 3. Send request to FastAPI backend
            # Note: Using localhost for now. Change to service name in Docker.
            try:
                files = {"file": ("image.jpg", img_bytes, "image/jpeg")}
                response = requests.post(f"{BACKEND_URL}/predict", files=files)
                
                if response.status_code == 200:
                    result = response.json()
                    st.success(f"Diagnosis: **{result['prediction']}**")
                    st.info(f"Confidence Level: {result['confidence']:.2%}")
                else:
                    st.error("Failed to get prediction from server.")
            except Exception as e:
                st.error(f"Error connecting to backend: {e}")
