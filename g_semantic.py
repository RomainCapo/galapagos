import AST
from AST import addToClass
from g_parser import parse

@addToClass(AST.ProgramNode)
def semantic(self):
    print("Program node")
    for child in self.children:
        child.semantic()

@addToClass(AST.TokenNode)
def semantic(self):
    print("Token node")

@addToClass(AST.OpNode)
def semantic(self):
    print("Op node")

@addToClass(AST.AssignNode)
def semantic(self):
    print("Assign node")

@addToClass(AST.AvancerNode)
def semantic(self):
    print("Avancer node")

@addToClass(AST.ReculerNode)
def semantic(self):
    print("Reculer node")

@addToClass(AST.DecollerNode)
def semantic(self):
    print("Decoller node")

@addToClass(AST.AtterrirNode)
def semantic(self):
    print("Atterrir node")

@addToClass(AST.TournerGaucheNode)
def semantic(self):
    print("Tourner gauche node")

@addToClass(AST.TournerDroiteNode)
def semantic(self):
    print("Tourner droite node")

@addToClass(AST.PositionXNode)
def semantic(self):
    print("Position x node")

@addToClass(AST.PositionYNode)
def semantic(self):
    print("Position y node")

@addToClass(AST.TqNode)
def semantic(self):
    print("Tq node")

@addToClass(AST.SiNode)
def semantic(self):
    print("Si node")

if __name__ == "__main__":
    import sys, os
    prog = open("inputs/" + sys.argv[1]).read()
    ast = parse(prog)

    ast.semantic()
