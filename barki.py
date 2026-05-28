import cv2
import math
import numpy as np
import mediapipe as mp


def uruchom_barki():
    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils
    pose_cam1 = mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7)
    pose_cam2 = mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7)

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

    cap1 = cv2.VideoCapture(0)
    cap2 = cv2.VideoCapture(1)

    for cap in [cap1, cap2]:
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    while True:
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
            hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
            shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                        landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                     landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
            angle = calculate_angle(hip, shoulder, elbow)

            shoulder_pixel = (int(shoulder[0] * active_w), int(shoulder[1] * active_h))
            cv2.putText(img1, f"{int(angle)} deg", shoulder_pixel, cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2,
                        cv2.LINE_AA)

            if angle < 25:
                stage = "down"
                feedback = "Dobry opust. Unies rece w bok."
            if angle > 80 and stage == "down":
                stage = "up"
                counter += 1
                feedback = "Idealna wysokosc! Opusc powoli."
            if angle > 45 and angle < 75 and stage == "up":
                feedback = "Unies rece nieco wyzej!"

        combined_img = np.hstack((img1, img2))
        comb_h, comb_w, _ = combined_img.shape

        cv2.rectangle(combined_img, (0, 0), (comb_w, 100), (0, 0, 0), -1)
        cv2.putText(combined_img, f"POWTORZENIA: {counter}", (25, 45), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3,
                    cv2.LINE_AA)
        cv2.putText(combined_img, f"TRENER: {feedback}", (550, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2,
                    cv2.LINE_AA)

        cv2.imshow("Asystent Treningu - Wznosy Bokiem (Dual Camera)", combined_img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap1.release()
    cap2.release()
    cv2.destroyAllWindows()