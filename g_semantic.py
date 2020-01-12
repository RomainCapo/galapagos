import AST
from AST import addToClass
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

is_in_while = False

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
                node_val = compute_node_value(coords[0])
                if not is_in_while:
                    children[1] = AST.TokenNode(node_val)
                cache[identifier]['variable'] = node_val
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
            node_val = compute_node_value(coords[0])
            children[1] = AST.TokenNode(node_val)
            cache[identifier] = {"type" : "Entier", "variable": node_val}

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
        if identifier.compile() in cache:
            if cache[identifier.compile()]["type"] not in allowed_types[main_type][i]:
                logger.warning(f"\n\t Warning : Instruction '{main_type}' expected as parameter at pos {i+1} one of those types: {allowed_types[main_type][i]}."\
                    f"\n\t'{identifier.compile()}' ({cache[identifier.compile()]}) given.")
        else:
            if type(identifier.compile()) not in allowed_types[main_type][i]:
                logger.warning(f"\n\t Warning : Instruction '{main_type}' expected as parameter at pos {i+1} one of those types: {allowed_types[main_type][i]}."\
                    f"\n\t'{identifier.compile()}' ({type(identifier.compile()) if type(identifier.compile()) is not str else 'unknown identifier'}) given.")


def get_simple_node_value(node):
    '''
    Get the node value in the node is a variable or a Position function, otherwise return the integer value
    :param AST.TokenNode node: node to evaluate
    :return int: return the int value of the node
    '''
    val = node.compile()
    if isinstance(node, AST.PositionXNode):
        val = bodyguard.dict_turtle[node.children[0].tok].x
    elif isinstance(node, AST.PositionYNode):
        val = bodyguard.dict_turtle[node.children[0].tok].y
    elif val in cache:
        val = cache[val]["variable"]
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
    for child in children:
        child.parent = children
        child.semantic()
    #if is_in_while:
    return children

@addToClass(AST.ProgramNode)
def semantic(self):
    logger.debug(f"Program node\n\t {self.children}\n")
    b = Bodyguard()
    visit_children(self.children)


@addToClass(AST.TokenNode)
def semantic(self):
    logger.debug(f"Token node\n\t {self.children}\n")

@addToClass(AST.OpNode)
def semantic(self):
    logger.debug(f"Op node\n\t {self.children}\n")

@addToClass(AST.AssignNode)
def semantic(self):
    logger.debug(f"Assign node\n\t {self.children}\n")
    assign_cache(self.children) #example: assign_cache(Tortue, t)

@addToClass(AST.AvancerNode)
def semantic(self):
    logger.debug(f"Avancer node\n\t {self.children}\n")

    node_val = compute_node_value(self.children[1])
    self.children[1]= AST.TokenNode(node_val)
    check_type(self.children, 'Avancer')
    bodyguard.dict_turtle[self.children[0].tok].move_straight(node_val)

@addToClass(AST.ReculerNode)
def semantic(self):
    logger.debug(f"Reculer node\n\t {self.children}\n")

    node_val = compute_node_value(self.children[1])
    self.children[1]= AST.TokenNode(node_val)
    check_type(self.children, 'Reculer')
    bodyguard.dict_turtle[self.children[0].tok].move_back(node_val)

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

    node_val = compute_node_value(self.children[1])
    self.children[1]= AST.TokenNode(node_val)
    check_type(self.children, 'TournerGauche')
    bodyguard.dict_turtle[self.children[0].tok].turn_left(node_val)

@addToClass(AST.TournerDroiteNode)
def semantic(self):
    logger.debug(f"Tourner droite node\n\t {self.children}\n")

    node_val = compute_node_value(self.children[1])
    self.children[1]= AST.TokenNode(node_val)
    check_type(self.children, 'TournerDroite')
    bodyguard.dict_turtle[self.children[0].tok].turn_right(node_val)

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
    logger.debug(f"Tq node\n\t {self.children}\n") # maybe move this debug inside while ?

    global is_in_while
    is_in_while = True
    
    left = compute_node_value(self.children[0].children[0])
    right = compute_node_value(self.children[0].children[1])
    cond = self.children[0].op

    while_s = str(left) + cond + str(right)
    nodes_to_push = []
    while(eval(while_s)):
        nodes_to_push.append(visit_children(self.children))
        left = compute_node_value(self.children[0].children[0])
        right = compute_node_value(self.children[0].children[1])
        while_s = str(left) + cond + str(right)
    
    index_while = [str(type(x)) for x in self.parent].index("<class 'AST.TqNode'>")
    del self.parent[index_while]
    for x in nodes_to_push:
        self.parent[index_while:index_while] = x[1].children
        index_while += 1
    
    is_in_while = False


@addToClass(AST.SiNode)
def semantic(self):
    logger.debug(f"Si node\n\t {self.children}\n")
    
    left = compute_node_value(self.children[0].children[0])
    right = compute_node_value(self.children[0].children[1])
    cond = self.children[0].op

    if_s = str(left) + cond + str(right)
    nodes_to_push = []

    if(eval(if_s)):
        nodes_to_push.append(visit_children(self.children)) 
		
    index_if =  [str(type(x)) for x in self.parent].index("<class 'AST.SiNode'>")
    del self.parent[index_if]

    for x in nodes_to_push:
        self.parent[index_if:index_if] = x[1].children
        index_if += 1
