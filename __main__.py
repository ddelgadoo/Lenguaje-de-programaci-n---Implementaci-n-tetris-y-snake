from __future__ import unicode_literals, print_function, absolute_import
import io


from Lexer.Lexer import tokenize
from Parser import parser
from Runtime.interpreter import evaluate
from Runtime.environment import Environment

file_path = u"test.brik"

with io.open(file_path, "r", encoding="utf-8") as file:
    source_code = file.read()

print(u"--- Iniciando Compilador (Lexer + Parser) ---")
tokens = tokenize(source_code)
ast_tree = parser.parse(tokens)
print(u"--- Compilacion Terminada ---")


print(u"\n--- Iniciando Runtime ---")

# 2. CREA EL ENTORNO
main_env = Environment()

try:
    # 3. PASA EL ENTORNO AL EVALUADOR
    evaluate(ast_tree, main_env)
except Exception as e:
    print(u"ERROR DE RUNTIME: " + unicode(e))

print(u"--- Runtime Terminado ---")

# Opcional: Imprime el estado final del "cerebro"
print(u"\nEstado final del Entorno:")
print(main_env.variables)