# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function


import sys
if sys.version_info[0] < 3:
    try:
        unicode # Intenta acceder a 'unicode'
    except NameError:

        unicode = type(u'')

import Ast1.statements as stmts
import Ast1.expressions as exprs
from Runtime.environment import Environment
from Runtime.types import BrikClass, BrikInstance, BrikBoundMethod, BrikNativeFunction, BrikFunction

try:
    unicode
except NameError:

    unicode = type(u'')



class ReturnException(Exception):
    """Excepcion especial usada para 'lanzar' un valor de retorno."""
    def __init__(self, value):
        self.value = value
class BreakException(Exception):
    """Excepcion especial usada para 'saltar' fuera de un bucle."""
    pass

# El despachador (Dispatcher)

def evaluate(node, env):
    """
    Funcion principal que "visita" un nodo del AST.
    """
    node_type = type(node).__name__
    visitor_method_name = u'visit_' + node_type
    visitor = globals().get(visitor_method_name)

    if visitor is None:
        raise Exception(u"No hay metodo visitante para el nodo: " + node_type)

    return visitor(node, env)


# Visitantes de Sentencias (No devuelven valor)

def visit_BlockStmt(node, env):
    """Visita un bloque de codigo (lista de sentencias)"""
    for stmt in node.body:
        evaluate(stmt, env)


def visit_ExpressionStmt(node, env):
    """Visita una expresion (ej. 5 + 10;)"""
    evaluate(node.expression, env)


def visit_PrintStmt(node, env):
    """Visita una sentencia 'print' y asegura un salto de línea."""

    # 1. Evalua la expresion dentro del print
    valor_a_imprimir = evaluate(node.expression, env)
    output_str = unicode(valor_a_imprimir)

    # 2. Manejo de la impresión
    import sys

    if isinstance(valor_a_imprimir, (str, unicode)):
        # CASO A: Es una cadena (incluye strings simples y el output formateado de Snake)

        # Escribimos la cadena directamente al stdout
        sys.stdout.write(output_str)

        # Si la cadena NO termina en un salto de línea, lo añadimos
        if not output_str.endswith(u'\n'):
            sys.stdout.write(u'\n')

    else:
        # CASO B: Es un número u otro tipo (no string)
        # Aquí usamos el print por defecto, pero con la función print_function
        # que siempre añade un salto de línea.
        print(valor_a_imprimir)


# --- NUEVO VISITANTE para 'let x = 5;' ---
def visit_VarDeclStmt(node, env):
    """Visita una declaracion 'let' o 'const'"""
    # 1. Evalua el valor de la derecha (ej. el '5')
    value = evaluate(node.assignedvalue, env)

    # 2. Declara la variable en el entorno
    env.declare(node.varname, value, node.isconstant)


# --- Visitantes de Expresiones  ---

def visit_NumberExpr(node, env):
    """Visita un numero literal (ej. 5)"""
    return node.value  # No necesita 'env'


def visit_StringExpr(node, env):
    """Visita un string literal (ej. "hola")"""
    return node.value.strip(u'"')  # No necesita 'env'


# --- NUEVO VISITANTE para 'x' ---
def visit_SymbolExpr(node, env):
    """Visita un simbolo (variable) (ej. x)"""
    # Busca el valor de la variable en el entorno
    return env.get(node.value)


def visit_AssignmentExpr(node, env):
    """Visita una asignacion (ej. x = 20, mi_objeto.propiedad = 20, o mi_array[0] = 20)"""

    # 1. Evalua el valor de la derecha (el valor a asignar)
    value = evaluate(node.value, env)

    # 2. Comprueba que tipo de asignacion es

    if isinstance(node.assign, exprs.SymbolExpr):
        # CASO 1: Asignacion simple (ej. x = 20)
        varname = node.assign.value
        return env.assign(varname, value)

    elif isinstance(node.assign, exprs.MemberAccessExpr):
        # CASO 2: Asignacion a propiedad (ej. self.anio = 20)
        instance = evaluate(node.assign.object, env)
        if not isinstance(instance, BrikInstance):
            raise Exception(u"No se puede asignar a la propiedad de algo que no es un objeto.")
        property_name = node.assign.property.value
        instance.fields[property_name] = value
        return value

    #
    elif isinstance(node.assign, exprs.IndexAccessExpr):
        # CASO 3: Asignacion a indice (ej. mi_array[0] = 10)

        # 3a. Evalua el array (ej. 'mi_array')
        array_val = evaluate(node.assign.array, env)

        # 3b. Evalua el indice (ej. '0')
        index_val = evaluate(node.assign.index, env)

        # 3c. Validaciones
        if not isinstance(array_val, list):
            raise Exception(u"No se puede indexar algo que no es un array (lista).")
        try:
            index_int = int(index_val)
        except (ValueError, TypeError):
            raise Exception(u"El indice del array debe ser un numero.")

        # 3d. Asigna el valor a la lista de Python
        try:
            array_val[index_int] = value
            return value
        except IndexError:
            raise Exception(u"Indice fuera de rango al asignar.")


    else:
        # Si no es un simbolo, acceso, o indice, es un error
        raise Exception(u"Asignacion invalida. Solo se puede asignar a un simbolo, propiedad o indice.")



def visit_BinaryExpr(node, env):
    """Visita una expresion binaria (ej. a + b)"""

    # 1. Evalua recursivamente la parte izquierda
    left = evaluate(node.left, env)

    # 2. Evalua recursivamente la parte derecha
    right = evaluate(node.right, env)

    # 3. Obtiene el operador (el string, ej. "+", "==")
    op = node.operator.lexeme

    # Operaciones Aritmeticas
    if op == u'+':
        if isinstance(left, (str, unicode)) or isinstance(right, (str, unicode)):
            # Si uno es un string, convierte ambos a string (unicode)
            return unicode(left) + unicode(right)
        else:
            # Si no, es una suma numerica normal
            return left + right

    elif op == u'-':
        return left - right
    elif op == u'*':
        return left * right
    elif op == u'/':
        if right == 0:
            raise Exception(u"Division por cero.")
        return left / right
    elif op == u'%':
        return left % right

    # Operaciones de Comparacion
    elif op == u'==':
        return left == right
    elif op == u'!=':
        return left != right
    elif op == u'<':
        return left < right
    elif op == u'<=':
        return left <= right
    elif op == u'>':
        return left > right
    elif op == u'>=':
        return left >= right

    # Operaciones Logicas
    elif op == u'&&':
        return left and right
    elif op == u'||':
        return left or right

    # Si llegamos aqui, el operador no esta implementado
    raise Exception(u"Operador binario no implementado: " + op)


def visit_ArrayExpr(node, env):
    """Visita una expresion de array (ej. [1, "hola", x])"""

    elements = []
    # 1. Itera sobre cada nodo de expresion en el array
    for element_node in node.elements:
        # 2. Evalua cada expresion
        element_value = evaluate(element_node, env)
        # 3. Anade el valor resultante a una lista de Python
        elements.append(element_value)

    # 4. Devuelve la lista de Python completa
    return elements


def visit_IfStmt(node, env):
    """Ejecuta una sentencia if-else"""
    condition_result = evaluate(node.condition, env)

    # 2. Comprueba si el resultado es "verdadero"
    #    (Python 2.7 trata 0, False, None, y '' como Falso)
    if condition_result:
        # 3. Si es verdadero, ejecuta el bloque 'then'
        evaluate(node.then_branch, env)
    elif node.else_branch is not None:
        # 4. O (si existe un 'else'), ejecuta el bloque 'else'
        evaluate(node.else_branch, env)


def visit_WhileStmt(node, env):
    """Ejecuta un bucle while y atrapa la excepcion 'break'."""

    # 1. Evalua la condicion por primera vez
    condition_result = evaluate(node.condition, env)

    while condition_result:
        try:
            # 2. Ejecuta el cuerpo del bucle
            evaluate(node.body, env)

        except BreakException:
            # 3. Si atrapamos 'break', salimos del bucle inmediatamente
            break

        except ReturnException as e:
            # 4. Si atrapamos 'return', lo relanzamos
            raise e

        # 5. Vuelve a evaluar la condicion para el proximo ciclo
        condition_result = evaluate(node.condition, env)

def visit_ClassStatement(node, env):
    """Visita una declaracion 'class ...'"""

    # 1. Crea la "plantilla" (BrikClass) guardando los nodos
    #    de los atributos y metodos para usarlos despues.
    brik_class = BrikClass(node.name, node.attributes, node.methods)

    # 2. Almacena la plantilla en el entorno.
    #    ej. 'PantallaTetris' -> <class PantallaTetris>
    env.declare(node.name, brik_class, is_constant=True)

def visit_NewExpr(node, env):
    """Visita una expresion 'new ...'"""

    # 1. El nodo 'class_name' es un SymbolExpr (ej. 'PantallaTetris')
    #  solo queremos su nombre.
    class_name = node.class_name.value

    # 2. Busca la "plantilla" (BrikClass) en el entorno
    brik_class = env.get(class_name)

    if not isinstance(brik_class, BrikClass):
        raise Exception(u"No se puede usar 'new' en algo que no es una clase.")

    # 3. Crea la instancia (el objeto real)
    instance = BrikInstance(brik_class)

    # 4. Inicializa los atributos de la instancia
    #    (ej. 'let pixeles = [...]')
    for attr_stmt in brik_class.attributes:
        # visit_VarDeclStmt añadira 'attr_stmt.varname' al
        # diccionario 'instance.fields'
        value = evaluate(attr_stmt.assignedvalue, env)
        instance.fields[attr_stmt.varname] = value

    return instance


def visit_MemberAccessExpr(node, env):
    """Visita un acceso a miembro (ej. mi_objeto.pixeles o mi_objeto.iniciar)"""

    # 1. Evalua el objeto de la izquierda para obtener la instancia
    instance = evaluate(node.object, env)

    # 2. Asegura de que es una instancia
    if not isinstance(instance, BrikInstance):
        raise Exception(u"No se puede acceder a la propiedad de algo que no es un objeto.")

    # 3. Obtener el nombre de la propiedad
    property_name = node.property.value

    # 4.  Buscar la propiedad en los atributos
    if property_name in instance.fields:
        return instance.fields[property_name]

    # 5. Si no es un atributo, buscar en los métodos de la clase
    for method_node in instance.brik_class.methods:
        if method_node.name == property_name:
            # Encontrado, Devolver un bound method
            # Esto empaqueta la instancia (self) con la funcion
            return BrikBoundMethod(instance, method_node)

    # 6. Si no se encuentra en ninguno
    raise Exception(u"El objeto no tiene la propiedad o metodo: " + property_name)

def visit_ReturnStatement(node, env):
    """Visita una sentencia 'return'."""

    value = None
    if node.value is not None:
        # 1. Si hay un valor (ej. return 5;), evalua
        value = evaluate(node.value, env)

    # 2. Lanza la excepcion con el valor
    raise ReturnException(value)


def visit_CallExpr(node, env):
    """Visita una llamada (ej. mi_objeto.arrancar(), len(arr), o dibujar())"""

    # 1. Evalua el 'callee' (lo que se esta llamando)
    callee = evaluate(node.callee, env)

    # 2. Evaluar los argumentos
    arg_values = []
    for arg_node in node.args:
        arg_values.append(evaluate(arg_node, env))

    # --- CASO 1: Es una funcion nativa (ej. len(arr)) ---
    if isinstance(callee, BrikNativeFunction):
        return callee.py_function(*arg_values)

    # --- CASO 2: Es un metodo de clase (ej. miAuto.setAnio(2030)) ---
    if isinstance(callee, BrikBoundMethod):

        bound_method = callee
        function_node = bound_method.function

        expected_param_count = len(function_node.params) - 1  # Resta 1 por 'self'
        received_arg_count = len(arg_values)

        if received_arg_count != expected_param_count:
            raise Exception(
                u"Argumentos incorrectos para {0}: se esperaban {1}, se recibieron {2}".format(
                    function_node.name, expected_param_count, received_arg_count
                )
            )

        call_env = Environment()
        call_env.declare(u"self", bound_method.instance, is_constant=True)

        for i in range(expected_param_count):
            param_name = function_node.params[i + 1]  # Salta 'self'
            arg_value = arg_values[i]
            call_env.declare(param_name, arg_value, is_constant=False)

        return_value = None
        try:
            for stmt in function_node.body:
                evaluate(stmt, call_env)
        except ReturnException as e:
            return_value = e.value
        return return_value

    # CASO 3: Es una funcion global de Brik (ej. dibujarPantalla(...))
    if isinstance(callee, BrikFunction):

        function_node = callee.function  # El nodo FunctionStatement

        # 3a. Comprobar que el numero de argumentos sea correcto
        expected_param_count = len(function_node.params)
        received_arg_count = len(arg_values)

        if received_arg_count != expected_param_count:
            raise Exception(
                u"Argumentos incorrectos para {0}: se esperaban {1}, se recibieron {2}".format(
                    function_node.name, expected_param_count, received_arg_count
                )
            )

        # 3b. Crear un NUEVO entorno (scope) para esta llamada
        call_env = Environment()

        # 3c. Definir todos los argumentos en el nuevo entorno
        for i in range(expected_param_count):
            param_name = function_node.params[i]
            arg_value = arg_values[i]
            call_env.declare(param_name, arg_value, is_constant=False)

        # 3d. Ejecutar el cuerpo de la funcion y capturar el 'return'
        return_value = None
        try:
            for stmt in function_node.body:
                evaluate(stmt, call_env)
        except ReturnException as e:
            return_value = e.value
        return return_value

    # Si no es ninguno de los tres tipos
    raise Exception(u"No se puede 'llamar' a algo que no es un metodo o funcion nativa.")



def visit_IndexAccessExpr(node, env):
    """Visita un acceso por indice (ej. mi_array[0])"""

    # 1. Evalua la expresion del array (ej. mi_array)
    array_val = evaluate(node.array, env)

    # 2. Evalua la expresion del indice (ej. 0 o 'i')
    index_val = evaluate(node.index, env)

    # 3. Asegurarse de que el array es una lista
    if not isinstance(array_val, list):
        raise Exception(u"No se puede indexar algo que no es un array (lista).")

    # 4. Asegurarse de que el indice es un numero y convertirlo a entero
    try:
        index_int = int(index_val)
    except (ValueError, TypeError):
        raise Exception(u"El indice del array debe ser un numero.")

    # 5. Devolver el elemento
    try:
        return array_val[index_int]
    except IndexError:
        raise Exception(u"Indice fuera de rango.")


def visit_FunctionStatement(node, env):

    brik_function = BrikFunction(node)
    env.declare(node.name, brik_function, is_constant=True)


def visit_PrefixExpr(node, env):
    """Visita una expresion prefija (ej. -5)"""

    # 1. Evalua la expresion de la derecha (ej. el 5)
    value = evaluate(node.rightexpr, env)

    # 2. Obtiene el operador (el string, ej. "-")
    op = node.operator.lexeme

    # 3. Aplica la operacion
    if op == u'-':
        # Asumiendo que 'value' es un numero
        return -value

    raise Exception(u"Operador prefijo no implementado: " + op)

def visit_BreakStmt(node, env):
    """Visita una sentencia 'break'."""
    # Lanza la excepcion para saltar inmediatamente fuera del bucle
    raise BreakException()