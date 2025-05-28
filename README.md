# Object Detection CCTV

Aplikasi web untuk deteksi objek real-time menggunakan CCTV feed.

## Fitur

- Deteksi objek real-time (orang, mobil, motor, sepeda, truk, bus, kucing, anjing)
- Deteksi plat nomor kendaraan
- Antarmuka web responsif
- Update real-time jumlah objek terdeteksi
- Dukungan untuk stream HLS (m3u8)

## Teknologi

- Flask
- OpenCV
- YOLOS (You Only Look Once)
- EasyOCR
- PyTorch
- Vercel (Deployment)

## Cara Menjalankan

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Jalankan aplikasi:
```bash
python app.py
```

3. Buka browser dan akses `http://localhost:8080`

## Deployment

Aplikasi ini sudah dikonfigurasi untuk deployment di Vercel. Untuk deploy:

1. Push kode ke repository GitHub
2. Import proyek di Vercel
3. Deploy

## Struktur Proyek

```
.
├── app.py              # Aplikasi Flask utama
├── wsgi.py            # Entry point untuk Vercel
├── requirements.txt   # Dependencies
├── runtime.txt        # Versi Python
├── vercel.json        # Konfigurasi Vercel
└── templates/         # Template HTML
    └── index.html     # Halaman utama
```

## Lisensi

MIT 