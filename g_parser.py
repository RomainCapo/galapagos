import ply.yacc as yacc
from g_lexer import tokens
import AST
import os

vars = {}

operations = {
        '>' : lambda x, y: x > y,
        '<' : lambda x, y: x < y,
        '+' : lambda x, y: x + y,
        '-' : lambda x, y: x - y,
    }

def p_programme_statement(p):
    '''programme : statement ';' '''
    p[0] = AST.ProgramNode(p[1])

def p_programme_recursive(p):
    '''programme : statement ';' programme'''
    p[0] = AST.ProgramNode([p[1]] + p[3].children)

def p_statement(p):
    '''statement : assignation
        | structure'''
    p[0] = p[1]

def p_tq_structure(p):
    '''structure : TQ expression '{' programme '}' '''
    p[0] = AST.TqNode([p[2], p[4]])

def p_si_structure(p):
    '''structure : SI expression '{' programme '}' '''
    p[0] = AST.SiNode([p[2], p[4]])

def p_expression_algebric_op(p):
    '''expression : expression ALGEBRAIC_OP expression'''
    p[0] = AST.OpNode(p[2], [p[1], p[3]])

def p_expression_num_or_var(p):
    '''expression : NUMBER
        | IDENTIFIER'''
    p[0] = AST.TokenNode(p[1])

def p_assign(p):
    '''assignation : ENTIER IDENTIFIER '=' expression
        | GALAPAGOS IDENTIFIER '=' expression expression expression expression
        | TORTUE IDENTIFIER '=' expression expression expression expression'''

    if len(p) == 8:
        p[0] = AST.AssignNode([AST.TokenNode([p[1], p[2]]), p[4], p[5], p[6], p[7]])
    else:
        p[0] = AST.AssignNode([AST.TokenNode([p[1], p[2]]), p[4]])

def p_statement_avancer(p):
    '''statement : AVANCER expression expression'''
    p[0] = AST.AvancerNode([p[2], p[3]])

def p_statement_reculer(p):
    '''statement : RECULER expression expression'''
    p[0] = AST.ReculerNode([p[2], p[3]])

def p_statement_tourner_gauche(p):
    '''statement : TOURNERGAUCHE expression expression'''
    p[0] = AST.TournerGaucheNode([p[2], p[3]])

def p_statement_tourner_droite(p):
    '''statement : TOURNERDROITE expression expression'''
    p[0] = AST.TournerDroiteNode([p[2], p[3]])

def p_statement_decoller(p):
    '''statement : DECOLLER expression'''
    p[0] = AST.DecollerNode(p[2])

def p_statement_atterrir(p):
    '''statement : ATTERRIR expression'''
    p[0] = AST.AtterrirNode(p[2])

def p_statement_position_x(p):
    '''expression : POSITIONX '(' expression ')' '''
    p[0] = AST.PositionXNode(p[3])

def p_statement_position_y(p):
    '''expression : POSITIONY '(' expression ')' '''
    p[0] = AST.PositionYNode(p[3])

def p_error(p):
    if p:
        print(f"Syntax error in line {p.lineno}")
        parser.errok()
        raise Exception(f'''\n\nError in line {p.lineno}: Incorrect {p.type}: '{p.value}'.\nMaybe you should check the number of arguments you wrote, or maybe you forgot to end with ';', or maybe it's something else, idk...''')
    else:
        raise Exception(f"\nSyntax error: unexpected end of file!")

if not os.path.exists('generated'):
    os.makedirs('generated')

def parse(program):
    return yacc.parse(program)

parser = yacc.yacc(outputdir='generated')
