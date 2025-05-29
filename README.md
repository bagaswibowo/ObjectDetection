# Object Detection CCTV

Aplikasi web untuk deteksi objek real-time menggunakan CCTV feed dengan kemampuan deteksi plat nomor kendaraan.

## 🚀 Fitur Utama

- **Deteksi Objek Real-time**
  - Deteksi berbagai objek: orang, mobil, motor, sepeda, truk, bus, kucing, anjing
  - Akurasi tinggi menggunakan model YOLO
  - Visualisasi bounding box dan label real-time

- **Deteksi Plat Nomor**
  - Ekstraksi plat nomor kendaraan
  - OCR untuk membaca teks plat nomor
  - Dukungan format plat nomor Indonesia

- **Antarmuka Web**
  - Desain responsif dan modern
  - Update real-time jumlah objek terdeteksi
  - Visualisasi statistik deteksi
  - Dukungan untuk stream HLS (m3u8)

## 🛠️ Teknologi

- **Backend**
  - Flask (Web Framework)
  - OpenCV (Image Processing)
  - YOLO (Object Detection)
  - EasyOCR (Text Recognition)
  - PyTorch (Deep Learning)

- **Frontend**
  - HTML5
  - CSS3
  - JavaScript
  - Bootstrap

## 📋 Prasyarat

- Python 3.8+
- pip (Python package manager)
- Webcam atau CCTV feed
- Koneksi internet

## 🚀 Cara Menjalankan

1. Clone repository:
```bash
git clone [URL_REPOSITORY]
cd ObjectDetection
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Jalankan aplikasi:
```bash
python app.py
```

4. Buka browser dan akses `http://localhost:8080`

## 🚀 Deployment

Aplikasi ini di-deploy menggunakan GitHub Actions ke Azure Web App. Setiap push ke branch `main` akan memicu proses deployment otomatis.

## 📁 Struktur Proyek

```