import cv2
import time
import voiceassistant
import exercise_utils


def uruchom_wyskok():
    mp_pose, mp_drawing, pose_cam1, pose_cam2 = exercise_utils.setup_mediapipe()
    counter, stage, feedback, feedback_glosowy, poprzedni_feedback = exercise_utils.inicjalizuj_trening("Unies OBIE rece by skalibrowac")

    baseline_hip_y = 0
    cm_per_pixel = 0
    is_calibrated = False
    calibration_start_time = 0
    max_flight_y = 0
    last_jump_height = 0.0
    user_height_cm = 175.0

    cap1, cap2, ma_kamere2 = exercise_utils.setup_cameras()

    while True:
        success1, img1, img2, active_results, active_h, active_w, ma_kamere2 = exercise_utils.pobierz_i_przetworz_obraz(
            cap1, cap2, ma_kamere2, pose_cam1, pose_cam2, mp_drawing, mp_pose
        )

        if not success1:
            break

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
                            cm_per_pixel = user_height_cm / pixel_height
                            is_calibrated = True
                            stage = "standing"
                            feedback = "Skalibrowano! Mozesz skakac."
                            feedback_glosowy = "Skalibrowano. Mozesz skakac."
                        else:
                            feedback = "Blad! Odsun sie od kamery."
                            feedback_glosowy = "Odsun sie od kamery"
                            calibration_start_time = 0
                    else:
                        feedback = f"Trzymaj rece w gorze... {time_left}"
                else:
                    calibration_start_time = 0
                    feedback = "Unies OBIE rece do gory by skalibrowac"
            else:
                displacement = baseline_hip_y - hip_y_pixel
                if displacement < -30:
                    if stage != "squat":
                        stage = "squat"
                        feedback = "Dobre zejscie. Odbij sie!"
                        feedback_glosowy = ""
                elif displacement > 20 and stage == "squat":
                    stage = "air"
                    max_flight_y = displacement
                    feedback_glosowy = ""
                elif stage == "air":
                    if displacement > max_flight_y:
                        max_flight_y = displacement
                    if displacement < 10:
                        stage = "standing"
                        counter += 1
                        last_jump_height = max_flight_y * cm_per_pixel
                        feedback = "Swietne ladowanie! Skacz znowu."
                        feedback_glosowy = f"{int(last_jump_height)} centymetrow"
                        max_flight_y = 0

            if feedback_glosowy != poprzedni_feedback:
                if feedback_glosowy != "":
                    voiceassistant.wiadomosci_do_przeczytania.put(feedback_glosowy)
                poprzedni_feedback = feedback_glosowy

        combined_img = exercise_utils.combine_and_draw_ui(img1, img2, ma_kamere2, counter, feedback)

        if is_calibrated:
            cv2.putText(combined_img, f"OSTATNI SKOK: {last_jump_height:.1f} cm", (25, 85), cv2.FONT_HERSHEY_SIMPLEX,
                        0.9,
                        (255, 255, 0), 2, cv2.LINE_AA)

        tytul_okna = "Asystent Treningu - Wyskok Pionowy (Dual Camera)" if ma_kamere2 else "Asystent Treningu - Wyskok Pionowy (Single Camera)"
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