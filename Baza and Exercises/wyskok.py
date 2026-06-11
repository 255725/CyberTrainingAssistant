import cv2
import numpy as np
import mediapipe as mp
import time

AKTYWNY = False

def zatrzymaj_trening():
    global AKTYWNY
    AKTYWNY = False

def generuj_obraz_wyskok():
    global AKTYWNY
    AKTYWNY = True

    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils
    pose_cam1 = mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7)
    pose_cam2 = mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7)

    counter = 0
    stage = None
    feedback = "Rozpocznij cwiczenie"

    baseline_hip_y = 0
    cm_per_pixel = 0
    is_calibrated = False
    calibration_start_time = 0
    max_flight_y = 0
    last_jump_height = 0.0
    USER_HEIGHT_CM = 175.0

    cap1 = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap2 = cv2.VideoCapture(1, cv2.CAP_DSHOW)

    for cap in [cap1, cap2]:
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    try:
        while AKTYWNY:
            success1, img1 = cap1.read()
            success2, img2 = cap2.read()

            if not success1 or not success2:
                print("Blad pobierania obrazu!")
                break

            imgRGB1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
            results1 = pose_cam1.process(imgRGB1)
            imgRGB2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
            results2 = pose_cam2.process(imgRGB2)

            active_results = results1
            active_h, active_w, _ = img1.shape

            if results1.pose_landmarks:
                mp_drawing.draw_landmarks(img1, results1.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            if results2.pose_landmarks:
                mp_drawing.draw_landmarks(img2, results2.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            if active_results and active_results.pose_landmarks:
                landmarks = active_results.pose_landmarks.landmark

                nose_y_pixel = int(landmarks[mp_pose.PoseLandmark.NOSE.value].y * active_h)
                hip_y_pixel = int(landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y * active_h)
                ankle_y_pixel = int(landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y * active_h)

                nose_y = landmarks[mp_pose.PoseLandmark.NOSE.value].y
                left_wrist_y = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y
                right_wrist_y = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y

                if not is_calibrated:
                    if left_wrist_y < nose_y and right_wrist_y < nose_y:
                        if calibration_start_time == 0:
                            calibration_start_time = time.time()

                        elapsed_time = time.time() - calibration_start_time
                        time_left = max(1, 3 - int(elapsed_time))

                        if elapsed_time >= 3.0:
                            pixel_height = ankle_y_pixel - nose_y_pixel
                            if pixel_height > 200:
                                baseline_hip_y = hip_y_pixel
                                cm_per_pixel = USER_HEIGHT_CM / pixel_height
                                is_calibrated = True
                                stage = "standing"
                                feedback = "Skalibrowano! Mozesz skakac."
                            else:
                                feedback = "Blad! Odsun sie od kamery."
                                calibration_start_time = 0
                        else:
                            feedback = f"Trzymaj rece w gorze... {time_left}"
                    else:
                        calibration_start_time = 0
                        feedback = "Unies OBIE rece do gory by skalibrowac"
                else:
                    displacement = baseline_hip_y - hip_y_pixel

                    if displacement < -30:
                        stage = "squat"
                        feedback = "Dobre zejscie. Odbij sie!"
                    elif displacement > 20 and stage == "squat":
                        stage = "air"
                        max_flight_y = displacement
                    elif stage == "air":
                        if displacement > max_flight_y:
                            max_flight_y = displacement
                        if displacement < 10:
                            stage = "standing"
                            counter += 1
                            last_jump_height = max_flight_y * cm_per_pixel
                            feedback = "Swietne ladowanie! Skacz znowu."
                            max_flight_y = 0

            combined_img = np.hstack((img1, img2))
            comb_h, comb_w, _ = combined_img.shape

            cv2.rectangle(combined_img, (0, 0), (comb_w, 100), (0, 0, 0), -1)
            cv2.putText(combined_img, f"POWTORZENIA: {counter}", (25, 45), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3,
                        cv2.LINE_AA)

            if is_calibrated:
                cv2.putText(combined_img, f"OSTATNI SKOK: {last_jump_height:.1f} cm", (25, 85), cv2.FONT_HERSHEY_SIMPLEX,
                            0.9, (255, 255, 0), 2, cv2.LINE_AA)

            cv2.putText(combined_img, f"TRENER: {feedback}", (550, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2,
                        cv2.LINE_AA)

            ret, buffer = cv2.imencode('.jpg', combined_img)
            if not ret:
                continue
            
            # Konwersja na bajty
            frame_bytes = buffer.tobytes()

            # "Wyrzucenie" klatki do serwera FastAPI
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    finally:            
        cap1.release()
        cap2.release()
        AKTYWNY = False
        