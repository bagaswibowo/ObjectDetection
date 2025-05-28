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

Aplikasi ini dapat di-deploy di berbagai platform hosting Python seperti:
- Heroku
- PythonAnywhere
- DigitalOcean
- AWS
- Google Cloud Platform

Untuk deployment, pastikan untuk:
1. Mengatur environment variables yang diperlukan
2. Mengkonfigurasi web server (seperti Nginx atau Apache)
3. Menggunakan WSGI server (seperti Gunicorn atau uWSGI)

## 📁 Struktur Proyek

```
.
├── app.py              # Aplikasi Flask utama
├── wsgi.py            # Entry point WSGI
├── requirements.txt   # Dependencies
├── runtime.txt        # Versi Python
└── templates/         # Template HTML
    └── index.html     # Halaman utama
```

## 🤝 Kontribusi

Kontribusi selalu diterima! Untuk berkontribusi:

1. Fork repository
2. Buat branch fitur (`git checkout -b fitur-baru`)
3. Commit perubahan (`git commit -m 'Menambahkan fitur baru'`)
4. Push ke branch (`git push origin fitur-baru`)
5. Buat Pull Request

## 📝 Lisensi

Proyek ini dilisensikan di bawah Lisensi MIT - lihat file [LICENSE](LICENSE) untuk detailnya.

## 📞 Kontak

Untuk pertanyaan atau dukungan, silakan buat issue di repository ini. 