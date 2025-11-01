from Ast1.ast import Expr,Stmt
from Parser.bindingPowers import BindingPower


def stmt_handler(parser):
    return Stmt
def nud_handler(parser):
    return Expr
def led_handler(parser, left, binding_power):
    return Expr


bp_lu = {}
nud_lu = {}
led_lu = {}
stmt_lu = {}

def led(kind, bindingpower, ledfunction):
    bp_lu[kind] = bindingpower
    led_lu[kind] = ledfunction

def nud(kind,nudfunction):
    nud_lu[kind] = nudfunction

def stmt(kind, stmtfunction):
    bp_lu[kind] = BindingPower.default_bp
    stmt_lu[kind] = stmtfunction





