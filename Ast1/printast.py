from __future__ import unicode_literals
from Ast1.statements import ClassStatement, FunctionStatement, ReturnStatement


def print_ast(node, file, indent=0):
    spacing = u'  ' * indent

    if isinstance(node, ClassStatement):
        file.write(u"{0}ClassStmt\n".format(spacing))
        file.write(u"{0}  name: {1}\n".format(spacing, node.name))
        file.write(u"{0}  attributes:\n".format(spacing))
        if node.attributes:
            for attr in node.attributes:
                print_ast(attr, file, indent + 2)
        else:
            file.write(u"{0}    (no attributes)\n".format(spacing))
        file.write(u"{0}  methods:\n".format(spacing))
        if node.methods:
            for method in node.methods:
                print_ast(method, file, indent + 2)
        else:
            file.write(u"{0}    (no methods)\n".format(spacing))

    elif isinstance(node, FunctionStatement):
        file.write(u"{0}FunctionStmt\n".format(spacing))
        file.write(u"{0}  name: {1}\n".format(spacing, node.name))
        file.write(u"{0}  params: {1}\n".format(spacing, node.params))
        file.write(u"{0}  body:\n".format(spacing))
        for stmt in node.body:
            print_ast(stmt, file, indent + 2)

    elif isinstance(node, ReturnStatement):
        file.write(u"{0}ReturnStmt\n".format(spacing))
        if node.value:
            file.write(u"{0}  value:\n".format(spacing))
            print_ast(node.value, file, indent + 2)
        else:
            file.write(u"{0}  value: None\n".format(spacing))

    elif hasattr(node, 'body'):  # BlockStmt
        file.write(u"{0}BlockStmt\n".format(spacing))
        file.write(u"{0}  body:\n".format(spacing))
        for stmt in node.body:
            print_ast(stmt, file, indent + 2)

    elif hasattr(node, 'expression'):  # ExpressionStmt
        file.write(u"{0}ExpressionStmt\n".format(spacing))
        file.write(u"{0}  expression:\n".format(spacing))
        print_ast(node.expression, file, indent + 2)

    elif hasattr(node, 'operator') and hasattr(node, 'left') and hasattr(node, 'right'):  # BinaryExpr
        file.write(u"{0}BinaryExpr(operator:{1})\n".format(spacing, node.operator.lexeme))
        file.write(u"{0}  left:\n".format(spacing))
        print_ast(node.left, file, indent + 2)
        file.write(u"{0}  right:\n".format(spacing))
        print_ast(node.right, file, indent + 2)


    elif hasattr(node, 'value') and not hasattr(node, 'assign'):  # NumberExpr, StringExpr
        file.write(u"{0}{1}(value:{2})\n".format(spacing, type(node).__name__, node.value))

    elif hasattr(node, 'name'):  # SymbolExpr u otros
        file.write(u"{0}{1}(name:{2})\n".format(spacing, type(node).__name__, node.name))

    elif hasattr(node, 'varname') and hasattr(node, 'isconstant') and hasattr(node, 'assignedvalue'):  # VarDeclStmt
        file.write(u"{0}VarDeclStmt\n".format(spacing))
        file.write(u"{0}  varname: {1}\n".format(spacing, node.varname))
        file.write(u"{0}  isconstant: {1}\n".format(spacing, node.isconstant))
        file.write(u"{0}  assignedvalue:\n".format(spacing))
        print_ast(node.assignedvalue, file, indent + 2)

    elif hasattr(node, "operator") and hasattr(node, "rightexpr"):
        file.write(u"{0}PrefixExpr(operator: {1})\n".format(spacing, node.operator.lexeme))
        file.write(u"{0}  rightexpr:\n".format(spacing))
        print_ast(node.rightexpr, file, indent + 2)

    elif hasattr(node, 'assign') and hasattr(node, 'operator') and hasattr(node, 'value'):  # AssignmentExpr
        file.write(u"{0}AssignmentExpr(operator:{1})\n".format(spacing, node.operator.lexeme))
        file.write(u"{0}  assign:\n".format(spacing))
        print_ast(node.assign, file, indent + 2)
        file.write(u"{0}  value:\n".format(spacing))
        print_ast(node.value, file, indent + 2)

    elif hasattr(node, 'elements'):  # ArrayExpr
        file.write(u"{0}ArrayExpr\n".format(spacing))
        file.write(u"{0}  elements:\n".format(spacing))
        for element in node.elements:
            print_ast(element, file, indent + 2)

    else:
        file.write(u"{0}{1}\n".format(spacing, repr(node)))
