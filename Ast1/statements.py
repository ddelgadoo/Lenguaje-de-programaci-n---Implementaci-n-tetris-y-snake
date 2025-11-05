from Ast1.ast1 import Stmt

class BlockStmt(Stmt):
    def __init__(self, body): # Body es un array
        self.body = body
    def stmt(self):
        pass


class ExpressionStmt(Stmt):
    def __init__(self, expression):
        self.expression = expression
    def stmt(self):
        pass

class VarDeclStmt(Stmt):
    def __init__(self, varname, isconstant, assignedvalue):
        self.varname = varname
        self.isconstant = isconstant
        self.assignedvalue = assignedvalue
    def stmt(self):
        pass

class ClassStatement(Stmt):
    def __init__(self, name, attributes=None, methods=None):
        self.name = name
        self.attributes = attributes if attributes is not None else []
        self.methods = methods if methods is not None else []
    def stmt(self):
        pass

class FunctionStatement(Stmt):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body
    def stmt(self):
        pass

class ReturnStatement(Stmt):
    def __init__(self, value):
        self.value = value
    def stmt(self):
        pass

class PrintStmt(Stmt):
    def __init__(self, expression):
        self.expression = expression
    def stmt(self):
        pass

class IfStmt(Stmt):
    def __init__(self, condition, then_branch, else_branch):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

    def stmt(self):
        pass


class WhileStmt(Stmt):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def stmt(self):
        pass


class BreakStmt(Stmt):

    def __init__(self):
        pass

    def stmt(self):
        pass