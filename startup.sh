#!/bin/bash

# Aktifkan virtual environment
source /home/site/wwwroot/antenv/bin/activate

# Pre-download model YOLO
python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"

# Jalankan aplikasi dengan Gunicorn
gunicorn --bind=0.0.0.0 --timeout 600 --workers 4 --threads 2 wsgi:app 