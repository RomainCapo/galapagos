import ply.lex as lex

reserved_words = (
	'SI',
	'TQ',
    'GALAPAGOS',
    'TORTUE',
    'AVANCE',
    'TOURNEGAUCHE',
    'TOURNEDROITE',
    'DECOLLER',
    'ATTERIR',
)

tokens = (
    'NUMBER',
    'IDENTIFIER',
    'VARIABLE',
    'COMMENTS',
	'COMPARISON_OP',
    'AFFECTATION_OP',
    'SEPARATOR',
) + tuple(map(lambda s:s.upper(),reserved_words))

literals = '();={}'

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_IDENTIFIER(t):
	r'[A-Z]+[a-zA-Z]+'
	if t.value in reserved_words:
		t.type = t.value.upper()
	return t

def t_VARIABLE(t):
    r'[A-Za-z]+'
    t.value = str(t.value)
    return t

def t_COMMENTS(t):
	r'//.*\n'
	t.value = str(t.value)
	t.lexer.lineno += 1
	return t

def t_COMPARISON_OP(t):
	r'[><]'
	return t

t_AFFECTATION_OP = '='

t_SEPARATOR = ','

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

    prog = open("../inputs/" + sys.argv[1]).read()

    lex.input(prog)

    while 1:
        tok = lex.token()
        if not tok: break
        print("line %d: %s(%s)" % (tok.lineno, tok.type, tok.value))
