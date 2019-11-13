import AST
from AST import addToClass
from g_parser import parse

def visit_children(children):
    for child in children:
        child.semantic()

@addToClass(AST.ProgramNode)
def semantic(self):
    print("Program node")
    print(f"\n {self.children}")
    visit_children(self.children)

@addToClass(AST.TokenNode)
def semantic(self):
    print("Token node")
    print(f"\n {self.children}")

@addToClass(AST.OpNode)
def semantic(self):
    print("Op node")
    print(f"\n {self.children}")

@addToClass(AST.AssignNode)
def semantic(self):
    print("Assign node")
    print(f"\n {self.children}")

@addToClass(AST.AvancerNode)
def semantic(self):
    print("Avancer node")
    print(f"\n {self.children}")

@addToClass(AST.ReculerNode)
def semantic(self):
    print("Reculer node")
    print(f"\n {self.children}")

@addToClass(AST.DecollerNode)
def semantic(self):
    print("Decoller node")
    print(f"\n {self.children}")

@addToClass(AST.AtterrirNode)
def semantic(self):
    print("Atterrir node")
    print(f"\n {self.children}")

@addToClass(AST.TournerGaucheNode)
def semantic(self):
    print("Tourner gauche node")
    print(f"\n {self.children}")

@addToClass(AST.TournerDroiteNode)
def semantic(self):
    print("Tourner droite node")
    print(f"\n {self.children}")

@addToClass(AST.PositionXNode)
def semantic(self):
    print("Position x node")
    print(f"\n {self.children}")

@addToClass(AST.PositionYNode)
def semantic(self):
    print("Position y node")
    print(f"\n {self.children}")

@addToClass(AST.TqNode)
def semantic(self):
    print("Tq node")
    print(f"\n {self.children}")
    visit_children(self.children)

@addToClass(AST.SiNode)
def semantic(self):
    print("Si node")
    print(f"\n {self.children}")
    visit_children(self.children)

if __name__ == "__main__":
    import sys, os
    prog = open("inputs/" + sys.argv[1]).read()
    ast = parse(prog)

    ast.semantic()
