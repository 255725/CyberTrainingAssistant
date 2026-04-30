import subprocess
import os
import pygame
import speech_recognition as sr
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
# Tu wpisz ścieżkę do folderu, gdzie masz plik piper.exe
PIPER_EXE = BASE_DIR / "piper" / "piper.exe"
# Tu wpisz ścieżkę do pliku .onnx (głos bass-high)
MODEL_PATH = BASE_DIR / "piper" / "pl_PL-bass-high.onnx"
OUTPUT_FILE = BASE_DIR / "trener_mowa.wav"


def mow(tekst):
    print(f"Trener mówi: {tekst}")

    # 1. Budujemy komendę (używamy cudzysłowów dla ścieżek ze spacjami)
    # Echo przesyła tekst do Pipera, który tworzy plik .wav
    command = f'echo {tekst} | "{PIPER_EXE}" --model "{MODEL_PATH}" --output_file "{OUTPUT_FILE}"'

    try:
        # Wykonujemy generowanie mowy
        subprocess.run(command, shell=True, check=True, capture_output=True)

        # 2. Odtwarzanie audio
        pygame.mixer.init()
        pygame.mixer.music.load(str(OUTPUT_FILE))
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.quit()

    except Exception as e:
        print(f"Błąd generowania mowy: {e}")
        print("PRÓBA AWARYJNA: Używam głosu systemowego Windows...")
        import pyttsx3
        alt_engine = pyttsx3.init()
        alt_engine.say(tekst)
        alt_engine.runAndWait()


def sluchaj():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n[TRENER SŁUCHA...]")
        r.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = r.listen(source, timeout=5)
            tekst = r.recognize_google(audio, language="pl-PL")
            return tekst.lower()
        except:
            return ""


# --- START PROGRAMU ---
if __name__ == "__main__":
    mow("Witaj! Jestem twoim darmowym trenerem. Powiedz start, żeby zacząć, lub koniec, żeby wyłączyć.")

    while True:
        komenda = sluchaj()
        if komenda:
            print(f"Usłyszałem: {komenda}")

            if any(slowo in komenda for slowo in ["koniec", "stop", "wyłącz"]):
                mow("Dobra, kończymy na dzisiaj. Kawał dobrej roboty!")
                break

            elif "pompki" in komenda:
                mow("Jasne! Kładź się i robimy pompki. Raz, dwa, trzy! Dawaj dalej!")

            elif "przerwa" in komenda:
                mow("Odpocznij chwilę, ale nie siadaj. Głębokie wdechy!")