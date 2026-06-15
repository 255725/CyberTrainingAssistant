import cv2
import numpy as np
import math
import mediapipe as mp
import voiceAssistant


def inicjalizuj_trening(komunikat_startowy="Rozpocznij cwiczenie"):
    voiceAssistant.flaga_koniec = False
    voiceAssistant.uruchom_asystenta()
    voiceAssistant.uruchom_nasluchiwanie()

    return 0, None, komunikat_startowy, komunikat_startowy, ""

def pobierz_i_przetworz_obraz(cap1, cap2, ma_kamere2, pose_cam1, pose_cam2, mp_drawing, mp_pose):
    success1, img1 = cap1.read()
    if not success1:
        return False, None, None, None, 0, 0, ma_kamere2

    imgRGB1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
    results1 = pose_cam1.process(imgRGB1)

    active_results = results1
    active_h, active_w, _ = img1.shape

    if results1.pose_landmarks:
        mp_drawing.draw_landmarks(img1, results1.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    img2 = None
    if ma_kamere2:
        success2, img2 = cap2.read()
        if success2:
            imgRGB2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
            results2 = pose_cam2.process(imgRGB2)
            if results2.pose_landmarks:
                mp_drawing.draw_landmarks(img2, results2.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        else:
            ma_kamere2 = False

    return True, img1, img2, active_results, active_h, active_w, ma_kamere2

def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    radians = math.atan2(c[1] - b[1], c[0] - b[0]) - math.atan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    if angle > 180.0:
        angle = 360 - angle
    return angle

def pobierz_kat_i_rysuj(img, landmarks, p1_enum, p2_enum, p3_enum, active_w, active_h):
    p1 = [landmarks[p1_enum.value].x, landmarks[p1_enum.value].y]
    p2 = [landmarks[p2_enum.value].x, landmarks[p2_enum.value].y]
    p3 = [landmarks[p3_enum.value].x, landmarks[p3_enum.value].y]

    angle = calculate_angle(p1, p2, p3)

    pixel_coords = (int(p2[0] * active_w), int(p2[1] * active_h))
    cv2.putText(img, f"{int(angle)} deg", pixel_coords, cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)

    return angle

def setup_mediapipe():
    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils
    pose_cam1 = mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7)
    pose_cam2 = mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7)
    return mp_pose, mp_drawing, pose_cam1, pose_cam2


def setup_cameras():
    cap1 = cv2.VideoCapture(0)
    cap2 = cv2.VideoCapture(1)

    if not cap1.isOpened():
        print("BŁĄD: Nie można połączyć się z główną kamerą (indeks 0).")
    else:
        print("SUKCES: Główna kamera została wykryta.")
    ma_kamere2 = cap2.isOpened()

    cap1.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    if ma_kamere2:
        cap2.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap2.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    return cap1, cap2, ma_kamere2


def combine_and_draw_ui(img1, img2, ma_kamere2, counter, feedback):
    if ma_kamere2 and img2 is not None:
        # Pobieramy wymiary obu obrazów
        h1, w1, _ = img1.shape
        h2, w2, _ = img2.shape

        # Jeśli wysokości są różne, skalujemy img2 do wysokości img1
        if h1 != h2:
            # Obliczamy nową szerokość, zachowując proporcje
            nowa_szerokosc = int(w2 * (h1 / h2))
            img2_gotowy = cv2.resize(img2, (nowa_szerokosc, h1))
        else:
            img2_gotowy = img2

        # Sklejamy obrazy poziomo
        combined_img = np.hstack((img1, img2_gotowy))
    else:
        combined_img = img1

    comb_h, comb_w, _ = combined_img.shape

    # Rysowanie interfejsu
    cv2.rectangle(combined_img, (0, 0), (comb_w, 100), (0, 0, 0), -1)
    cv2.putText(combined_img, f"POWTORZENIA: {counter}", (25, 45), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3,
                cv2.LINE_AA)
    cv2.putText(combined_img, f"TRENER: {feedback}", (550, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2,
                cv2.LINE_AA)

    return combined_img