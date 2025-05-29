#!/bin/bash

# Buat virtual environment jika belum ada
if [ ! -d "/home/site/wwwroot/antenv" ]; then
    python -m venv /home/site/wwwroot/antenv
fi

# Aktifkan virtual environment
source /home/site/wwwroot/antenv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Pre-download model YOLO
python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"

# Jalankan aplikasi dengan Gunicorn
gunicorn --bind=0.0.0.0 --timeout 600 --workers 4 --threads 2 wsgi:app 