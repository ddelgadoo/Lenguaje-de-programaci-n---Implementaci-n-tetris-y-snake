
from __future__ import unicode_literals, print_function

from Lexer.Tokens import TokenKind
from Ast1.expressions import NumberExpr, StringExpr, SymbolExpr, BinaryExpr, PrefixExpr, AssignmentExpr, \
    ArrayExpr, NewExpr, MemberAccessExpr, CallExpr, IndexAccessExpr
from Parser.bindingPowers import BindingPower
from Parser.lookups import nud_lu,bp_lu,led_lu


def parse_expr(p, bp):
    token_kind = p.currentTokenKind()
    nud_fn = nud_lu.get(token_kind)

    if nud_fn is None:

        raise Exception(u"NUD Handler expected for token {0}".format(token_kind))

    left = nud_fn(p)

    while bp_lu.get(p.currentTokenKind(), BindingPower.default_bp) > bp:
        token_kind = p.currentTokenKind()
        led_fn = led_lu.get(token_kind)

        if led_fn is None:

            raise Exception(u"LED Handler expected for token {0}".format(token_kind))

        left = led_fn(p, left, bp_lu[p.currentTokenKind()])

    return left

def parse_primary_expr(p):
    kind = p.currentTokenKind()

    if kind == TokenKind.NUMBER:
        number = float(p.advance().value)
        return NumberExpr(number)

    elif kind == TokenKind.STRING:
        return StringExpr(p.advance().value)

    elif kind == TokenKind.IDENTIFIER:
        return SymbolExpr(p.advance().value)

    else:

        raise Exception(
            u"Cannot create primary_expr from {0}".format(p.currentTokenKind())
        )

def parse_binary_expression(p, left, bp):
    operatorToken = p.advance()
    right = parse_expr(p, bp_lu[operatorToken.tokenKind])
    return BinaryExpr(left, operatorToken, right)

def parse_assignment_expr(p, left, bp):
    operatorToken = p.advance()
    rhs = parse_expr(p, bp)
    return AssignmentExpr(left,operatorToken ,rhs)


def parse_prefix_expr(p):
    operatorToken = p.advance()

    rhs = parse_expr(p, BindingPower.default_bp)

    return PrefixExpr(operatorToken, rhs)

def parse_grouping_expr(p):
    p.advance()
    expr = parse_expr(p,BindingPower.default_bp)
    p.expect(TokenKind.CLOSED_PARENT)
    return expr

def parse_array_expr(p):
    p.expect(TokenKind.OPEN_BRAC)
    elements = []
    if p.currentTokenKind() != TokenKind.CLOSED_BRAC:
        while True:
            elements.append(parse_expr(p, BindingPower.default_bp))
            if p.currentTokenKind() == TokenKind.CLOSED_BRAC:
                break
            p.expect(TokenKind.COMMA)
    p.expect(TokenKind.CLOSED_BRAC)
    return ArrayExpr(elements)


def parse_new_expr(p):
    """Parsea una expresion 'new ...' (ej. new PantallaTetris)"""
    p.expect(TokenKind.NEW)  # Consume el token 'new'

    # Lo que sigue a 'new' debe ser un nombre de clase
    class_name_expr = parse_expr(p, BindingPower.default_bp)

    # Aseguramos que sea un simbolo (un nombre)
    if not isinstance(class_name_expr, SymbolExpr):
        raise Exception(u"Se esperaba un nombre de clase despues de 'new'.")

    # (Mas tarde aqui podriamos parsear '()' para argumentos del constructor)

    return NewExpr(class_name_expr)


def parse_member_access_expr(p, left, bp):
    """Parsea un acceso a miembro (ej. objeto.propiedad)"""

    # 'left' es el objeto (ej. mi_objeto) que ya fue parseado.

    # 1. Consume el token '.'
    p.expect(TokenKind.DOT)

    # 2. Lo que sigue debe ser el nombre de la propiedad (un Identificador)
    property_name_token = p.expectError(
        TokenKind.IDENTIFIER,
        u"Se esperaba un nombre de propiedad despues de '.'"
    )

    # 3. Crea un SymbolExpr para el nombre de la propiedad
    property_symbol = SymbolExpr(property_name_token.value)

    return MemberAccessExpr(left, property_symbol)


def parse_call_expr(p, callee, bp):
    """Parsea una llamada a funcion (ej. mi_funcion(arg1, arg2))"""

    # 'callee' es la expresion de la izquierda (ej. mi_funcion)
    # El token actual es '(', que ya fue consumido por el 'led'
    p.expect(TokenKind.OPEN_PARENT)
    args = []

    # 1. Comprobar si no hay argumentos (ej. mi_funcion())
    if p.currentTokenKind() != TokenKind.CLOSED_PARENT:
        # 2. Parsear la lista de argumentos, separados por comas
        while True:
            # Parsea una expresion de argumento
            arg_expr = parse_expr(p, BindingPower.default_bp)
            args.append(arg_expr)

            # Si el siguiente token no es ',', parar de buscar argumentos
            if p.currentTokenKind() != TokenKind.COMMA:
                break

            p.expect(TokenKind.COMMA)  # Consume la ','

    # 3. Esperar el ')' final
    p.expect(TokenKind.CLOSED_PARENT)

    return CallExpr(callee, args)


def parse_index_access_expr(p, array, bp):
    """Parsea un acceso por indice (ej. mi_array[0])"""

    # 'array' es la expresion de la izquierda (ej. mi_array)

    # 1. Consume el token '['
    p.expect(TokenKind.OPEN_BRAC)

    # 2. Parsea la expresion del indice (ej. 0, o 'i')
    index_expr = parse_expr(p, BindingPower.default_bp)

    # 3. Espera el ']' final
    p.expect(TokenKind.CLOSED_BRAC)

    return IndexAccessExpr(array, index_expr)