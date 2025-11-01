# -*- coding: utf-8 -*-
from __future__ import unicode_literals

"""CLASSES"""

# En Python 2.7, 'Enum' y 'auto' no existen.
# Creamos una clase simple con constantes de enteros.
# Los imports de 'logging.config' y 'token' se eliminaron
# ya que definías tus propios IDENTIFIER, NUMBER y STRING.

class TokenKind(object): # Hereda de (object)
    # Asignamos enteros manualmente, como sugería tu comentario (IOF = 0)
    IOF = 0
    NUMBER = 1
    STRING = 2
    IDENTIFIER = 3

    OPEN_BRAC = 4  # [
    CLOSED_BRAC = 5  # ]
    OPEN_CURL = 6  # {
    CLOSED_CURL = 7  # }
    OPEN_PARENT = 8  # (
    CLOSED_PARENT = 9  # )

    ASSIGNMENT = 10  # =
    EQUAL = 11  # ==
    NOT = 12  # !
    NOT_EQUAL = 13  # !=

    LESS = 14
    LESS_EQUAL = 15
    GREATER = 16
    GREATER_EQUAL = 17

    OR = 18
    AND = 19

    DOT = 20
    COLON = 21
    COMMA = 22
    SEMICOMMA = 23
    QUESTION = 24

    PLUS_PLUS = 25  # ++
    MINUS_MINUS = 26  # --
    PLUS_EQUAL = 27  # +=
    MINUS_EQUAL = 28  # -=

    PLUS = 29
    DASH = 30
    SLASH = 31
    STAR = 32
    PERCENT = 33

    # Reserved words
    DEF = 34
    CONST = 35
    CLASS = 36
    NEW = 37
    IMPORT = 38
    FROM = 39
    IF = 40
    ELSE = 41
    WHILE = 42
    FOR = 43
    IN = 44
    RANGE = 45
    EXPORT = 46
    TYPEOF = 47
    RETURN = 48
    LET = 49
    PRINT = 50
    BREAK = 51

# Esta tupla es necesaria para reemplazar la función .name de Enum
# DEBE estar exactamente en el mismo orden que los enteros de arriba
TOKEN_KIND_NAMES = (
    u"IOF", u"NUMBER", u"STRING", u"IDENTIFIER",
    u"OPEN_BRAC", u"CLOSED_BRAC", u"OPEN_CURL", u"CLOSED_CURL",
    u"OPEN_PARENT", u"CLOSED_PARENT",
    u"ASSIGNMENT", u"EQUAL", u"NOT", u"NOT_EQUAL",
    u"LESS", u"LESS_EQUAL", u"GREATER", u"GREATER_EQUAL",
    u"OR", u"AND",
    u"DOT", u"COLON", u"COMMA", u"SEMICOMMA", u"QUESTION",
    u"PLUS_PLUS", u"MINUS_MINUS", u"PLUS_EQUAL", u"MINUS_EQUAL",
    u"PLUS", u"DASH", u"SLASH", u"STAR", u"PERCENT",
    u"DEF", u"CONST", u"CLASS", u"NEW", u"IMPORT", u"FROM",
    u"IF", u"ELSE", u"WHILE", u"FOR", u"IN", u"RANGE",
    u"EXPORT", u"TYPEOF", u"RETURN", u"LET", u"PRINT", u"BREAK"
)


#A global dictionary for reserved words
# Se añaden prefijos 'u' para consistencia con unicode_literals
reserved_lu = {
        u"def": TokenKind.DEF,
        u"let": TokenKind.LET,
        u"return": TokenKind.RETURN,
        u"const": TokenKind.CONST,
        u"class": TokenKind.CLASS,
        u"new": TokenKind.NEW,
        u"import": TokenKind.IMPORT,
        u"from": TokenKind.FROM,
        u"if": TokenKind.IF,
        u"else": TokenKind.ELSE,
        u"while": TokenKind.WHILE,
        u"for": TokenKind.FOR,
        u"in": TokenKind.IN ,
        u"range": TokenKind.RANGE,
        u"export": TokenKind.EXPORT,
        u"typeof": TokenKind.TYPEOF,
        U"print": TokenKind.PRINT,
        U"break" : TokenKind.BREAK
    }

#Global constant EOF
IOF = TokenKind.IOF


class Token(object): # Hereda de (object) para ser "new-style class"
    def __init__(self, tokenKind, value): #Define token as a type of token and a string value
        self.tokenKind = tokenKind
        self.value = value
        self.lexeme = value


"""----------------------------------------------------------------------------"""

"""GLOBAL FUNCTIONS"""
def newToken(kind , value):
    return Token(kind,value)

def tokenKindString(kind): # Modificada para usar la tupla
    # 'kind' es ahora un entero (ej. 0, 1, ...)
    return TOKEN_KIND_NAMES[kind]

def debug(tok): # If the type of the token is IDENTIFIER, NUMBER or STRING, it prints its string form, and its value.
    if tok.tokenKind in (TokenKind.IDENTIFIER, TokenKind.NUMBER, TokenKind.STRING):
        # Se usa .format() y prefijo 'u' para compatibilidad
        return u"{} ({})".format(tokenKindString(tok.tokenKind), tok.value)
    else:
        return u"{}".format(tokenKindString(tok.tokenKind))


