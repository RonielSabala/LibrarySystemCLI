"""
Frontend helpers — utilidades de entrada/salida para el menu de consola.
"""

import sys
import os
from datetime import datetime


# ──────────────────────────────────────────────
#  Colores ANSI (compatibles con Windows 10+)
# ──────────────────────────────────────────────
class Color:
    RESET  = "\033[0m"
    BOLD   = "\033[1m"
    RED    = "\033[91m"
    GREEN  = "\033[92m"
    YELLOW = "\033[93m"
    CYAN   = "\033[96m"
    WHITE  = "\033[97m"
    DIM    = "\033[2m"


def enable_ansi_windows() -> None:
    """Habilita los codigos ANSI en la terminal de Windows si es necesario."""
    if sys.platform == "win32":
        os.system("")  # activa el modo VT100 en Windows
        # Forzar stdout a UTF-8 para evitar UnicodeEncodeError
        sys.stdout.reconfigure(encoding="utf-8")


# ──────────────────────────────────────────────
#  Impresion con estilo (solo ASCII)
# ──────────────────────────────────────────────
def print_header(title: str) -> None:
    ancho = 52
    linea = "=" * ancho
    print(f"\n{Color.CYAN}{linea}{Color.RESET}")
    print(f"{Color.BOLD}{Color.WHITE}  {title.upper()}{Color.RESET}")
    print(f"{Color.CYAN}{linea}{Color.RESET}\n")


def print_success(msg: str) -> None:
    print(f"{Color.GREEN}  [OK]  {msg}{Color.RESET}")


def print_error(msg: str) -> None:
    print(f"{Color.RED}  [ERR] {msg}{Color.RESET}")


def print_info(msg: str) -> None:
    print(f"{Color.YELLOW}  [i]   {msg}{Color.RESET}")


def print_separator() -> None:
    print(f"{Color.DIM}  {'-' * 48}{Color.RESET}")


def pause() -> None:
    input(f"\n{Color.DIM}  Presiona Enter para continuar...{Color.RESET}")


# ──────────────────────────────────────────────
#  Funciones de entrada validada
# ──────────────────────────────────────────────
def input_int(prompt: str, allow_empty: bool = False) -> "int | None":
    """Solicita un entero; si allow_empty=True y el usuario da Enter, retorna None."""
    while True:
        raw = input(f"{Color.WHITE}  {prompt}: {Color.RESET}").strip()
        if allow_empty and raw == "":
            return None
        try:
            return int(raw)
        except ValueError:
            print_error("Debes ingresar un numero entero valido.")


def input_str(prompt: str, allow_empty: bool = False) -> "str | None":
    """Solicita texto; si allow_empty=True y el usuario da Enter, retorna None."""
    while True:
        raw = input(f"{Color.WHITE}  {prompt}: {Color.RESET}").strip()
        if raw == "" and allow_empty:
            return None
        if raw:
            return raw
        print_error("Este campo no puede estar vacio.")


def input_date(prompt: str) -> datetime:
    """Solicita una fecha en formato YYYY-MM-DD."""
    while True:
        raw = input(f"{Color.WHITE}  {prompt} (YYYY-MM-DD): {Color.RESET}").strip()
        try:
            return datetime.strptime(raw, "%Y-%m-%d")
        except ValueError:
            print_error("Formato invalido. Usa YYYY-MM-DD (ej: 2025-12-31).")


def input_option(prompt: str, options: list) -> str:
    """Pide que el usuario elija una opcion de una lista."""
    opts_str = " / ".join(options)
    while True:
        raw = input(
            f"{Color.WHITE}  {prompt} [{opts_str}]: {Color.RESET}"
        ).strip().upper()
        if raw in [o.upper() for o in options]:
            return raw
        print_error(f"Opcion invalida. Elige entre: {opts_str}")


# ──────────────────────────────────────────────
#  Funcion: mostrar tabla de libros
# ──────────────────────────────────────────────
def print_books(books: list) -> None:
    if not books:
        print_info("No hay libros que mostrar.")
        return

    header = (
        f"  {'ID':<5} {'Titulo':<25} {'Autor':<22} "
        f"{'Categoria':<14} {'Seccion':<9} {'Estado'}"
    )
    print(f"{Color.CYAN}{header}{Color.RESET}")
    print_separator()
    for b in books:
        status_color = (
            Color.GREEN if str(b.status) == "ON_LIBRARY" else Color.YELLOW
        )
        autor = f"{b.author_name} {b.author_surname}"
        print(
            f"  {b.book_id:<5} {b.title[:24]:<25} "
            f"{autor[:21]:<22} "
            f"{b.category[:13]:<14} {b.section:<9} "
            f"{status_color}{b.status}{Color.RESET}"
        )
