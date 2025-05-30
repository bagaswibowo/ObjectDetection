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

## 📁 Struktur Proyek

```
ObjectDetection/
├── app.py                 # Aplikasi Flask utama
├── wsgi.py               # Entry point untuk Gunicorn
├── requirements.txt      # Dependencies Python
├── runtime.txt          # Runtime Python untuk Azure
├── README.md            # Dokumentasi proyek
├── .gitignore          # Git ignore rules
├── templates/          # Template HTML
│   └── index.html      # Template utama
├── .github/
│   └── workflows/
│       └── main.yml    # GitHub Actions untuk Azure App Service
└── static/             # File statis (jika ada)
    ├── css/
    ├── js/
    └── images/
```

## 🔧 Konfigurasi

### Environment Variables (Opsional)
```bash
# Untuk production
export FLASK_ENV=production
export FLASK_DEBUG=False

# Untuk development
export FLASK_ENV=development
export FLASK_DEBUG=True
```

### Model Configuration
- Model: `hustvl/yolos-tiny` dari Hugging Face
- Model akan didownload otomatis saat pertama kali dijalankan
- Cache model tersimpan di `~/.cache/huggingface/`

## 🧪 Testing

### Test Lokal
```bash
# Test import dependencies
python3 -c "import cv2, torch, transformers; print('All dependencies OK')"

# Test aplikasi
curl http://localhost:5000/health
```

### Troubleshooting Common Issues

1. **ImportError: libGL.so.1**
   ```bash
   # Ubuntu/Debian
   sudo apt install libgl1-mesa-glx libglib2.0-0
   
   # CentOS/RHEL
   sudo yum install mesa-libGL glib2
   ```

2. **ModuleNotFoundError: cv2**
   ```bash
   pip install opencv-python-headless==4.5.5.64
   ```

3. **ImportError: YolosImageProcessor**
   ```bash
   pip install transformers>=4.19.2
   ```

4. **Memory Issues**
   - Pastikan minimal 4GB RAM tersedia
   - Reduce worker count di Gunicorn
   - Gunakan swap jika diperlukan

## 📊 Performance

- **Model Load Time**: ~10-30 detik (pertama kali)
- **Detection Latency**: ~100-500ms per frame
- **Memory Usage**: ~2-4GB (tergantung ukuran batch)
- **Throughput**: ~2-10 FPS (tergantung hardware)

## 🔒 Security

- Aplikasi tidak menyimpan video atau gambar secara permanen
- Model berjalan offline setelah download pertama
- Gunakan HTTPS di production
- Implementasikan rate limiting jika diperlukan

## 🤝 Contributing

1. Fork repository
2. Buat feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit perubahan (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buat Pull Request

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.

## 📞 Contact

- Project Link: [https://github.com/username/ObjectDetection](https://github.com/username/ObjectDetection)
- Issues: [https://github.com/username/ObjectDetection/issues](https://github.com/username/ObjectDetection/issues)

## 🙏 Acknowledgments

- [Hugging Face](https://huggingface.co/) untuk model YOLOS
- [OpenCV](https://opencv.org/) untuk computer vision
- [Flask](https://flask.palletsprojects.com/) untuk web framework
- [PyTorch](https://pytorch.org/) untuk deep learning
- [EasyOCR](https://github.com/JaidedAI/EasyOCR) untuk text recognition