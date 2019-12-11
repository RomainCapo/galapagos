import ply.lex as lex
import sys

reserved_words = (
    'SI',
    'TQ',
    'GALAPAGOS',
    'TORTUE',
    'ENTIER',
    'AVANCER',
    'RECULER',
    'TOURNERGAUCHE',
    'TOURNERDROITE',
    'DECOLLER',
    'ATTERRIR',
    'POSITIONX',
    'POSITIONY',
)

tokens = (
    'NUMBER',
    'IDENTIFIER',
    'COMMENTS',
    'ALGEBRAIC_OP',
) + tuple(map(lambda s:s.upper(), reserved_words))

literals = '();={},'

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_IDENTIFIER(t):
    r'[a-zA-Z_]\w*'
    if t.value.upper() in reserved_words:
        t.type = t.value.upper()
    return t

def t_COMMENTS(t):
    r'//.*\n'
    t.lexer.lineno += 1
    # Pas de retourne car non utilisé par l'analyseur syntaxique

def t_ALGEBRAIC_OP(t):
    r'[><+\-*/]'
    return t

def t_ADD_OP(t):
	r'[+-]'
	return t

def t_MUL_OP(t):
	r'[*/]'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Illegal character {repr(t.value[0])}")
    sys.exit(1)

t_ignore = ' \t'

lex.lex()
