# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
from Runtime.types import BrikNativeFunction
import time
import random
import os
try:
    # Para Windows
    import msvcrt
except ImportError:
    # Para Mac/Linux
    import sys
    import tty
    import termios
    import select


def native_len(value):
    """Devuelve el tamano de un array (lista) o string."""
    if not hasattr(value, '__len__'):
        raise Exception(u"No se puede aplicar 'len()' a este tipo.")
    return float(len(value))

def native_sleep(ms):
    """Pausa la ejecucion por milisegundos."""
    time.sleep(ms / 1000.0) # convertir seg a miliseg
    return None

def native_rand(min_val, max_val):
    """Devuelve un entero aleatorio entre min_val y max_val (incluidos)."""

    return float(random.randrange(int(min_val), int(max_val) + 1))

def native_clear_screen():
    """Limpia la terminal."""
    # 'nt' es para Windows, 'posix' es para Mac/Linux
    os.system('cls' if os.name == 'nt' else 'clear')
    return None

def native_push_front(array, value):
    """Inserta un 'value' al inicio de un 'array' (lista)."""
    if not isinstance(array, list):
        raise Exception(u"push_front() solo funciona con arrays.")
    array.insert(0, value)
    return None

def native_pop_tail(array):
    """Quita y devuelve el ultimo elemento de un 'array' (lista)."""
    if not isinstance(array, list):
        raise Exception(u"pop_tail() solo funciona con arrays.")
    if len(array) == 0:
        raise Exception(u"pop_tail() no se puede usar en un array vacio.")
    return array.pop()


def native_get_key():
    """Obtiene una tecla presionada sin bloquear la ejecucion."""
    try:
        if msvcrt.kbhit():
            return msvcrt.getch().decode('utf-8')
        return None

    except NameError:


        if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):


            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setcbreak(fd)
                ch = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch
        return None



class Environment(object):
    def __init__(self):
         # Es un diccionario para guardar variables
        self.variables = {}
        self.declare(u"len", BrikNativeFunction(native_len), is_constant=True)
        self.declare(u"sleep", BrikNativeFunction(native_sleep), is_constant=True)
        self.declare(u"rand", BrikNativeFunction(native_rand), is_constant=True)
        self.declare(u"clear_screen", BrikNativeFunction(native_clear_screen), is_constant=True)
        self.declare(u"push_front", BrikNativeFunction(native_push_front), is_constant=True)
        self.declare(u"pop_tail", BrikNativeFunction(native_pop_tail), is_constant=True)
        self.declare(u"get_key", BrikNativeFunction(native_get_key), is_constant=True)

        self.declare(u"true", True, is_constant=True)
        self.declare(u"false", False, is_constant=True)

    def declare(self, name, value, is_constant):
        """Define una nueva variable (let o const)"""
        self.variables[name] = value
        return value

    def get(self, name):
        """Obtiene el valor de una variable"""
        if name not in self.variables:
            raise Exception(u"Variable no definida: " + name)
        return self.variables[name]

    def assign(self, name, value):
        """Asigna un nuevo valor a una variable ya existente"""
        if name not in self.variables:
            raise Exception(u"Asignacion a variable no definida: " + name)

        self.variables[name] = value
        return value