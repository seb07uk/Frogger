# 🐸 Frogger: Enhanced Graphics Edition

![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)
![Pygame](https://img.shields.io/badge/library-Pygame-green.svg)
![License](https://img.shields.io/badge/license-All%20Rights%20Reserved-red.svg)

**Frogger Enhanced** to nowoczesna, wysokiej jakości implementacja klasycznej gry zręcznościowej. Projekt skupia się na **grafice proceduralnej** (generowanej w 100% z kodu) oraz zaawansowanych efektach wizualnych, eliminując potrzebę używania zewnętrznych plików graficznych.



## 🌟 Kluczowe Cechy

* **Grafika Proceduralna:** Wszystkie elementy (żaba, samochody, kłody) są rysowane dynamicznie przy użyciu prymitywów graficznych, gradientów i funkcji trygonometrycznych.
* **System Cząsteczek (Particle Engine):**
    * **Pluski wody:** Generowane przy kontakcie z rzeką.
    * **Pył skoku:** Subtelne efekty przy każdym ruchu żaby.
    * **Iskry kolizji:** Intensywne efekty przy zderzeniu z pojazdem.
* **Dynamiczne Środowisko:** Rzeka z animacją fal (sinusoidalne przesunięcia kolorów) oraz pojazdy z systemem świateł (headlights).
* **Persistent Storage:** Automatyczny zapis 5 najlepszych wyników w formacie JSON w ukrytym folderze systemowym `.polsoft`.

---

## 🛠️ Specyfikacja Techniczna

Gra została napisana w paradygmacie obiektowym (OOP), co pozwala na łatwą rozbudowę:

* **`ConfigManager`**: Obsługuje zapis/odczyt konfiguracji i wyników (cross-platform).
* **`ParticleSystem`**: Niezależny silnik zarządzający cyklem życia, grawitacją i przezroczystością cząsteczek.
* **`WaterEffect`**: Algorytm renderujący animowaną taflę wody w czasie rzeczywistym.
* **`Vehicle` & `Log`**: Klasy encji z logiką zapętlania pozycji (wrapping).



---

## 🚀 Instalacja i Uruchomienie

### Wymagania
* Python 3.10 lub nowszy
* Biblioteka Pygame

### Szybki start
1.  **Zainstaluj Pygame:**
    ```bash
    pip install pygame
    ```
2.  **Uruchom grę:**
    ```bash
    python frogger.py
    ```

---

## 🎮 Sterowanie

| Klawisz | Akcja |
| :--- | :--- |
| **Strzałki (↑ ↓ ← →)** | Poruszanie żabą / Nawigacja w menu |
| **Enter** | Start gry / Potwierdzenie |
| **Esc** | Wyjście / Powrót do menu |

---

## 📂 Lokalizacja Danych
Wyniki i ustawienia są przechowywane w:
* **Windows:** `%USERPROFILE%\.polsoft\games\Frogger.json`
* **Linux/Mac:** `~/.polsoft/games/Frogger.json`

---

## 📝 Informacje o Autorze
* **Autor:** Sebastian Januchowski
* **Organizacja:** polsoft.ITS™ London
* **Wersja:** 2.0.0 (Production)
* **Status:** Stable

© 2026 Sebastian Januchowski. Wszystkie prawa zastrzeżone. Projekt polsoft.ITS™ London.