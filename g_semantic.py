import AST
from AST import addToClass, OpNode
from g_bodyguard import Bodyguard, Galapagos, Turtle
import logging

logger = logging.getLogger('compiler')

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
bodyguard = Bodyguard()

def assign_cache(children):
    '''
    When a new variable is declared, add it to the dictionnary (cache).
    Raise an error if a variable with this name already exists.
    '''

    identifier = children[0].tok[1]
    d_type = children[0].tok[0]
    coords = children[1:]

    if identifier in cache:
        if d_type == 'REASSIGN':#If a node is a Reassign node, we put the new variable value in the dict
            if cache[identifier]['type'].upper().strip() == "Entier".upper().strip():#Only interger type can be reassign
               cache[identifier]['variable'] = coords[0]
            else:# With an other type than Integer that throw up an error.
                 raise Exception(f"Error: Redefinition of '{identifier}'. Check your grammar yo")
        else:
            raise Exception(f"Error: Redefinition of '{identifier}'. Check your grammar yo")
    else:
        if d_type == 'Galapagos':
            galapagos = Galapagos(*[x.tok for x in coords])
            bodyguard.add_galapagos(identifier, galapagos)
            cache[identifier] = {"type" : d_type, "variable": galapagos}
        elif d_type == 'Tortue':
            turtle = Turtle(identifier, *[x.tok for x in coords])
            bodyguard.add_turtle(identifier, turtle)
            cache[identifier] = {"type" : d_type, "variable": turtle}
        elif d_type == "Entier":
            cache[identifier] = {"type" : "Entier", "variable": coords[0]}

allowed_types = {
    'Galapagos': [[int, float, 'Entier'], [int, float, 'Entier'], [int, float, 'Entier'], [int, float, 'Entier']],
    'Tortue': [['Galapagos'], [int, float, 'Entier'], [int, float, 'Entier'], [int, float, 'Entier']],
    'Avancer': [['Tortue'], [int, float, 'Entier']],
    'Reculer': [['Tortue'], [int, float, 'Entier']],
    'TournerGauche': [['Tortue'], [int, float, 'Entier']],
    'TournerDroite': [['Tortue'], [int, float, 'Entier']],
    'Decoller':  [['Tortue']],
    'Atterrir': [['Tortue']],
    'Entier': [[int, float]],
    'REASSIGN' : [[int, float]]
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
        main_type: Tortue'''

    for i, identifier in enumerate(identifiers):
        if identifier.tok in cache:
            if cache[identifier.tok]["type"] not in allowed_types[main_type][i]:
                logger.warning(f"\n\t Warning : Instruction '{main_type}' expected as parameter at pos {i+1} one of those types: {allowed_types[main_type][i]}."\
                    f"\n\t'{identifier.tok}' ({cache[identifier.tok]}) given.")
        else:
            if type(identifier.tok) not in allowed_types[main_type][i]:
                logger.warning(f"\n\t Warning : Instruction '{main_type}' expected as parameter at pos {i+1} one of those types: {allowed_types[main_type][i]}."\
                    f"\n\t'{identifier.tok}' ({type(identifier.tok) if type(identifier.tok) is not str else 'unknown identifier'}) given.")


def get_simple_node_value(node):
    '''
    Get the node value in the node is a variable or a Position function, otherwise return the integer value
    :param AST.TokenNode node: node to evaluate
    :return int: return the int value of the node
    '''
    val = node.tok
    if isinstance(node, AST.PositionXNode):
        val = bodyguard.dict_turtle[node.children[0].tok].x
    elif isinstance(node, AST.PositionYNode):
        val = bodyguard.dict_turtle[node.children[0].tok].y
    elif val in cache:
        val = cache[val]["variable"].tok
    return val

def eval_node_recursively(node):
    '''
    Compute the node value recursively. Useful for OpNode object.
    :param AST.TokenNode: node to evaluate
    :return string: evaluated node in string format
    '''

    if isinstance(node.children[1], AST.OpNode):
        right_value = node.children[1]
        left_value = get_simple_node_value(node.children[0])

        return str(left_value) + node.op + eval_node_recursively(right_value)

    left_value = get_simple_node_value(node.children[0])
    right_value = get_simple_node_value(node.children[1])

    return str(left_value) + node.op + str(right_value)

def compute_node_value(node):
    '''
    Get the value from a simple node or a recursive node.
    :param AST.TokenNode node: node object
    :return int: int node value
    '''
    val = None
    if isinstance(node, AST.OpNode):
        val = int(eval(eval_node_recursively(node)))
    else :
        val = get_simple_node_value(node)
    return val

def visit_children(children):
    if len(children) > 0:
        for child in children:
            child.semantic()

@addToClass(AST.ProgramNode)
def semantic(self):
    logger.debug(f"Program node\n\t {self.children}\n")
    b = Bodyguard()
    visit_children(self.children)

@addToClass(AST.TokenNode)
def semantic(self):
    logger.debug(f"Token node\n\t {self.children}\n")
    if isinstance(self.tok, list):
        if self.tok[0] == "Entier":
            val = eval_node_recursively(self)
            print("IS entier", val)
    visit_children(self.children)

@addToClass(AST.OpNode)
def semantic(self):
    self.tok = int(eval(eval_node_recursively(self)))
    self.children = []
    logger.debug(f"Op node\n\t {self.children}\n")

@addToClass(AST.AssignNode)
def semantic(self):
    logger.debug(f"Assign node\n\t {self.children}\n")
    assign_cache(self.children) #example: assign_cache(Tortue, t)
    visit_children(self.children)
    '''for i, child in enumerate(self.children[1:]):
        self.children[i+1].tok = compute_node_value(child)

    check_type(self.children[1:], self.children[0].tok[0]) #example: check_type([0, 10, 50, 50], Galapagos)'''

@addToClass(AST.AvancerNode)
def semantic(self):
    logger.debug(f"Avancer node\n\t {self.children}\n")
    visit_children(self.children)
    print("CHILDREN :", self.children[1].__dict__)
    check_type(self.children, 'Avancer')
    bodyguard.dict_turtle[self.children[0].tok].move_straight(self.children[1].tok)

@addToClass(AST.ReculerNode)
def semantic(self):
    logger.debug(f"Reculer node\n\t {self.children}\n")

    check_type(self.children, 'Reculer')
    visit_children(self.children)
    bodyguard.dict_turtle[self.children[0].tok].move_back(self.children[1].tok)

@addToClass(AST.DecollerNode)
def semantic(self):
    logger.debug(f"Decoller node\n\t {self.children}\n")
    check_type(self.children, 'Decoller')

@addToClass(AST.AtterrirNode)
def semantic(self):
    logger.debug(f"Atterrir node\n\t {self.children}\n")
    check_type(self.children, 'Atterrir')

@addToClass(AST.TournerGaucheNode)
def semantic(self):
    logger.debug(f"Tourner gauche node\n\t {self.children}\n")

    check_type(self.children, 'TournerGauche')
    visit_children(self.children)
    bodyguard.dict_turtle[self.children[0].tok].turn_left(self.children[1].tok)

@addToClass(AST.TournerDroiteNode)
def semantic(self):
    logger.debug(f"Tourner droite node\n\t {self.children}\n")

    check_type(self.children, 'TournerDroite')
    visit_children(self.children)
    bodyguard.dict_turtle[self.children[0].tok].turn_right(self.children[1].tok)

@addToClass(AST.PositionXNode)
def semantic(self):
    logger.debug(f"Position x node\n\t {self.children}")
    check_type(self.children[0])

@addToClass(AST.PositionYNode)
def semantic(self):
    logger.debug(f"Position y node\n\t {self.children}")
    check_type(self.children[0])

@addToClass(AST.TqNode)
def semantic(self):
    logger.debug(f"Tq node\n\t {self.children}\n")
    visit_children(self.children)

@addToClass(AST.SiNode)
def semantic(self):
    logger.debug(f"Si node\n\t {self.children}\n")
    visit_children(self.children)
