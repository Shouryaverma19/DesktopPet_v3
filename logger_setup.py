import logging
from logging.handlers import QueueHandler, QueueListener
from pathlib import Path
from datetime import datetime

class ColorFormatter(logging.Formatter):
    """Formatter z kolorami ANSI dla konsoli"""

    COLORS = {
        'DEBUG': '\033[36m',  # Cyan
        'INFO': '\033[92m',  # Light Green
        'WARNING': '\033[93m',  # Light Yellow
        'ERROR': '\033[91m',  # Light Red
        'CRITICAL': '\033[41m\033[97m',  # Red bg + White text
    }
    RESET = '\033[0m'

    def format(self, record):
        levelname = record.levelname
        orig_levelname = record.levelname
        if levelname in self.COLORS:
            record.levelname = f"{self.COLORS[levelname]}{f'[{levelname}]':10s}{self.RESET}"
        result = super().format(record)
        record.levelname = orig_levelname

        return result

class PlainFormatter(logging.Formatter):
    """Formatter bez kolorów ANSI"""

    def format(self, record):
        # Zwykły format bez kolorów
        return super().format(record)

def _czyszcz_stare_logi(folder_logow: Path, prefiks: str, logger, max_pliki: int = 3) -> None:
    """Usuwa stare pliki logów, zachowując tylko określoną liczbę najnowszych"""
    if not folder_logow.exists():
        return

    # Znajdź wszystkie pliki logów z danym prefiksem
    pliki_logow = sorted(
        folder_logow.glob(f"{prefiks}_*.log"),
        key=lambda p: p.stat().st_mtime,
        reverse=True  # Najnowsze pierwsze
    )

    # Usuń pliki starsze niż top N
    for plik_do_usuniecia in pliki_logow[max_pliki:]:
        try:
            plik_do_usuniecia.unlink()
            logger.debug(f"Usunięto stary plik logu: {plik_do_usuniecia.name}")
        except Exception as e:
            logger.warning(f"Nie udało się usunąć {plik_do_usuniecia.name}: {e}")

def skonfiguruj_glowny_listener(nazwa_pliku: str, kolejka, debug=False, max_stare_logi: int=3) -> QueueListener:
    folder_logow = Path("logs")
    if not folder_logow.exists():
        folder_logow.mkdir()

    # Tworzenie nazwy pliku z datą i czasem
    teraz = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nazwa_z_data = f"{nazwa_pliku}_{teraz}.log"
    sciezka_pliku = folder_logow / nazwa_z_data

    # Handler konsoli (z kolorami)
    handler_konsola = logging.StreamHandler()
    handler_konsola.setLevel(logging.DEBUG if debug else logging.INFO)

    format_konsoli = ColorFormatter(fmt="%(levelname)s [%(name)s]: %(message)s")
    handler_konsola.setFormatter(format_konsoli)

    # Handler pliku (bez kolorów)
    handler_plik = logging.FileHandler(
        sciezka_pliku,
        mode="w",
        encoding="utf-8"
    )
    handler_plik.setLevel(logging.DEBUG)

    format_pliku = PlainFormatter(
        fmt="[%(asctime)s]-[%(levelname)s]-(%(filename)s:%(lineno)d) -> %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    handler_plik.setFormatter(format_pliku)

    listener = QueueListener(kolejka, handler_konsola, handler_plik, respect_handler_level=True)

    # Czyszczenie starych plików logów
    logger = skonfiguruj_logger_procesu("logger_setup", kolejka)
    logger.info("[✅] Uruchomiono centralny systemu logowania")
    _czyszcz_stare_logi(folder_logow, nazwa_pliku, logger, max_stare_logi)

    return listener

def skonfiguruj_logger_procesu(nazwa_loggera: str, kolejka) -> logging.Logger:
    logger = logging.getLogger(nazwa_loggera)
    logger.setLevel(logging.DEBUG)

    if logger.hasHandlers():
        logger.handlers.clear()

    handler_kolejki = QueueHandler(kolejka)
    logger.addHandler(handler_kolejki)

    return logger
