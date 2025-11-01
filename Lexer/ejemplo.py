from __future__ import print_function, unicode_literals


import Lexer
import Tokens



source_code = u"""
let x = 5;
let y = "hola mundo";

// Esto es un comentario y debe ser ignorado
if (x == 5) {
    return y + 10.5;
}
"""

print("--- Tokenizando el codigo fuente ---")
print(source_code)
print("--- Resultado ---")


try:
    tokens = Lexer.tokenize(source_code)


    for tok in tokens:
        print(Tokens.debug(tok))

except Exception as e:
    print("Error del Lexer:")
    print(e)