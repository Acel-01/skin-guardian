---
title: Skin Guardian AI
emoji: 🛡️
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
pinned: false
---

# Skin Guardian AI: Deep Learning for Skin Lesion Detection

Skin Guardian AI is a production-ready medical computer vision application designed to provide instant screening for common skin conditions. By leveraging Transfer Learning with a ResNet18 architecture, the system classifies skin lesions into five diagnostic categories with high accuracy, bridging the gap between clinical research and accessible web-based healthcare tools.

## Try It Live

- **Frontend**: [https://skin-guardian.streamlit.app](https://skin-guardian.streamlit.app)
- **Backend API**: [https://acel-01-skin-guardian.hf.space/docs](https://acel-01-skin-guardian.hf.space/docs)

## Project Overview

Medical imaging data has increased tremendously, making manual inspection a bottleneck for early diagnosis. Skin Guardian AI aims to solve this by providing a high-performance screening tool that can be used from any device.

- **Goal**: Automated classification of skin conditions to support early detection
- **Target Conditions**: Arsenic, Eczema, Melanoma, Normal, and Psoriasis
- **Technology**: PyTorch, ONNX Runtime, FastAPI, Streamlit, and Docker

## Technical Architecture

This project follows a modern microservices architecture to ensure scalability and portability.

- **Backend (FastAPI)**: Serves the model using ONNX Runtime for high-speed inference without the overhead of heavy deep learning frameworks
- **Frontend (Streamlit)**: A user-friendly interface for image uploading and real-time visualization of diagnostic results
- **Model Format (ONNX)**: The PyTorch model is exported to ONNX to allow cross-platform compatibility and optimized performance on CPU-based cloud servers

## Model & Data

- **Architecture**: ResNet18 (Transfer Learning)
- **Model Performance**: Achieved a validation accuracy of 91.87%
- **Dataset**: Custom skin lesion dataset split into Training and Validation sets
- **Preprocessing**: Normalization using ImageNet statistics and 224×224 resizing

## Local Setup (Development)

This project uses `uv` for lightning-fast Python package management and reproducible environments.

### Prerequisites

- Python 3.12+
- `uv` installed: `curl -LsSf https://astral.sh/uv/install.sh | sh`

### Installation

```bash
# Clone the repository
git clone https://github.com/Acel-01/skin-guardian.git
cd skin-guardian

# Create virtual environment and install dependencies
uv sync

# Run the Backend (Terminal 1)
uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Run the Frontend (Terminal 2)
uv run streamlit run streamlit_app.py
```

## Containerization (Docker)

The project is fully containerized for seamless deployment.

```bash
# Build and run with Docker Compose
docker-compose up --build
```

- **Backend**: http://localhost:8000/docs (Swagger UI)
- **Frontend**: http://localhost:8501

## Deployment

- **Backend**: Hosted on Hugging Face Spaces using Docker
- **Frontend**: Hosted on Streamlit Community Cloud
- **CI/CD**: GitHub Actions are used to automatically sync the repository with Hugging Face

## Repository Structure

```
.
├── .github/workflows/           # CI/CD sync for Hugging Face
├── main.py                      # FastAPI backend logic
├── streamlit_app.py             # Streamlit frontend UI
├── skin_guardian.onnx           # Model architecture (LFS)
├── skin_guardian.onnx.data      # Model weights (LFS)
├── Dockerfile                   # Multi-service container config
├── docker-compose.yml           # Docker Compose configuration
├── pyproject.toml               # uv configuration
├── requirements.txt             # Fallback for Streamlit Cloud
├── skin_guardian.ipynb          # Jupyter Notebook (Training & EDA)
├── LICENSE
└── README.md
```
