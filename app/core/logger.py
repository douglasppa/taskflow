from datetime import datetime, timezone
import inspect

COLORS = {
    "INFO": "\033[94m",  # Azul
    "DEBUG": "\033[90m",  # Cinza
    "WARNING": "\033[38;5;178m",  # Amarelo
    "ERROR": "\033[91m",  # Vermelho
    "RESET": "\033[0m",  # Reset
}


def log(msg: str, level: str = "INFO"):
    frame = inspect.stack()[1]
    module = inspect.getmodule(frame[0])
    mod_name = module.__name__ if module else "unknown"

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    color = COLORS.get(level.upper(), COLORS["RESET"])
    reset = COLORS["RESET"]

    print(f"{color}{timestamp} [{level.upper()}] {mod_name}: {msg}{reset}")
