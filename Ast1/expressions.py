from ast import Expr


class NumberExpr(Expr):
    def __init__(self, value):
        self.value = value
    def expr(self):
        pass

class StringExpr(Expr):
    def __init__(self, value):
        self.value = value
    def expr(self):
        pass

class SymbolExpr(Expr):
    def __init__(self, value):
        self.value = value
    def expr(self):
        pass
#--------------------------------------------------

class BinaryExpr(Expr):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def expr(self):
        pass

class PrefixExpr(Expr):
    def __init__(self, operator, rightexpr):
        self.operator = operator
        self.rightexpr = rightexpr

    def expr(self):
        pass

class AssignmentExpr(Expr):
    def __init__(self, assign, operator, value):
        self.assign = assign
        self.operator = operator
        self.value = value

    def expr(self):
        pass

class ArrayExpr(Expr):
    def __init__(self, elements):
        self.elements = elements

    def expr(self):
        pass


class NewExpr(Expr):
    def __init__(self, class_name):
        self.class_name = class_name

    def expr(self):
        pass


class MemberAccessExpr(Expr):
    def __init__(self, object, property):
        self.object = object  # La instancia (ej. mi_objeto)
        self.property = property  # El nombre del campo (ej. pixeles)

    def expr(self):
        pass


class CallExpr(Expr):
    def __init__(self, callee, args):
        self.callee = callee  # La expresion que se esta llamando (ej. mi_auto.arrancar)
        self.args = args  # La lista de expresiones de argumentos (ej. [arg1, arg2])

    def expr(self):
        pass


class IndexAccessExpr(Expr):
    def __init__(self, array, index):
        self.array = array  # La expresion del array (ej. mi_array)
        self.index = index  # La expresion del indice (ej. 0)

    def expr(self):
        pass






