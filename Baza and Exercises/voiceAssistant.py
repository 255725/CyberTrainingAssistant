import pyttsx3
import queue
import threading
import speech_recognition as sr

wiadomosci_do_przeczytania = queue.Queue()
flaga_koniec = False


def powiedz_to(tekst):
    try:
        import pythoncom
        pythoncom.CoInitialize()
    except ImportError:
        pass

    engine = pyttsx3.init()
    engine.setProperty('rate', 180)
    engine.say(str(tekst))
    engine.runAndWait()


def odtwarzacz_glosu():
    while True:
        tekst = wiadomosci_do_przeczytania.get()
        if tekst == "STOP":
            break

        print(f">>> ASYSTENT: {tekst}")

        watek = threading.Thread(target=powiedz_to, args=(tekst,), daemon=True)
        watek.start()
        watek.join()


def uruchom_asystenta():
    watek_glosowy = threading.Thread(target=odtwarzacz_glosu, daemon=True)
    watek_glosowy.start()
    return watek_glosowy


def callback_nasluchu(recognizer, audio):
    global flaga_koniec
    try:
        tekst = recognizer.recognize_google(audio, language="pl-PL").lower()
        print(f">>> USŁYSZANO: {tekst}")
        if "koniec" in tekst:
            flaga_koniec = True
    except sr.UnknownValueError:
        pass
    except sr.RequestError:
        pass


def uruchom_nasluchiwanie():
    r = sr.Recognizer()
    m = sr.Microphone()
    with m as source:
        r.adjust_for_ambient_noise(source)
    r.listen_in_background(m, callback_nasluchu)