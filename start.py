import bicepsy
import barki
import wyskok

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
        break
    print("Nieprawidłowy wybór. Wpisz 1, 2 lub 3.")

if wybor == "1":
    bicepsy.uruchom_biceps()
elif wybor == "2":
    barki.uruchom_barki()
elif wybor == "3":
    wyskok.uruchom_wyskok()