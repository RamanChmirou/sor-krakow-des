# Symulacja SOR w Krakowie (DES)

Studium przypadku: SOR Szpitala im. G. Narutowicza w Krakowie.
Projekt z przedmiotu *Symulacja systemów dyskretnych*.

**Zespół:** Bednarski Paweł, Chmirou Raman, Czosnek Bartłomiej, Danilau Mikhail

## Struktura
- `model/sor_des.py` – pierwsza wersja modelu DES (lista zdarzeń, triaż, lekarze z kolejką wg koloru)
- `dane/parametry_SOR_Krakow.xlsx` – 55 parametrów modelu ze źródłami (stan na 22.10.2026)
- `prezentacje/Gotowe.pptx` – prezentacja projektu (15 slajdów)

## Uruchomienie
```
python3 model/sor_des.py
```
Wymaga tylko Pythona 3 (bez zewnętrznych bibliotek). Wynik: średni czas do lekarza wg koloru triażu
dla 3 i 4 lekarzy (10 przebiegów po 30 dni). To wersja demonstracyjna, jeszcze bez kalibracji na TOPSOR.

## Do zrobienia
- kalibracja na danych TOPSOR
- scenariusze szczególne (karetki, zdarzenie masowe, zmiana dyżuru)
- prognoza napływu i tryb awaryjny
