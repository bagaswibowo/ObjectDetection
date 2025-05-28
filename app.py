from flask import Flask, render_template, request, Response, jsonify
import cv2
import numpy as np
from PIL import Image
import torch
import threading
import queue
import easyocr
from transformers import YolosImageProcessor, YolosForObjectDetection
import time
from collections import Counter
import os
import logging
from functools import lru_cache

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cache untuk model dan processor
@lru_cache(maxsize=1)
def get_model():
    try:
        model = YolosForObjectDetection.from_pretrained('hustvl/yolos-tiny')
        return model
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        raise

@lru_cache(maxsize=1)
def get_processor():
    try:
        processor = YolosImageProcessor.from_pretrained("hustvl/yolos-tiny")
        return processor
    except Exception as e:
        logger.error(f"Error loading processor: {str(e)}")
        raise

@lru_cache(maxsize=1)
def get_ocr():
    try:
        reader = easyocr.Reader(['id'])
        return reader
    except Exception as e:
        logger.error(f"Error loading OCR: {str(e)}")
        raise

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

def process_frame(frame):
    """Process a single frame for object detection"""
    try:
        # Convert frame to PIL Image
        image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        
        # Get model and processor
        model = get_model()
        processor = get_processor()
        
        # Process image
        inputs = processor(images=image, return_tensors="pt")
        outputs = model(**inputs)

        target_sizes = torch.tensor([image.size[::-1]])
        results = processor.post_process_object_detection(
            outputs, threshold=0.8, target_sizes=target_sizes)[0]

        detected_objects = Counter()
        processed_frame = frame.copy()

        for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
            box = [round(i, 2) for i in box.tolist()]
            if score > 0.85 and model.config.id2label[label.item()] in ('car', 'motorcycle', 'truck', 'bus', 'person', 'human', 'cat', 'dog'):
                x1, y1, x2, y2 = map(int, box)
                vehicle_area = (x2 - x1) * (y2 - y1)
                
                # Process vehicle plate if applicable
                if model.config.id2label[label.item()] in ('car', 'motorcycle', 'truck', 'bus'):
                    processed_frame = detect_plate(processed_frame, (x1, y1, x2, y2), vehicle_area)

                # Add object to counter
                obj_label = label_translation.get(model.config.id2label[label.item()], label.item())
                detected_objects[obj_label] += 1

                # Draw bounding box
                cv2.rectangle(processed_frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                cv2.putText(processed_frame, f"{obj_label}: {round(score.item(), 3)}", 
                            (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

        return processed_frame, detected_objects

    except Exception as e:
        logger.error(f"Error processing frame: {str(e)}")
        return frame, Counter()

def detect_plate(frame, bbox, vehicle_area):
    """Detect license plate in the given bounding box"""
    try:
        x1, y1, x2, y2 = bbox
        roi = frame[y1:y2, x1:x2]
        
        # Convert to grayscale
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        enhanced_gray = cv2.equalizeHist(gray)
        edges = cv2.Canny(enhanced_gray, 100, 200)
        
        # Find contours
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Get OCR reader
        reader = get_ocr()
        
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            plate_area = w * h
            
            if plate_area <= vehicle_area / 10:
                aspect_ratio = w / h
                if 2 < aspect_ratio < 5:
                    plate_region = roi[y:y+h, x:x+w]
                    result = reader.readtext(plate_region)
                    
                    if result:
                        plat_text = " ".join([detection[1] for detection in result])
                        cv2.rectangle(frame, (x1 + x, y1 + y), (x1 + x + w, y1 + y + h), (0, 255, 0), 2)
                        cv2.putText(frame, plat_text, (x1 + x, y1 + y - 10), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        
        return frame
    except Exception as e:
        logger.error(f"Error detecting plate: {str(e)}")
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
    global stop_detection, detected_objects
    cap = cv2.VideoCapture(hls_url)
    
    if not cap.isOpened():
        print("Error: Tidak dapat membuka stream CCTV.")
        return

    while not stop_detection:
        ret, frame = cap.read()
        if not ret:
            print("Error: Tidak bisa membaca frame.")
            time.sleep(1)  # Tunggu sebentar sebelum mencoba lagi
            continue

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
                    cropped_frame = detect_plate(cropped_frame, (x1, y1, x2, y2), vehicle_area)

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

@app.route('/process_frame', methods=['POST'])
def process_frame_route():
    try:
        if 'frame' not in request.files:
            return jsonify({'error': 'No frame provided'}), 400
            
        # Read frame from request
        frame_file = request.files['frame']
        frame_array = np.frombuffer(frame_file.read(), np.uint8)
        frame = cv2.imdecode(frame_array, cv2.IMREAD_COLOR)
        
        if frame is None:
            return jsonify({'error': 'Invalid frame data'}), 400
            
        # Process frame
        processed_frame, detected_objects = process_frame(frame)
        
        # Encode processed frame
        _, buffer = cv2.imencode('.jpg', processed_frame)
        processed_frame_bytes = buffer.tobytes()
        
        return jsonify({
            'frame': processed_frame_bytes.decode('latin1'),
            'objects': dict(detected_objects),
            'total': sum(detected_objects.values())
        })
        
    except Exception as e:
        logger.error(f"Error in process_frame_route: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy'})

# Untuk Vercel
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port) 