import cv2
import voiceAssistant
import exerciseUtils

AKTYWNY = False
counter = 0

def zatrzymaj_trening():
    global AKTYWNY, counter
    AKTYWNY = False
    wynik_koncowy = counter
    counter = 0
    return wynik_koncowy

def generuj_obraz_barki():
    global AKTYWNY, counter
    AKTYWNY = True
    counter = 0

    mp_pose, mp_drawing, pose_cam1, pose_cam2 = exerciseUtils.setup_mediapipe()
    _, stage, feedback, feedback_glosowy, poprzedni_feedback = exerciseUtils.inicjalizuj_trening()

    cap1, cap2, ma_kamere2 = exerciseUtils.setup_cameras()

    try:
        while AKTYWNY:
            success1, img1, img2, active_results, active_h, active_w, ma_kamere2 = exerciseUtils.pobierz_i_przetworz_obraz(
                cap1, cap2, ma_kamere2, pose_cam1, pose_cam2, mp_drawing, mp_pose
            )

            if not success1:
                break

            if active_results and active_results.pose_landmarks:
                landmarks = active_results.pose_landmarks.landmark
                angle = exerciseUtils.pobierz_kat_i_rysuj(
                    img1, landmarks,
                    mp_pose.PoseLandmark.RIGHT_HIP,
                    mp_pose.PoseLandmark.RIGHT_SHOULDER,
                    mp_pose.PoseLandmark.RIGHT_ELBOW,
                    active_w, active_h
                )

                if angle < 25:
                    if stage == "lifting":
                        feedback = "Ruch byl zbyt plytki!"
                        feedback_glosowy = "Popraw technike"
                    elif stage == "lowering":
                        feedback = "Dobry opust. Unies rece w bok."
                        feedback_glosowy = "Dobrze"
                    stage = "down"

                if angle > 40 and stage == "down":
                    stage = "lifting"
                    feedback_glosowy = ""

                if angle > 80:
                    if stage == "lifting":
                        stage = "up"
                        counter += 1
                        feedback = "Idealna wysokosc! Opusc powoli."
                        feedback_glosowy = str(counter)
                    elif stage == "lowering":
                        stage = "up"
                        feedback = "Brak pelnego opustu!"
                        feedback_glosowy = "Popraw technike"

                if angle < 60 and stage == "up":
                    stage = "lowering"
                    feedback_glosowy = ""

                if feedback_glosowy != poprzedni_feedback:
                    if feedback_glosowy != "":
                        voiceAssistant.wiadomosci_do_przeczytania.put(feedback_glosowy)
                    poprzedni_feedback = feedback_glosowy

            combined_img = exerciseUtils.combine_and_draw_ui(img1, img2, ma_kamere2, counter, feedback)

            if voiceAssistant.flaga_koniec:
                voiceAssistant.powiedz_to(f"Zakończono trening. Liczba powtórzeń: {counter}")
                break

            ret, buffer = cv2.imencode('.jpg', combined_img)
            if not ret:
                continue

            frame_bytes = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    finally:
        cap1.release()
        if ma_kamere2:
            cap2.release()
        voiceAssistant.wiadomosci_do_przeczytania.put("STOP")
        AKTYWNY = False