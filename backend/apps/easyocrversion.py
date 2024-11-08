import cv2
import mediapipe as mp
import easyocr
import time

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1,
                       min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

# Initialize EasyOCR Reader
reader = easyocr.Reader(['en'])  # English language

# OCR Timing and Position Tracking Variables
ocr_interval = 0.5  # Time interval for OCR
last_ocr_time = time.time()
prev_cx, prev_cy = None, None
detected_text = ""

# Define fingertip index for the index finger
INDEX_FINGER_TIP = 8

# Start video capture from IP camera
capture_url = "http://192.168.79.51:8080/video"
video_capture = cv2.VideoCapture(capture_url)

while video_capture.isOpened():
    success, frame = video_capture.read()
    if not success:
        break

    # Convert frame to RGB for hand detection
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Get fingertip coordinates of the index finger
            h, w, _ = frame.shape
            fingertip_x = int(hand_landmarks.landmark[INDEX_FINGER_TIP].x * w)
            fingertip_y = int(hand_landmarks.landmark[INDEX_FINGER_TIP].y * h)

            # Draw fingertip marker on the frame
            cv2.circle(frame, (fingertip_x, fingertip_y),
                       10, (255, 0, 255), cv2.FILLED)

            # Perform OCR if time interval has passed and position has changed
            current_time = time.time()
            if (current_time - last_ocr_time > ocr_interval) and ((fingertip_x, fingertip_y) != (prev_cx, prev_cy)):
                # Set separate width and height for the bounding box
                box_width = 20   # Width of the bounding box
                box_height = 30  # Height of the bounding box
                y_offset = 10    # Vertical offset for positioning the box slightly above the fingertip

                # Calculate the top-left (x1, y1) and bottom-right (x2, y2) coordinates of the bounding box
                x1 = max(fingertip_x - box_width // 2, 0)
                y1 = max(fingertip_y - box_height - y_offset, 0)
                x2 = min(fingertip_x + box_width // 2, frame.shape[1])
                y2 = min(fingertip_y - y_offset, frame.shape[0])
                fingertip_region = frame[y1:y2, x1:x2]

                # Draw the bounding box for OCR
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

                # Convert region to grayscale and threshold for better OCR results
                fingertip_region_gray = cv2.cvtColor(
                    fingertip_region, cv2.COLOR_BGR2GRAY)
                _, fingertip_thresh = cv2.threshold(
                    fingertip_region_gray, 130, 255, cv2.THRESH_BINARY_INV)

                # Run OCR with confidence levels
                ocr_results = reader.readtext(
                    fingertip_thresh, detail=1, allowlist='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789')

                # Process each detected result
                for result in ocr_results:
                    _, detected_char, confidence = result  # Unpack result tuple

                    # Filter by confidence and ensure single-character detection
                    # Adjust confidence threshold as needed

                    # print(f"Detected Text: {
                    #     detected_char}, Confidence: {confidence:.2f}")

                    if confidence > 0.7:
                        detected_text += detected_char[-1]
                        print(detected_text)  # Print updated detected text

                # Update time and fingertip position
                last_ocr_time = current_time
                prev_cx, prev_cy = fingertip_x, fingertip_y

    # Show the frame with fingertip marker and bounding box
    cv2.imshow("Finger OCR", frame)

    # Optionally, show the fingertip region for debugging
    if 'fingertip_region' in locals():
        cv2.imshow("Fingertip Region", fingertip_thresh)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
video_capture.release()
cv2.destroyAllWindows()
