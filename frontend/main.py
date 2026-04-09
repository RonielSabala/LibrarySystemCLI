"""
Library System CLI -- Menu principal (WILKER)
Punto de entrada del frontend de consola.
"""

import sys

from frontend.helpers import (
    Color,
    enable_ansi_windows,
    input_date,
    input_int,
    input_option,
    input_str,
    pause,
    print_books,
    print_error,
    print_header,
    print_info,
    print_separator,
    print_success,
)

# -- Servicios de libros (ANGERY) ---------------------------------------------
from backend.services.books.create_book import create_book
from backend.services.books.delete_book import delete_book_by_id
from backend.services.books.get_books   import get_all
from backend.services.books.update_book import update_book_by_id

# -- Servicios de prestamos (EMIL) --------------------------------------------
from backend.services.loans.create_loan import make_loan
from backend.services.loans.renew_loan  import renew_loan
from backend.services.loans.return_book import return_book

# -- Enum de estado de libro --------------------------------------------------
from backend.domain.enums import BookStatusEnum


# =============================================================================
#  MENU -- GESTION DE LIBROS
# =============================================================================

def menu_crear_libro() -> None:
    print_header("Agregar nuevo libro")
    try:
        book_id      = input_int("ID del libro")
        title        = input_str("Titulo")
        author_name  = input_str("Nombre del autor")
        author_sname = input_str("Apellido del autor")
        category     = input_str("Categoria")
        publisher    = input_str("Editorial")
        section      = input_int("Seccion (numero)")

        create_book(
            id=book_id,
            title=title,
            author_name=author_name,
            author_surname=author_sname,
            category=category,
            publisher=publisher,
            section=section,
        )
        print_success(f'Libro "{title}" creado con ID {book_id}.')
    except ValueError as e:
        print_error(str(e))
    pause()


def menu_ver_libros() -> None:
    print_header("Consultar libros")

    print_info("Puedes filtrar por ID o nombre (deja en blanco para omitir).")
    book_id   = input_int("Filtrar por ID", allow_empty=True)
    book_name = input_str("Filtrar por nombre", allow_empty=True)

    books = get_all(book_id=book_id, book_name=book_name)

    print_separator()
    print_books(books)
    pause()


def menu_actualizar_libro() -> None:
    print_header("Actualizar libro")
    print_info("Deja en blanco los campos que NO deseas modificar.")

    book_id = input_int("ID del libro a actualizar")

    title        = input_str("Nuevo titulo",              allow_empty=True)
    author_name  = input_str("Nuevo nombre del autor",    allow_empty=True)
    author_sname = input_str("Nuevo apellido del autor",  allow_empty=True)
    category     = input_str("Nueva categoria",           allow_empty=True)
    publisher    = input_str("Nueva editorial",           allow_empty=True)
    section      = input_int("Nueva seccion",             allow_empty=True)

    # Estado opcional
    status = None
    change_status = input_option("Cambiar estado del libro?", ["S", "N"])
    if change_status == "S":
        choice = input_option(
            "Nuevo estado",
            [BookStatusEnum.ON_LIBRARY, BookStatusEnum.LOANED],
        )
        status = BookStatusEnum(choice)

    ok = update_book_by_id(
        id=book_id,
        title=title,
        author_name=author_name,
        author_surname=author_sname,
        category=category,
        publisher=publisher,
        section=section,
        status=status,
    )

    if ok:
        print_success(f"Libro con ID {book_id} actualizado correctamente.")
    else:
        print_error(f"No se encontro ningun libro con ID {book_id}.")
    pause()


def menu_eliminar_libro() -> None:
    print_header("Eliminar libro")
    book_id = input_int("ID del libro a eliminar")

    confirm = input_option(
        f"Confirmas eliminar el libro con ID {book_id}?", ["S", "N"]
    )
    if confirm != "S":
        print_info("Operacion cancelada.")
        pause()
        return

    ok = delete_book_by_id(book_id)
    if ok:
        print_success(f"Libro con ID {book_id} eliminado.")
    else:
        print_error(f"No se encontro ningun libro con ID {book_id}.")
    pause()


# =============================================================================
#  MENU -- GESTION DE PRESTAMOS
# =============================================================================

def menu_crear_prestamo() -> None:
    print_header("Realizar prestamo")
    try:
        book_id    = input_int("ID del libro")
        student_id = input_int("ID del estudiante")
        end_date   = input_date("Fecha de devolucion")

        make_loan(
            book_id=book_id,
            student_id=student_id,
            end_date=end_date,
        )
        print_success(
            f"Prestamo registrado: libro {book_id} -> estudiante {student_id} "
            f"(hasta {end_date.strftime('%Y-%m-%d')})."
        )
    except ValueError as e:
        print_error(str(e))
    pause()


def menu_renovar_prestamo() -> None:
    print_header("Renovar prestamo")
    try:
        book_id      = input_int("ID del libro")
        student_id   = input_int("ID del estudiante")
        new_end_date = input_date("Nueva fecha de devolucion")

        ok = renew_loan(
            book_id=book_id,
            student_id=student_id,
            new_end_date=new_end_date,
        )
        if ok:
            print_success(
                f"Prestamo renovado hasta {new_end_date.strftime('%Y-%m-%d')}."
            )
        else:
            print_error("No se encontro el prestamo especificado.")
    except Exception as e:
        print_error(str(e))
    pause()


def menu_devolver_libro() -> None:
    print_header("Devolver libro")
    try:
        book_id    = input_int("ID del libro")
        student_id = input_int("ID del estudiante")

        ok = return_book(book_id=book_id, student_id=student_id)
        if ok:
            print_success(
                f"Libro {book_id} devuelto por estudiante {student_id}. "
                "Estado actualizado a ON_LIBRARY."
            )
        else:
            print_error("No se encontro el prestamo activo para esos datos.")
    except Exception as e:
        print_error(str(e))
    pause()


# =============================================================================
#  SUBMENUS
# =============================================================================

def submenu_libros() -> None:
    opciones = {
        "1": ("Agregar libro",     menu_crear_libro),
        "2": ("Consultar libros",  menu_ver_libros),
        "3": ("Actualizar libro",  menu_actualizar_libro),
        "4": ("Eliminar libro",    menu_eliminar_libro),
        "0": ("Volver",            None),
    }
    while True:
        print_header("[LIBROS]  Gestion de Libros")
        for key, (label, _) in opciones.items():
            bullet = Color.CYAN if key != "0" else Color.DIM
            print(f"  {bullet}[{key}]{Color.RESET}  {label}")
        print()
        opcion = input(
            f"{Color.WHITE}  Selecciona una opcion: {Color.RESET}"
        ).strip()

        if opcion not in opciones:
            print_error("Opcion no valida.")
            pause()
            continue

        label, fn = opciones[opcion]
        if fn is None:
            break
        fn()


def submenu_prestamos() -> None:
    opciones = {
        "1": ("Realizar prestamo",  menu_crear_prestamo),
        "2": ("Renovar prestamo",   menu_renovar_prestamo),
        "3": ("Devolver libro",     menu_devolver_libro),
        "0": ("Volver",             None),
    }
    while True:
        print_header("[PRESTAMOS]  Gestion de Prestamos")
        for key, (label, _) in opciones.items():
            bullet = Color.CYAN if key != "0" else Color.DIM
            print(f"  {bullet}[{key}]{Color.RESET}  {label}")
        print()
        opcion = input(
            f"{Color.WHITE}  Selecciona una opcion: {Color.RESET}"
        ).strip()

        if opcion not in opciones:
            print_error("Opcion no valida.")
            pause()
            continue

        label, fn = opciones[opcion]
        if fn is None:
            break
        fn()


# =============================================================================
#  MENU PRINCIPAL
# =============================================================================

def menu_principal() -> None:
    opciones = {
        "1": ("Gestion de Libros",     submenu_libros),
        "2": ("Gestion de Prestamos",  submenu_prestamos),
        "0": ("Salir",                 None),
    }
    while True:
        print_header("Library System  --  Menu Principal")
        for key, (label, _) in opciones.items():
            bullet = Color.CYAN if key != "0" else Color.RED
            print(f"  {bullet}[{key}]{Color.RESET}  {label}")
        print()
        opcion = input(
            f"{Color.WHITE}  Selecciona una opcion: {Color.RESET}"
        ).strip()

        if opcion not in opciones:
            print_error("Opcion no valida. Elige 1, 2 o 0.")
            pause()
            continue

        label, fn = opciones[opcion]
        if fn is None:
            print(f"\n{Color.CYAN}  Hasta luego!{Color.RESET}\n")
            sys.exit(0)
        fn()


# =============================================================================
#  ENTRADA
# =============================================================================

if __name__ == "__main__":
    enable_ansi_windows()
    menu_principal()
