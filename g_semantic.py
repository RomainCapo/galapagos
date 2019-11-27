import AST
from AST import addToClass
from g_parser import parse

'''
DEV note:
Pour l'instant, le correct nombre de d'arguments est géré dans g_parser.py (la méthode p_error(p)).
Cette méthode est call par exemple quand qqn écrit "Decoller t 12" (ce qui est faux).
Si, après discussion, nous voudrions gérer ces erreurs de nombre d'args ici, on utiliserait qqch comme ceci, par exemple:

if len(self.children) != 1:
        raise Exception(f"Error: 'Decoller' does not take properties.")
    else:
        raise Exception(f"{len(self.children)}")

'''

cache = {}

def assign_cache(d_type, identifier):
    ''' When a new variable is declared, add it to the dictionnary (cache). Raise an error if a variable with this name already exists. '''
    if identifier not in cache:
        cache[identifier] = d_type
    else:
        raise Exception(f"Error: Redefinition of '{identifier}'.")

def hit_cache(identifiers):
    ''' check if children are variables beforehand declared or integer/float. Else raise an error. '''
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
    print(f"\t {self.children}\n")
    visit_children(self.children)

@addToClass(AST.TokenNode)
def semantic(self):
    print("Token node")
    print(f"\t {self.children}\n")

@addToClass(AST.OpNode)
def semantic(self):
    print("Op node")
    print(f"\t {self.children}\n")

@addToClass(AST.AssignNode)
def semantic(self):
    print("Assign node")
    print(f"\t {self.children}\n")
    assign_cache(self.children[0].tok[0], self.children[0].tok[1])
    hit_cache(self.children[1:])

@addToClass(AST.AvancerNode)
def semantic(self):
    print("Avancer node")
    print(f"\t {self.children}\n")
    hit_cache(self.children)

@addToClass(AST.ReculerNode)
def semantic(self):
    print("Reculer node")
    print(f"\t {self.children}\n")
    hit_cache(self.children)

@addToClass(AST.DecollerNode)
def semantic(self):
    print("Decoller node")
    print(f"\t {self.children}\n")

@addToClass(AST.AtterrirNode)
def semantic(self):
    print("Atterrir node")
    print(f"\t {self.children}\n")

@addToClass(AST.TournerGaucheNode)
def semantic(self):
    print("Tourner gauche node")
    print(f"\t {self.children}\n")
    hit_cache(self.children)

@addToClass(AST.TournerDroiteNode)
def semantic(self):
    print("Tourner droite node")
    print(f"\t {self.children}\n")
    hit_cache(self.children)

@addToClass(AST.PositionXNode)
def semantic(self):
    print("Position x node")
    print(f"\n {self.children}")
    print(f"---{self}----")
    hit_cache(self.children[0])

@addToClass(AST.PositionYNode)
def semantic(self):
    print("Position y node")
    print(f"\n {self.children}")
    print(f"---{self}----")
    hit_cache(self.children[0])

@addToClass(AST.TqNode)
def semantic(self):
    print("Tq node")
    print(f"\t {self.children}\n")
    visit_children(self.children)

@addToClass(AST.SiNode)
def semantic(self):
    print("Si node")
    print(f"\t {self.children}\n")
    visit_children(self.children)

if __name__ == "__main__":
    import sys, os
    prog = open("inputs/" + sys.argv[1]).read()
    ast = parse(prog)

    ast.semantic()
