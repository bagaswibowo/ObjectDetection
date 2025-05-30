# Object Detection CCTV

Aplikasi web untuk deteksi objek real-time menggunakan CCTV feed dengan kemampuan deteksi plat nomor kendaraan, dibangun dengan Flask dan PyTorch.

## 🚀 Fitur Utama

- **Deteksi Objek Real-time**
  - Deteksi berbagai objek: orang, mobil, motor, sepeda, truk, bus, kucing, anjing
  - Menggunakan model YOLOS (You Only Look at One Sequence) dari Hugging Face
  - Visualisasi bounding box dan label real-time
  - Terjemahan label ke bahasa Indonesia

- **Deteksi Plat Nomor**
  - Ekstraksi plat nomor kendaraan otomatis
  - OCR menggunakan EasyOCR untuk membaca teks plat nomor
  - Dukungan format plat nomor Indonesia

- **Antarmuka Web Modern**
  - Desain responsif dengan Bootstrap 5
  - Update real-time jumlah objek terdeteksi
  - Visualisasi statistik deteksi dengan Plotly
  - Dashboard monitoring real-time
  - Dukungan untuk stream HLS (m3u8) dan RTSP

- **Fitur Lanjutan**
  - Riwayat deteksi dan statistik
  - Export data ke Excel
  - Filter objek berdasarkan jenis
  - Monitoring kesehatan aplikasi

## 🛠️ Teknologi

- **Backend**
  - Flask 2.0.1 (Web Framework)
  - OpenCV 4.5.5 (Image Processing)
  - PyTorch 1.13.1 & Torchvision 0.14.1 (Deep Learning)
  - Transformers 4.19.2 (YOLOS Model)
  - EasyOCR 1.4.1 (Text Recognition)
  - Gunicorn 20.1.0 (WSGI Server)

- **Frontend**
  - HTML5, CSS3, JavaScript
  - Bootstrap 5.1.3 (UI Framework)
  - Font Awesome 6.0 (Icons)
  - Plotly.js (Data Visualization)

- **Machine Learning**
  - YOLOS-tiny model dari Hugging Face
  - YolosImageProcessor untuk preprocessing
  - Real-time object detection pipeline

## 📋 Prasyarat

- Python 3.9+ (direkomendasikan Python 3.9)
- pip (Python package manager)
- Webcam, CCTV feed, atau URL stream (HLS/RTSP)
- Koneksi internet (untuk download model pertama kali)
- Minimal 4GB RAM (untuk model PyTorch dan OpenCV)

## 🚀 Instalasi dan Menjalankan Lokal

### 1. Clone Repository
```bash
git clone https://github.com/username/ObjectDetection.git
cd ObjectDetection
```

### 2. Setup Environment (Direkomendasikan)
```bash
# Buat virtual environment
python3 -m venv .venv

# Aktifkan virtual environment
# macOS/Linux:
source .venv/bin/activate
# Windows:
# .venv\Scripts\activate
```

### 3. Install Dependencies
```bash
# Upgrade pip terlebih dahulu
pip install --upgrade pip

# Install semua dependencies
pip install -r requirements.txt
```

### 4. Jalankan Aplikasi
```bash
# Untuk development
python3 app.py

# Atau menggunakan Gunicorn (untuk production)
gunicorn --bind 0.0.0.0:8000 wsgi:app
```

### 5. Akses Aplikasi
Buka browser dan akses:
- Development: `http://localhost:5000`
- Production: `http://localhost:8000`

## 🌐 Deployment ke Production

### Azure App Service (Direkomendasikan)

Aplikasi ini dikonfigurasi untuk deployment otomatis ke Azure App Service menggunakan GitHub Actions.

**Setup:**
1. Fork repository ini
2. Buat Azure App Service dengan Python 3.9 runtime
3. Konfigurasi GitHub Actions secrets:
   - `AZURE_WEBAPP_PUBLISH_PROFILE`
4. Push ke branch `main` akan otomatis trigger deployment

**Startup Command di Azure:**
```bash
apt-get update && apt-get install -y libgl1-mesa-glx libglib2.0-0 libsm6 libxext6 libxrender1 && source antenv/bin/activate && pip install -r requirements.txt && gunicorn --bind=0.0.0.0:8000 wsgi:app
```

### Server Linux Manual

1. **Setup Server:**
```bash
# Update sistem
sudo apt update && sudo apt upgrade -y

# Install Python dan dependencies
sudo apt install python3 python3-pip python3-venv -y

# Install system libraries untuk OpenCV
sudo apt install libgl1-mesa-glx libglib2.0-0 libsm6 libxext6 libxrender1 -y
```

2. **Deploy Aplikasi:**
```bash
# Clone ke server
git clone https://github.com/username/ObjectDetection.git
cd ObjectDetection

# Setup virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Jalankan dengan Gunicorn
gunicorn --workers 3 --bind 0.0.0.0:8000 wsgi:app
```

3. **Setup sebagai Service (systemd):**
```bash
# Buat file service
sudo nano /etc/systemd/system/objectdetection.service

# Reload dan enable
sudo systemctl daemon-reload
sudo systemctl enable objectdetection
sudo systemctl start objectdetection
```

### 🐳 Docker Deployment (Direkomendasikan)

Docker menyediakan cara yang konsisten dan mudah untuk men-deploy aplikasi di berbagai environment.

**Keuntungan Docker:**
- Konsistensi environment di semua platform
- Isolasi dependencies dan sistem
- Mudah untuk scaling dan maintenance
- Tidak perlu setup manual dependencies sistem

#### Quick Start dengan Docker

1. **Install Docker:**
```bash
# macOS (dengan Homebrew)
brew install docker docker-compose

# Ubuntu/Debian
sudo apt install docker.io docker-compose

# Atau install Docker Desktop dari docker.com
```

2. **Build dan Jalankan:**
```bash
# Clone repository
git clone https://github.com/username/ObjectDetection.git
cd ObjectDetection

# Build dan jalankan dengan Docker Compose
docker-compose up --build

# Atau jalankan di background
docker-compose up -d --build
```

3. **Akses Aplikasi:**
```
http://localhost:8000
```

#### Perintah Docker Berguna

```bash
# Lihat status container
docker-compose ps

# Lihat logs
docker-compose logs -f

# Stop aplikasi
docker-compose down

# Update aplikasi (rebuild image)
git pull
docker-compose down
docker-compose up --build -d

# Masuk ke container untuk debugging
docker-compose exec objectdetection bash

# Cleanup (hapus container, image, dan volume)
docker-compose down --rmi all --volumes
```

#### Build Manual (tanpa Docker Compose)

```bash
# Build image
docker build -t objectdetection-app .

# Jalankan container
docker run -d \
  --name objectdetection \
  -p 8000:8000 \
  --restart unless-stopped \
  objectdetection-app

# Lihat logs
docker logs -f objectdetection
```

#### Production dengan Docker

Untuk production, Anda bisa menggunakan:

1. **Docker Swarm:**
```bash
docker swarm init
docker stack deploy -c docker-compose.yml objectdetection
```

2. **Kubernetes:**
```bash
# Convert docker-compose ke Kubernetes manifests
kompose convert
kubectl apply -f .
```

3. **Cloud Container Services:**
   - Azure Container Instances (ACI)
   - AWS ECS/Fargate
   - Google Cloud Run
````