import AST
from AST import addToClass
from g_parser import parse

cache = {}

def assign_cache(d_type, identifier):
    if identifier not in cache:
        cache[identifier] = d_type
    else:
        raise Exception(f"Error: Redefinition of '{identifier}'.")

def hit_cache(identifiers):
    for identifier in identifiers:
        if identifier.tok not in cache:
            if type(identifier.tok) in [float, int]:
                continue
            raise Exception(f"Error: undeclared '{identifier.tok}'.")

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
    assign_cache(self.children[0].tok[0], self.children[0].tok[1])
    hit_cache(self.children[1:])

@addToClass(AST.AvancerNode)
def semantic(self):
    print("Avancer node")
    print(f"\n {self.children}")
    hit_cache(self.children)

@addToClass(AST.ReculerNode)
def semantic(self):
    print("Reculer node")
    print(f"\n {self.children}")
    hit_cache(self.children)

@addToClass(AST.DecollerNode)
def semantic(self):
    print("Decoller node")
    print(f"\n {self.children}")
    if len(self.children) != 1:
        raise Exception(f"Error: 'Decoller' does not take properties.")
    '''else:
        raise Exception(f"{len(self.children)}")'''


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
