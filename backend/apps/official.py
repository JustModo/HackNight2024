import cv2
import mediapipe as mp
import pytesseract
import time

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2,
                       min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

# Initialize variables for optimization
last_ocr_time = time.time()
ocr_interval = 0.3  # OCR every 0.3 seconds
prev_cx, prev_cy = None, None  # Previous coordinates for comparison
detected_text = ""

# Define the tip landmarks for each finger (thumb, index, middle, ring, pinky)
finger_tips = [4, 8, 12, 16, 20]


def find_hands(img, draw=True):
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            if draw:
                for i in [8]:  # Only index fingertip for marking
                    landmark = hand_landmarks.landmark[i]
                    h, w, _ = img.shape
                    cx, cy = int(landmark.x * w), int(landmark.y * h)
                    cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)
    return img, results


def find_position(img, results, hand_no=0):
    lm_list = []
    if results.multi_hand_landmarks:
        my_hand = results.multi_hand_landmarks[hand_no]
        for id, lm in enumerate(my_hand.landmark):
            h, w, c = img.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            lm_list.append([id, cx, cy])
    return lm_list


# Start video capture
capture_url = "http://192.168.79.51:8080/video"
video_capture = cv2.VideoCapture(capture_url)

while True:
    success, frame = video_capture.read()
    if not success:
        break

    # Detect hands in the frame and get landmark positions
    frame, results = find_hands(frame)
    landmarks = find_position(frame, results)

    if len(landmarks) != 0:
        # Detect if index finger is up and closer to the camera
        if landmarks[finger_tips[1]][2] < landmarks[finger_tips[1] - 2][2]:  # Index finger is up
            tip_id = finger_tips[1]  # Index finger tip
            cx, cy = landmarks[tip_id][1], landmarks[tip_id][2]

            # Check if enough time has passed and position has changed
            current_time = time.time()
            if current_time - last_ocr_time > ocr_interval and (cx != prev_cx or cy != prev_cy):
                # Define a narrow bounding box around the fingertip
                box_width = 20  # Narrower box for single character
                box_height = 30
                x1, y1 = max(cx - box_width // 2,
                             0), max(cy - box_height - 10, 0)
                x2, y2 = min(cx + box_width // 2,
                             frame.shape[1]), min(cy - 10, frame.shape[0])

                # Draw the bounding boxqq
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

                # Extract and resize the region for OCR
                fingertip_region = frame[y1:y2, x1:x2]
                fingertip_region_resized = cv2.resize(
                    fingertip_region, (box_width, box_height))

                # Run Tesseract OCR on the region, focus on single character
                text = pytesseract.image_to_string(
                    fingertip_region_resized, config='--psm 10 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz')

                # Add character to the detected text if it's a single alphanumeric character
                if len(text.strip()) == 1:
                    detected_text += text.strip()

                # Display accumulated detected text
                # cv2.putText(frame, detected_text, (50, 50),
                #             cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                print(detected_text)

                # Update the last OCR time and previous coordinates
                last_ocr_time = current_time
                prev_cx, prev_cy = cx, cy

    # Show the video frame
    cv2.imshow("Finger OCR", frame)

    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and destroy all OpenCV windows
video_capture.release()
cv2.destroyAllWindows()
