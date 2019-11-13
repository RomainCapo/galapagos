import AST
from AST import addToClass
from g_parser import parse

@addToClass(AST.ProgramNode)
def semantic(self):
    print("In here")

if __name__ == "__main__":
    import sys, os
    prog = open("inputs/" + sys.argv[1]).read()
    ast = parse(prog)

    ast.semantic()
