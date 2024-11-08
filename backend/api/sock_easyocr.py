import cv2
import mediapipe as mp
import easyocr
import time
from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
import threading

# Initialize Flask and SocketIO
app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1,
                       min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Initialize EasyOCR Reader
reader = easyocr.Reader(['en'])

# OCR Timing and Position Tracking Variables
ocr_interval = 0.5
last_ocr_time = time.time()
prev_cx, prev_cy = None, None

# Define fingertip index for the index finger
INDEX_FINGER_TIP = 8

capture_url = "http://192.168.79.51:8080/video"

# SocketIO event for character transmission
@socketio.on('connect')
def handle_connect():
    print("Client connected")

@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected")

def detect_character():
    global last_ocr_time, prev_cx, prev_cy
    video_capture = cv2.VideoCapture(capture_url)

    while video_capture.isOpened():
        success, frame = video_capture.read()
        if not success:
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                h, w, _ = frame.shape
                fingertip_x = int(hand_landmarks.landmark[INDEX_FINGER_TIP].x * w)
                fingertip_y = int(hand_landmarks.landmark[INDEX_FINGER_TIP].y * h)

                cv2.circle(frame, (fingertip_x, fingertip_y), 10, (255, 0, 255), cv2.FILLED)

                current_time = time.time()
                if (current_time - last_ocr_time > ocr_interval) and ((fingertip_x, fingertip_y) != (prev_cx, prev_cy)):
                    box_width, box_height, y_offset = 20, 30, 10
                    x1 = max(fingertip_x - box_width // 2, 0)
                    y1 = max(fingertip_y - box_height - y_offset, 0)
                    x2 = min(fingertip_x + box_width // 2, frame.shape[1])
                    y2 = min(fingertip_y - y_offset, frame.shape[0])
                    fingertip_region = frame[y1:y2, x1:x2]

                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    fingertip_region_gray = cv2.cvtColor(fingertip_region, cv2.COLOR_BGR2GRAY)
                    _, fingertip_thresh = cv2.threshold(fingertip_region_gray, 130, 255, cv2.THRESH_BINARY_INV)

                    ocr_results = reader.readtext(fingertip_thresh, detail=1,
                                                  allowlist='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789')
                    for result in ocr_results:
                        _, detected_char, confidence = result
                        if confidence > 0.7:
                            socketio.emit('ocr_result', detected_char[-1])
                            print(f"Detected Character: {detected_char[-1]}")

                    last_ocr_time = current_time
                    prev_cx, prev_cy = fingertip_x, fingertip_y

        cv2.imshow("Finger OCR", frame)
        if 'fingertip_region' in locals():
            cv2.imshow("Fingertip Region", fingertip_thresh)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

@socketio.on('start_ocr')
def handle_start_ocr():
    threading.Thread(target=detect_character).start()

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)