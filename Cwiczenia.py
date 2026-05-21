import cv2
import math
import numpy as np
import mediapipe as mp
import time

print("=======================================")
print("   CYBER ASYSTENT TRENINGU - MENU      ")
print("=======================================")
print("1. Uginanie przedramion (Biceps)")
print("2. Wznosy hantli bokiem (Barki)")
print("3. Wyskok pionowy (Dynamika i wysokosc)")
print("=======================================")

while True:
    wybor = input("Wybierz numer ćwiczenia (1-3): ").strip()
    if wybor in ["1", "2", "3"]:
        mode = int(wybor)
        break
    print("Nieprawidłowy wybór. Wpisz 1, 2 lub 3.")

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7)


def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    radians = math.atan2(c[1] - b[1], c[0] - b[0]) - math.atan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    if angle > 180.0:
        angle = 360 - angle
    return angle


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

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

while True:
    success, img = cap.read()
    if not success:
        print("Brak obrazu z kamery!")
        break

    h, w, c = img.shape
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)

    if results.pose_landmarks:
        mp_drawing.draw_landmarks(img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        landmarks = results.pose_landmarks.landmark

        if mode == 1:
            shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                        landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                     landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
            wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                     landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
            angle = calculate_angle(shoulder, elbow, wrist)

            if angle > 150:
                stage = "down"
                feedback = "Dobry wyprost! Unos ciezar."
            if angle < 40 and stage == "down":
                stage = "up"
                counter += 1
                feedback = "Swietnie! Opuszczaj powoli."
            if angle < 110 and stage == "up":
                feedback = "Pamietaj o PELNYM wyproscie rak!"

        elif mode == 2:
            hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
            shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                        landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                     landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
            angle = calculate_angle(hip, shoulder, elbow)

            if angle < 25:
                stage = "down"
                feedback = "Dobry opust. Unies rece w bok."
            if angle > 80 and stage == "down":
                stage = "up"
                counter += 1
                feedback = "Idealna wysokosc! Opusc powoli."
            if angle > 45 and angle < 75 and stage == "up":
                feedback = "Unies rece nieco wyzej!"

        elif mode == 3:
            nose_y_pixel = int(landmarks[mp_pose.PoseLandmark.NOSE.value].y * h)
            hip_y_pixel = int(landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y * h)
            ankle_y_pixel = int(landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y * h)

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

    cv2.rectangle(img, (0, 0), (w, 100), (0, 0, 0), -1)

    cv2.putText(img, f"POWTORZENIA: {counter}", (25, 45), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3, cv2.LINE_AA)

    if mode == 3 and is_calibrated:
        cv2.putText(img, f"OSTATNI SKOK: {last_jump_height:.1f} cm", (25, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                    (255, 255, 0), 2, cv2.LINE_AA)

    cv2.putText(img, f"TRENER: {feedback}", (550, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2, cv2.LINE_AA)

    tytuly = {1: "Uginanie Przedramion", 2: "Wznosy Bokiem", 3: "Wyskok Pionowy"}
    cv2.imshow(f"Asystent Treningu - {tytuly.get(mode, '')}", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()