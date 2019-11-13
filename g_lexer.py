import ply.lex as lex

reserved_words = (
    'SI',
    'TQ',
    'GALAPAGOS',
    'TORTUE',
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
    'COMPARISON_OP',
) + tuple(map(lambda s:s.upper(), reserved_words))

literals = '();={},'

def t_NUMBER(t):
    r'\d+'
    print("*********")
    print(t.value)
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

def t_COMPARISON_OP(t):
    r'[><]'
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Illegal character {repr(t.value[0])}")
    t.lexer.skip(1)

t_ignore = ' \t'

lex.lex()

if __name__ == "__main__":
    import sys

    prog = open("inputs/" + sys.argv[1]).read()

    lex.input(prog)

    while 1:
        tok = lex.token()
        if not tok: break
        print("line %d: %s(%s)" % (tok.lineno, tok.type, tok.value))
