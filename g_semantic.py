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
        raise Exception(f"Error: Redefinition of '{identifier}'. Check your grammar yo")

allowed_types = {
    'Galapagos': [[int, float], [int, float], [int, float], [int, float]],
    'Tortue': [['Galapagos'], [int, float], [int, float], [int, float]],
    'Avancer': [['Tortue'], [int, float]],
    'Reculer': [['Tortue'], [int, float]],
    'TournerGauche': [['Tortue'], [int, float]],
    'TournerDroite': [['Tortue'], [int, float]],
    'Decoller':  [['Tortue']],
    'Atterrir': [['Tortue']],
}

def check_type(identifiers, main_type):
    '''
    Verification if identifiers are part of a type that is allowed based on the type of main_type.
    Use dictionnary 'allowed_types' to compare if expected parameters are respected.
    Raise an error if not.

    :param list<AST.TokenNode> identifiers: all variables
    :param string main_type: Type variable

    Example with "Tortue t = g 10 10 0;":
        identifiers: [g, 10, 10, 0]
        main_type: Tortue
    '''
    for i, identifier in enumerate(identifiers):
        if identifier.tok not in cache:
            if type(identifier.tok) not in allowed_types[main_type][i]:
                raise Exception(f"\n\tInstruction '{main_type}' expected as parameter at pos {i+1} one of those types: {allowed_types[main_type][i]}."\
                    f"\n\t'{identifier.tok}' ({type(identifier.tok) if type(identifier.tok) is not str else 'uknown identifier'}) given.")
        else:
            if cache[identifier.tok] not in allowed_types[main_type][i]:                
                raise Exception(f"\n\tInstruction '{main_type}' expected as parameter at pos {i+1} one of those types: {allowed_types[main_type][i]}."\
                    f"\n\t'{identifier.tok}' ({cache[identifier.tok]}) given.")

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
    assign_cache(self.children[0].tok[0], self.children[0].tok[1]) #example: assign_cache(Tortue, t)
    check_type(self.children[1:], self.children[0].tok[0]) #example: check_type([0, 10, 50, 50], Galapagos)

@addToClass(AST.AvancerNode)
def semantic(self):
    print("Avancer node")
    print(f"\t {self.children}\n")
    check_type(self.children, 'Avancer') #example: check_type(['t', 10])

@addToClass(AST.ReculerNode)
def semantic(self):
    print("Reculer node")
    print(f"\t {self.children}\n")
    check_type(self.children, 'Reculer')

@addToClass(AST.DecollerNode)
def semantic(self):
    print("Decoller node")
    print(f"\t {self.children}\n")
    check_type(self.children, 'Decoller')

@addToClass(AST.AtterrirNode)
def semantic(self):
    print("Atterrir node")
    print(f"\t {self.children}\n")
    check_type(self.children, 'Atterrir')

@addToClass(AST.TournerGaucheNode)
def semantic(self):
    print("Tourner gauche node")
    print(f"\t {self.children}\n")
    check_type(self.children, 'TournerGauche')

@addToClass(AST.TournerDroiteNode)
def semantic(self):
    print("Tourner droite node")
    print(f"\t {self.children}\n")
    check_type(self.children, 'TournerDroite')

@addToClass(AST.PositionXNode)
def semantic(self):
    print("Position x node")
    print(f"\n {self.children}")
    print(f"---{self}----")
    check_type(self.children[0])

@addToClass(AST.PositionYNode)
def semantic(self):
    print("Position y node")
    print(f"\n {self.children}")
    print(f"---{self}----")
    check_type(self.children[0])

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
