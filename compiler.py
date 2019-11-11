import AST 
from AST import addToClass
import parser

operations = {
	'+' : 'ADD',
	'-' : 'SUB',
	'*' : 'MUL',
	'/' : 'DIV'
}

@addToClass(AST.ProgramNode)
def compile(self):
    js_code = ""
    for c in self.children:
        js_code += c.compile()
    return js_code

@addToClass(AST.TokenNode)
def compile(self):
	pass

@addToClass(AST.OpNode)
def compile(self):
	pass

@addToClass(AST.AssignNode)
def compile(self):
    js_code = ""
    
    if self.tok[0] == "Tortue":
        js_code += "let {0} = new Turtle(context, {1}, {2}, {3}, {4});\n".format(self.tok[1], self.tok[2], self.tok[3], self.tok[4], self.tok[5])
    elif self.tok[0] == "Galapagos":
        js_code += "let {0} = new Galapagos(context, {1}, {2}, {3}, {4});\n".format(self.tok[1], self.tok[2], self.tok[3], self.tok[4], self.tok[5])
    elif self.tok[0] == "Entier":
        js_code += "let {0} = {1};\n".format(self.tok[1], self.tok[2])

    return js_code

@addToClass(AST.AvancerNode)
def compile(self):
    return "{0}.moveStraight({1});\n".format(self.tok[0], self.tok[1])

@addToClass(AST.ReculerNode)
def compile(self):
    return "{0}.moveBack({1});\n".format(self.tok[0], self.tok[1])

@addToClass(AST.DecollerNode)
def compile(self):
    return "{0}.takeOff();\n".format(self.tok)

@addToClass(AST.AtterrirNode)
def compile(self):
    return "{0}.landing();\n".format(self.tok)

@addToClass(AST.TournerGaucheNode)
def compile(self):
    return "{0}.turnLeft({1});\n".format(self.tok[0], self.tok[1])

@addToClass(AST.TournerDroiteNode)
def compile(self):
    return "{0}.turnRight({1});\n".format(self.tok[0], self.tok[1])

@addToClass(AST.PositionXNode)
def compile(self):
    return "{0}.getPosX();\n".format(self.tok)

@addToClass(AST.PositionYNode)
def compile(self):
    return "{0}.getPosY();\n".format(self.tok)

@addToClass(AST.TqNode)
def compile(self):
    js_code = ""
    pass

@addToClass(AST.SiNode)
def compile(self):
    js_code = ""
    pass

if __name__ == "__main__":
    import sys, os
    prog = open(sys.argv[1]).read()
    ast = parser.parse(prog)
    print(ast)

    compiled = "let context = document.getElementById('canvas').getContext('2d');\n"
    compiled += ast.compile()
    BASE_OUTPUT_DIR = "outputs/"
    OUTPUT_FILENAME = "compiled_code.js"
    name = BASE_OUTPUT_DIR + OUTPUT_FILENAME    
    outfile = open(name, 'w')
    outfile.write(compiled)
    outfile.close()
    print ("Wrote output to", name)