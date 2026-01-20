from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

import onnxruntime as ort
import numpy as np
from PIL import Image
import io
import os

app = FastAPI()

origins_raw = os.getenv("ALLOWED_ORIGINS", "http://localhost:8501")
origins = origins_raw.split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model once at startup for speed
session = ort.InferenceSession("skin_guardian.onnx")
CLASSES = ['Arsenic', 'Eczema', 'Melanoma', 'Normal', 'Psoriasis']

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # 1. Read image from request
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert('RGB')
    
    # 2. Preprocess (same logic as our fixed test script)
    image = image.resize((224, 224))
    img_data = np.array(image).astype('float32') / 255.0
    img_data = (img_data - [0.485, 0.456, 0.406]) / [0.229, 0.224, 0.225]
    img_data = np.transpose(img_data, (2, 0, 1))
    img_data = np.expand_dims(img_data.astype('float32'), axis=0)

    # 3. Run Inference
    input_name = session.get_inputs()[0].name
    raw_result = session.run(None, {input_name: img_data})
    
    # 4. Format Result
    probs = raw_result[0][0]
    idx = np.argmax(probs)
    
    return {
        "prediction": CLASSES[idx],
        "confidence": float(np.max(probs))
    }
