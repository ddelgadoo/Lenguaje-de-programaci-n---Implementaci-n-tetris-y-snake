from Parser.lookups import led,nud, stmt
from Parser.bindingPowers import BindingPower
from Lexer.Tokens import TokenKind
from Parser.expr import (parse_primary_expr, parse_binary_expression, parse_prefix_expr,
                         parse_assignment_expr, parse_grouping_expr, parse_array_expr, parse_new_expr,
                         parse_member_access_expr, parse_call_expr, parse_index_access_expr)
from Parser.stmt import (parse_var_dcl_stmt, parse_class_dcl_stmt, parse_function_stmt,
                         parse_return_stmt, parse_print_stmt, parse_if_stmt, parse_while_stmt, parse_break_stmt, )


def createTokenLookUps():
    led(TokenKind.ASSIGNMENT,BindingPower.assignment, parse_assignment_expr)
    led(TokenKind.PLUS_EQUAL, BindingPower.assignment,parse_assignment_expr)
    led(TokenKind.MINUS_EQUAL, BindingPower.assignment,parse_assignment_expr)



    #Binary Expressions

    #Logical
    led(TokenKind.AND,BindingPower.logical ,parse_binary_expression)
    led(TokenKind.OR,BindingPower.logical, parse_binary_expression)

    #Relational
    led(TokenKind.LESS,BindingPower.relational, parse_binary_expression)
    led(TokenKind.LESS_EQUAL,BindingPower.relational, parse_binary_expression)
    led(TokenKind.GREATER,BindingPower.relational,parse_binary_expression)
    led(TokenKind.GREATER_EQUAL,BindingPower.relational, parse_binary_expression)
    led(TokenKind.EQUAL, BindingPower.relational,parse_binary_expression)
    led(TokenKind.NOT_EQUAL,BindingPower.relational, parse_binary_expression)

    #Additive, mulplicative, call
    led(TokenKind.PLUS, BindingPower.additive, parse_binary_expression)
    led(TokenKind.DASH, BindingPower.additive, parse_binary_expression)
    led(TokenKind.STAR, BindingPower.multiplicative, parse_binary_expression)
    led(TokenKind.SLASH, BindingPower.multiplicative,parse_binary_expression)
    led(TokenKind.PERCENT, BindingPower.multiplicative, parse_binary_expression)
    led(TokenKind.DOT, BindingPower.member, parse_member_access_expr)
    led(TokenKind.OPEN_PARENT, BindingPower.call, parse_call_expr)
    led(TokenKind.OPEN_BRAC, BindingPower.call, parse_index_access_expr)

    #Primary Expressions
    nud(TokenKind.NUMBER , parse_primary_expr)
    nud(TokenKind.STRING, parse_primary_expr)
    nud(TokenKind.IDENTIFIER ,parse_primary_expr)
    nud(TokenKind.OPEN_PARENT, parse_grouping_expr)
    nud(TokenKind.DASH,parse_prefix_expr)
    nud(TokenKind.OPEN_BRAC, parse_array_expr)
    nud(TokenKind.NEW, parse_new_expr)

    #Statements
    stmt(TokenKind.CONST, parse_var_dcl_stmt)
    stmt(TokenKind.LET, parse_var_dcl_stmt)
    stmt(TokenKind.CLASS, parse_class_dcl_stmt)
    stmt(TokenKind.DEF, parse_function_stmt)
    stmt(TokenKind.RETURN, parse_return_stmt)
    stmt(TokenKind.PRINT, parse_print_stmt)
    stmt(TokenKind.IF,parse_if_stmt)
    stmt(TokenKind.WHILE, parse_while_stmt)
    stmt(TokenKind.BREAK, parse_break_stmt)