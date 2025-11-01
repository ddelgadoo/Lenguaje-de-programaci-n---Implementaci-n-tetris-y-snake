from abc import ABCMeta, abstractmethod

# The Ast is

class Stmt(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def stmt(self):
        pass

class Expr(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def expr(self):
        pass



