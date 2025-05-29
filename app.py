from flask import Flask, render_template, request, Response, jsonify, send_file
import cv2
import numpy as np
from PIL import Image
import torch
import threading
import queue
import easyocr
from transformers import YolosImageProcessor, YolosForObjectDetection
import time
from collections import Counter, defaultdict
import os
import pandas as pd
from datetime import datetime
import json
import plotly
import plotly.express as px
from io import BytesIO

app = Flask(__name__)

# Inisialisasi model dan komponen deteksi
model = YolosForObjectDetection.from_pretrained('hustvl/yolos-tiny')
image_processor = YolosImageProcessor.from_pretrained("hustvl/yolos-tiny")
reader = easyocr.Reader(['id'])

label_translation = {
    'bicycle': 'sepeda',
    'car': 'mobil',
    'motorcycle': 'motor',
    'bus': 'bus',
    'truck': 'truk',
    'person': 'Orang',
    'human': 'Manusia',
    'cat': 'Kucing',
    'dog': 'Anjing'
}

# Queue untuk menyimpan frame
frame_queue = queue.Queue(maxsize=2)
current_stream_url = None
detection_thread = None
stop_detection = False
detected_objects = Counter()  # Menggunakan Counter untuk menghitung jumlah objek

# Menyimpan riwayat deteksi per 10 detik
detection_history = defaultdict(lambda: defaultdict(int))
last_minute = None

def deteksi_plat(frame, vehicle_area):
    """Mendeteksi plat nomor kendaraan pada frame yang diberikan."""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    enhanced_gray = cv2.equalizeHist(gray)
    edges = cv2.Canny(enhanced_gray, 100, 200)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        plate_area = w * h

        if plate_area <= vehicle_area / 10:
            aspect_ratio = w / h
            if 2 < aspect_ratio < 5:  # Rasio plat nomor umumnya antara 2:1 hingga 5:1
                plate_region = frame[y:y+h, x:x+w]
                result = reader.readtext(plate_region)

                if result:
                    plat_text = " ".join([detection[1] for detection in result])
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(frame, plat_text, (x, y - 10), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    return frame

def generate_frames():
    while True:
        if not frame_queue.empty():
            frame = frame_queue.get()
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        time.sleep(0.1)  # Tambahkan delay kecil untuk mengurangi beban CPU

def detection_worker(hls_url):
    global stop_detection, detected_objects, last_minute
    cap = cv2.VideoCapture(hls_url)
    
    if not cap.isOpened():
        print("Error: Tidak dapat membuka stream CCTV.")
        return

    while not stop_detection:
        ret, frame = cap.read()
        if not ret:
            print("Error: Tidak bisa membaca frame.")
            time.sleep(1)
            continue

        # Update riwayat per 10 detik
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if not last_minute or (datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S') - 
                             datetime.strptime(last_minute, '%Y-%m-%d %H:%M:%S')).total_seconds() >= 10:
            for obj, count in detected_objects.items():
                detection_history[current_time][obj] = count
            last_minute = current_time

        # Ubah frame ke format PIL Image
        image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        inputs = image_processor(images=image, return_tensors="pt")
        outputs = model(**inputs)

        target_sizes = torch.tensor([image.size[::-1]])
        results = image_processor.post_process_object_detection(
            outputs, threshold=0.8, target_sizes=target_sizes)[0]

        # Reset detected objects setiap frame
        detected_objects.clear()

        for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
            box = [round(i, 2) for i in box.tolist()]
            if score > 0.85 and model.config.id2label[label.item()] in ('car', 'motorcycle', 'truck', 'bus', 'person', 'human', 'cat', 'dog'):
                x1, y1, x2, y2 = map(int, box)
                vehicle_area = (x2 - x1) * (y2 - y1)
                cropped_frame = frame[y1:y2, x1:x2]

                # Deteksi plat nomor untuk kendaraan
                if model.config.id2label[label.item()] in ('car', 'motorcycle', 'truck', 'bus'):
                    cropped_frame = deteksi_plat(cropped_frame, vehicle_area)

                # Tambahkan objek ke Counter
                obj_label = label_translation.get(model.config.id2label[label.item()], label.item())
                detected_objects[obj_label] += 1

                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                cv2.putText(frame, f"{obj_label}: {round(score.item(), 3)}", 
                            (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

        if not frame_queue.full():
            frame_queue.put(frame)

    cap.release()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_detection', methods=['POST'])
def start_detection():
    global current_stream_url, detection_thread, stop_detection
    
    hls_url = request.form.get('rtsp_url')
    if not hls_url:
        return jsonify({'error': 'URL stream tidak ditemukan'}), 400

    # Stop deteksi sebelumnya jika ada
    if detection_thread and detection_thread.is_alive():
        stop_detection = True
        detection_thread.join()

    # Reset variabel
    stop_detection = False
    current_stream_url = hls_url
    
    # Mulai thread deteksi baru
    detection_thread = threading.Thread(target=detection_worker, args=(hls_url,))
    detection_thread.start()
    
    return jsonify({'message': 'Deteksi dimulai'})

@app.route('/stop_detection', methods=['POST'])
def stop_detection_route():
    global stop_detection
    stop_detection = True
    return jsonify({'message': 'Deteksi dihentikan'})

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_detected_objects')
def get_detected_objects():
    return jsonify({
        'objects': dict(detected_objects),
        'total': sum(detected_objects.values())
    })

@app.route('/get_detection_history')
def get_detection_history():
    times = list(detection_history.keys())
    data = []
    
    for time in times:
        time_data = detection_history[time]
        total = sum(time_data.values())
        data.append({
            'timestamp': time,
            'objects': dict(time_data),
            'total': total
        })
    
    return jsonify(data)

@app.route('/get_statistics')
def get_statistics():
    # Buat DataFrame dari riwayat deteksi
    df = pd.DataFrame.from_dict(detection_history, orient='index')
    
    # Buat grafik line menggunakan Plotly
    fig_line = px.line(df, title='Statistik Deteksi per 10 Detik')
    fig_line.update_layout(
        xaxis_title='Waktu',
        yaxis_title='Jumlah Objek',
        legend_title='Jenis Objek'
    )
    
    return jsonify({
        'line_graph': json.loads(fig_line.to_json())
    })

@app.route('/export_data')
def export_data():
    # Buat DataFrame dari riwayat deteksi
    df = pd.DataFrame.from_dict(detection_history, orient='index')
    
    # Buat file Excel di memori
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Deteksi')
    
    output.seek(0)
    
    # Kirim file
    return send_file(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name=f'detection_history_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
    )

@app.route('/filter_objects', methods=['POST'])
def filter_objects():
    data = request.get_json()
    object_type = data.get('object_type')
    
    if not object_type:
        return jsonify({'error': 'Jenis objek tidak ditentukan'}), 400
    
    # Filter riwayat berdasarkan jenis objek
    filtered_history = {
        minute: counts.get(object_type, 0)
        for minute, counts in detection_history.items()
    }
    
    return jsonify({
        'object_type': object_type,
        'history': filtered_history
    })

@app.route('/get_object_summary')
def get_object_summary():
    # Buat DataFrame dari riwayat deteksi
    df = pd.DataFrame.from_dict(detection_history, orient='index')
    
    # Hitung total untuk setiap objek
    total_counts = df.sum()
    total_all = total_counts.sum()
    
    # Hitung persentase untuk setiap objek
    percentages = (total_counts / total_all * 100).round(2)
    
    # Buat dictionary untuk response
    summary = {
        'totals': total_counts.to_dict(),
        'percentages': percentages.to_dict(),
        'total_all': int(total_all)
    }
    
    return jsonify(summary)

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy"}), 200

# Untuk Vercel
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port) 