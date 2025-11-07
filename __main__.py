# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import
import sys
import os
import io



sys.path.append(os.path.dirname(os.path.abspath(__file__)))



from Lexer.lexer import tokenize
from Parser import parser
from Runtime.interpreter import evaluate
from Runtime.environment import Environment


def resource_path(relative_path):

    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)


# --- NUEVA FUNCION: El Lanzador ---
def elegir_juego():


    print("===============================")
    print("    REPRODUCTOR DE JUEGOS BRIK   ")
    print("===============================")
    print("")
    print("Por favor, elige un juego:")
    print("  1. Snake")
    print("  2. Tetris")
    print("")

    while True:
        try:

            opcion = raw_input("Escribe 1 o 2 y presiona Enter: ")
        except EOFError:
            return None

        if opcion == "1":
            print(u"Cargando Snake...")
            return u"Snake\snake.brik"
        elif opcion == "2":
            print(u"Cargando Tetris...")
            return u"Tetris\_tetris.brik"
        else:
            print(u"Opcion invalida, intenta de nuevo.")



if __name__ == "__main__":


    nombre_archivo_brik = elegir_juego()


    if nombre_archivo_brik is None:
        sys.exit()


    file_path = resource_path(nombre_archivo_brik)


    try:
        with io.open(file_path, "r", encoding="utf-8") as file:
            source_code = file.read()

        print(u"--- Iniciando Compilador (Lexer + Parser) ---")
        tokens = tokenize(source_code)
        ast_tree = parser.parse(tokens)
        print(u"--- Compilacion Terminada ---")

        print(u"\n--- Iniciando Runtime ---")
        main_env = Environment()
        evaluate(ast_tree, main_env)
        print(u"--- Runtime Terminado ---")

    except Exception as e:
        print(u"--- ERROR FATAL ---")
        print(u"ERROR: " + str(e))

        raw_input(u"\nPresiona Enter para salir.")