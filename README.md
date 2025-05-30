# Object Detection App

Aplikasi deteksi objek menggunakan YOLOS dan EasyOCR untuk mendeteksi kendaraan, orang, dan hewan dari stream CCTV.

## Fitur

- Deteksi objek real-time menggunakan model YOLOS
- Deteksi plat nomor kendaraan menggunakan EasyOCR
- Visualisasi statistik deteksi
- Export data ke Excel
- Antarmuka web yang responsif
- Dukungan untuk stream CCTV HLS

## Persyaratan Sistem

- Python 3.9 atau lebih baru
- OpenCV
- PyTorch
- Flask
- EasyOCR
- Transformers (Hugging Face)

## Instalasi

1. Clone repository:
```bash
git clone https://github.com/bagaswibowo/ObjectDetection.git
cd ObjectDetection
```

2. Buat virtual environment (opsional tapi direkomendasikan):
```bash
python -m venv venv
source venv/bin/activate  # Untuk macOS/Linux
# atau
.\venv\Scripts\activate  # Untuk Windows
```

3. Instal dependensi:
```bash
pip install -r requirements.txt
```

## Menjalankan Aplikasi

1. Aktifkan virtual environment (jika menggunakan):
```bash
source venv/bin/activate  # Untuk macOS/Linux
# atau
.\venv\Scripts\activate  # Untuk Windows
```

2. Jalankan aplikasi:
```bash
python app.py
```

3. Buka browser dan akses:
```
http://localhost:5000
```

## Penggunaan

1. Masukkan URL stream CCTV di kolom input
2. Klik "Start Detection" untuk memulai deteksi
3. Gunakan "Stop Detection" untuk menghentikan deteksi
4. Lihat statistik di tab "Statistics"
5. Export data ke Excel menggunakan tombol "Export Data"

## Objek yang Dapat Dideteksi

- Mobil
- Motor
- Bus
- Truk
- Orang
- Kucing
- Anjing

## Teknologi yang Digunakan

- Flask: Web framework
- YOLOS: Model deteksi objek
- EasyOCR: OCR untuk deteksi plat nomor
- OpenCV: Pemrosesan gambar
- PyTorch: Deep learning framework
- Plotly: Visualisasi data
- Pandas: Manipulasi data

## Struktur Proyek

```
ObjectDetection/
├── app.py              # Aplikasi utama
├── requirements.txt    # Dependensi Python
├── templates/          # Template HTML
│   └── index.html      # Halaman utama
└── README.md          # Dokumentasi
```

## Troubleshooting

1. Jika ada error "ModuleNotFoundError":
   - Pastikan semua dependensi terinstal dengan benar
   - Coba jalankan `pip install -r requirements.txt` lagi

2. Jika stream CCTV tidak muncul:
   - Periksa URL stream
   - Pastikan format URL benar (HLS/m3u8)

3. Jika deteksi tidak berjalan:
   - Periksa koneksi internet
   - Pastikan model YOLOS dan EasyOCR terunduh dengan benar

## Kontribusi

Silakan buat pull request untuk kontribusi. Untuk perubahan besar, buka issue terlebih dahulu untuk mendiskusikan perubahan yang diinginkan.

## Lisensi

[MIT](https://choosealicense.com/licenses/mit/)