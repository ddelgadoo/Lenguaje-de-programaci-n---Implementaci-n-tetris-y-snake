class BrikClass(object):
    """Representa la definicion de una clase 'brik', (la plantilla)."""
    def __init__(self, name, attributes, methods):
        self.name = name
        self.attributes = attributes # Lista de nodos VarDeclStmt
        self.methods = methods     # Lista de nodos FunctionStatement

    def __repr__(self):
        # Si se imprime el entorno
        return u"<class {0}>".format(self.name)

class BrikInstance(object):
    """Representa una instancia de una clase 'brik' (un objeto real)."""
    def __init__(self, brik_class):
        self.brik_class = brik_class
        self.fields = {} # Un diccionario para guardar atributos (ej. 'pixeles')

    def __repr__(self):
        return u"<instance {0}>".format(self.brik_class.name)

class BrikBoundMethod(object):
    """Representa una funcion que esta 'atada' a una instancia (self)."""
    def __init__(self, instance, function_node):
        self.instance = instance       # El 'self'
        self.function = function_node  # El nodo FunctionStatement (el 'def ...')

    def __repr__(self):
        # Para depuracion
        return u"<bound method {0}>".format(self.function.name)


class BrikNativeFunction(object):
    """Representa una funcion nativa (implementada en Python)."""

    def __init__(self, py_function):
        self.py_function = py_function  # El 'callable' de Python

    def __repr__(self):
        # Para depuracion
        return u"<native function>"


class BrikFunction(object):
    """Representa la definicion de una funcion global 'def'."""

    def __init__(self, function_node):
        self.function = function_node  # El nodo FunctionStatement

    def __repr__(self):
        # Para depuracion
        return u"<function {0}>".format(self.function.name)