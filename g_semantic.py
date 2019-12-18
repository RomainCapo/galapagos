import AST
from AST import addToClass

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
    'Galapagos': [[int, float, 'Entier'], [int, float, 'Entier'], [int, float, 'Entier'], [int, float, 'Entier']],
    'Tortue': [['Galapagos'], [int, float, 'Entier'], [int, float, 'Entier'], [int, float, 'Entier']],
    'Avancer': [['Tortue'], [int, float, 'Entier']],
    'Reculer': [['Tortue'], [int, float, 'Entier']],
    'TournerGauche': [['Tortue'], [int, float, 'Entier']],
    'TournerDroite': [['Tortue'], [int, float, 'Entier']],
    'Decoller':  [['Tortue']],
    'Atterrir': [['Tortue']],
    'Entier': [[int, float]]
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

        if identifier.compile() not in cache:
            if type(identifier.compile()) not in allowed_types[main_type][i]:
                raise Exception(f"\n\tInstruction '{main_type}' expected as parameter at pos {i+1} one of those types: {allowed_types[main_type][i]}."\
                    f"\n\t'{identifier.compile()}' ({type(identifier.compile()) if type(identifier.compile()) is not str else 'uknown identifier'}) given.")
        else:
            if cache[identifier.compile()] not in allowed_types[main_type][i]:                
                raise Exception(f"\n\tInstruction '{main_type}' expected as parameter at pos {i+1} one of those types: {allowed_types[main_type][i]}."\
                    f"\n\t'{identifier.compile()}' ({cache[identifier.compile()]}) given.")

def visit_children(children, DEBUG=False):
    for child in children:
        child.semantic(DEBUG=DEBUG)

@addToClass(AST.ProgramNode)
def semantic(self, DEBUG=False):
    print(f"Program node\n\t {self.children}\n") if DEBUG else 0
    visit_children(self.children, DEBUG=DEBUG)

@addToClass(AST.TokenNode)
def semantic(self, DEBUG=False):
    print(f"Token node\n\t {self.children}\n") if DEBUG else 0

@addToClass(AST.OpNode)
def semantic(self, DEBUG=False):
    print(f"Op node\n\t {self.children}\n") if DEBUG else 0

@addToClass(AST.AssignNode)
def semantic(self, DEBUG=False):
    print(f"Assign node\n\t {self.children}\n") if DEBUG else 0
    assign_cache(self.children[0].tok[0], self.children[0].tok[1]) #example: assign_cache(Tortue, t)
    check_type(self.children[1:], self.children[0].tok[0]) #example: check_type([0, 10, 50, 50], Galapagos)

@addToClass(AST.AvancerNode)
def semantic(self, DEBUG=False):
    print(f"Avancer node\n\t {self.children}\n") if DEBUG else 0
    check_type(self.children, 'Avancer') #example: check_type(['t', 10])

@addToClass(AST.ReculerNode)
def semantic(self, DEBUG=False):
    print(f"Reculer node\n\t {self.children}\n") if DEBUG else 0
    check_type(self.children, 'Reculer')

@addToClass(AST.DecollerNode)
def semantic(self, DEBUG=False):
    print(f"Decoller node\n\t {self.children}\n") if DEBUG else 0
    check_type(self.children, 'Decoller')

@addToClass(AST.AtterrirNode)
def semantic(self, DEBUG=False):
    print(f"Atterrir node\n\t {self.children}\n") if DEBUG else 0
    check_type(self.children, 'Atterrir')

@addToClass(AST.TournerGaucheNode)
def semantic(self, DEBUG=False):
    print(f"Tourner gauche node\n\t {self.children}\n") if DEBUG else 0
    check_type(self.children, 'TournerGauche')

@addToClass(AST.TournerDroiteNode)
def semantic(self, DEBUG=False):
    print(f"Tourner droite node\n\t {self.children}\n") if DEBUG else 0
    check_type(self.children, 'TournerDroite')

@addToClass(AST.PositionXNode)
def semantic(self, DEBUG=False):
    print(f"Position x node\n\t {self.children}") if DEBUG else 0
    check_type(self.children[0])

@addToClass(AST.PositionYNode)
def semantic(self, DEBUG=False):
    print(f"Position y node\n\t {self.children}") if DEBUG else 0
    check_type(self.children[0])

@addToClass(AST.TqNode)
def semantic(self, DEBUG=False):
    print(f"Tq node\n\t {self.children}\n") if DEBUG else 0
    visit_children(self.children)

@addToClass(AST.SiNode)
def semantic(self, DEBUG=False):
    print(f"Si node\n\t {self.children}\n") if DEBUG else 0
    visit_children(self.children)