import cv2
import voiceassistant
import exercise_utils


def uruchom_biceps():
    mp_pose, mp_drawing, pose_cam1, pose_cam2 = exercise_utils.setup_mediapipe()
    counter, stage, feedback, feedback_glosowy, poprzedni_feedback = exercise_utils.inicjalizuj_trening()

    cap1, cap2, ma_kamere2 = exercise_utils.setup_cameras()

    while True:
        success1, img1, img2, active_results, active_h, active_w, ma_kamere2 = exercise_utils.pobierz_i_przetworz_obraz(
            cap1, cap2, ma_kamere2, pose_cam1, pose_cam2, mp_drawing, mp_pose
        )

        if not success1:
            break

        if active_results and active_results.pose_landmarks:
            landmarks = active_results.pose_landmarks.landmark
            angle = exercise_utils.pobierz_kat_i_rysuj(
                img1, landmarks,
                mp_pose.PoseLandmark.RIGHT_SHOULDER,
                mp_pose.PoseLandmark.RIGHT_ELBOW,
                mp_pose.PoseLandmark.RIGHT_WRIST,
                active_w, active_h
            )

            if angle > 150:
                if stage == "lowering":
                    feedback = "Dobry wyprost. Unos ciezar."
                    feedback_glosowy = "Dobry wyprost"
                elif stage == "lifting":
                    feedback = "Ruch byl zbyt plytki!"
                    feedback_glosowy = "Popraw technike"
                stage = "down"

            if angle < 130 and stage == "down":
                stage = "lifting"
                feedback_glosowy = ""

            if angle < 40:
                if stage == "lifting":
                    stage = "up"
                    counter += 1
                    feedback = "Swietnie! Opuszczaj powoli."
                    feedback_glosowy = str(counter)
                elif stage == "lowering":
                    stage = "up"
                    feedback = "Brak pelnego wyprostu!"
                    feedback_glosowy = "Popraw technike"

            if angle > 60 and stage == "up":
                stage = "lowering"
                feedback_glosowy = ""

            if feedback_glosowy != poprzedni_feedback:
                if feedback_glosowy != "":
                    voiceassistant.wiadomosci_do_przeczytania.put(feedback_glosowy)
                poprzedni_feedback = feedback_glosowy

        combined_img = exercise_utils.combine_and_draw_ui(img1, img2, ma_kamere2, counter, feedback)

        tytul_okna = "Asystent Treningu - Uginanie Przedramion (Dual Camera)" if ma_kamere2 else "Asystent Treningu - Uginanie Przedramion (Single Camera)"
        cv2.imshow(tytul_okna, combined_img)

        if voiceassistant.flaga_koniec:
            voiceassistant.powiedz_to(f"Zakończono trening. Liczba powtórzeń: {counter}")
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap1.release()
    if ma_kamere2:
        cap2.release()
    cv2.destroyAllWindows()
    voiceassistant.wiadomosci_do_przeczytania.put("STOP")