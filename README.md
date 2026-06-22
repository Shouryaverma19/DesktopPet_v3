![language](https://img.shields.io/badge/language-python-239120)
![platform](https://img.shields.io/badge/platform-windows%2011-0078d4)
![status](https://img.shields.io/badge/status-w%20rozwoju-yellow)
[![GitHub release](https://img.shields.io/github/v/release/czarchmA8/DesktopPet_v3)](#)

# 🐉 DesktopPet_v3

Zaawansowane, interaktywne wirtualne zwierzątko na pulpit z systemem fizyki, panelem sterowania i zaawansowaną warstewizacją okien Windows.

---

## 📄 O Projekcie

**DesktopPet_v3** to aplikacja stworzona w Pythonie, która umożliwia użytkownikowi posiadanie inteligentnego, fizycznie symulowanego wirtualnego zwierzątka na pulpicie. Zwierzątko autonomicznie porusza się po ekranie, wchodzi w interakcje z oknami systemowymi, reaguje na działania użytkownika i posiada własny system statystyk.

---

## ✨ Główne Funkcje

- 🐉 **Inteligentne Zwierzątko**
  - Autonomiczny system zachowania z wieloma stanami animacji (chodzenie, siedzenie, spanie, upadek)
  - Zaawansowany system fizyki — grawitacja, kolizje, inercja ruchu
  - Reaktywność na działania myszki — łapanie, ciągnięcie i rzucanie
  - Animacje w formacie GIF z płynnym odświeżaniem

- 🎮 **Interaktywne Obiekty**
  - Dynamiczne obiekty umieszczane na pulpicie (piłki, jedzenie, przedmioty)
  - Fizyka kolizji między zwierzątkiem a obiektami oraz obiektów między sobą
  - Obsługa krawędzi okien i platformowania na oknach systemowych

- 📊 **System Statystyk i Emocji**
  - Zmienne statystyk zwierzątka: zadowolenie, kondycja, głód, senność
  - Dynamiczna zmiana nastroju na podstawie interakcji użytkownika
  - Śledzenie czasu spędzonego z zwierzątkiem

- 🎛️ **Panel Sterowania**
  - Dedykowany interfejs do konfiguracji aplikacji
  - Obsługa hotkeys — przypisywanie skrótów klawiszowych do akcji
  - Kontrola głośności dźwięków zwierzątka
  - Regulacja FPS i poziomów debugowania

- 📝 **System Logowania**
  - Centralizowane logowanie z obsługą wielu procesów
  - Kolorowy output na konsoli + zapis do pliku
  - Automatyczne czyszczenie starych logów

- 🖥️ **Tryb Debugowania**
  - Overlay hitbox z wizualizacją kolizji i masek zwierzątka
  - Debug panel z real-time informacjami o stanie aplikacji
  - Ścieżki animacji i statystyki FPS

---

## 🚀 Instalacja

1. **Sklonuj repozytorium**
   ```bash
   git clone https://github.com/czarchmA8/DesktopPet_v3.git
   cd DesktopPet_v3
   ```

2. **Utwórz wirtualne środowisko (opcjonalnie, ale rekomendowane)**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. **Zainstaluj wymagane biblioteki**
   ```bash
   pip install -r requirements.txt
   ```

## ▶️ Uruchomienie

### Normalne Uruchomienie

```bash
python main.py
```

### Opcje Uruchomienia z Argumentami

Aplikacja obsługuje następujące parametry wiersza komend:

| Argument  | Skrót | Typ   | Opis                     | Domyślnie |
|-----------|-------|-------|--------------------------|-----------|
| `--debug` | `-D`  | `int` | Poziom debugowania (0-2) | `0`       |

```bash
python main.py --debug 0
```

### Tworzenie pliku .exe (Windows, opcjonalne)
Jeśli chcesz stworzyć plik wykonywalny .exe, możesz użyć poniższej komendy:
```bash
pyinstaller main.py --onedir --windowed --icon=icon.ico --name=DesktopPet_v3
```

---

## ⚙️ Konfiguracja

Wszystkie ustawienia aplikacji znajdują się w pliku `settings.json`, a tylko niektóre są możliwe do zmiany przez panel sterowania. Zalecane jest zmienianie ustawień za pomocą panelu sterowania, aby uniknąć pomyłek. Niektóre ustawienia wymagają zostać zmienione za pomocą panelu sterowania, aby poprawnie działać (np. `autostart`)

---

## 🎯 Architektura i Wydajność

### Architektura Wieloprocesowa

Aplikacja działa na dwóch niezależnych procesach:

- **Proces PET** — silnik zwierzątka, fizyka, animacje, obsługa systemu warstw okien Windows
- **Proces DASHBOARD** — interfejs kontrolny, obsługa ustawień

Komunikacja między procesami odbywa się poprzez strukturalizowany protokół JSON wysyłany przez `multiprocessing.Pipe`.

### Optymalizacje Wydajności

- **BeginDeferWindowPos / EndDeferWindowPos** — batching aktualizacji z-order dla wszystkich obiektów
- **Cached Z-Order Neighbors** — optymalizowana funkcja `get_immediate_neighbors_above_and_below()` do benchmarkowania

---

## 📄 Licencja

Projekt jest rozwijany samodzielnie przez czarchmA8. Szczegóły licencji znajdują się w pliku LICENSE.
