import AST 
from AST import addToClass
from g_parser import parse

@addToClass(AST.ProgramNode)
def compile(self):
    js_code = ""
    for c in self.children:
        js_code += c.compile()
    return js_code

@addToClass(AST.TokenNode)
def compile(self):
    return self.tok

@addToClass(AST.OpNode)
def compile(self):
    print(self.children)

@addToClass(AST.AssignNode)
def compile(self):
    js_code = ""

    if len(self.children) == 2:
        js_code += "let {0} = {1};\n".format(self.children[0].compile(), self.children[1].compile())
    else:
        var_type = self.children[0].tok[0]
        var_name = self.children[0].tok[1]

        if var_type == "Tortue":
            js_code += "let {0} = new Turtle(context, {1}, {2}, {3}, {4});\n".format(var_name, self.children[1].compile(), self.children[2].compile(), self.children[3].compile(), self.children[4].compile())
        elif var_type == "Galapagos":
            js_code += "let {0} = new Galapagos(context, {1}, {2}, {3}, {4});\n".format(var_name, self.children[1].compile(), self.children[2].compile(), self.children[3].compile(), self.children[4].compile())

    return js_code

@addToClass(AST.AvancerNode)
def compile(self):
    return "{0}.moveStraight({1});\n".format(self.children[0].compile(), self.children[1].compile())

@addToClass(AST.ReculerNode)
def compile(self):
    return "{0}.moveBack({1});\n".format(self.children[0].compile(), self.children[1].compile())

@addToClass(AST.DecollerNode)
def compile(self):
    return "{0}.takeOff();\n".format(self.children[0].compile())

@addToClass(AST.AtterrirNode)
def compile(self):
    return "{0}.landing();\n".format(self.children[0].compile())

@addToClass(AST.TournerGaucheNode)
def compile(self):
    return "{0}.turnLeft({1});\n".format(self.children[0].compile(), self.children[1].compile())

@addToClass(AST.TournerDroiteNode)
def compile(self):
    return "{0}.turnRight({1});\n".format(self.children[0].compile(), self.children[1].compile())

@addToClass(AST.PositionXNode)
def compile(self):
    return "{0}.getPosX();\n".format(self.children[0].compile())

@addToClass(AST.PositionYNode)
def compile(self):
    return "{0}.getPosY();\n".format(self.children[0].compile())

@addToClass(AST.SiNode)
def compile(self):
    js_code = ""
    self.children[0].compile()
    js_code += "if() {\n"
    js_code += "\t" + self.children[1].compile()
    js_code += "}\n"
    return js_code

@addToClass(AST.TqNode)
def compile(self):
    js_code = ""
    pass



if __name__ == "__main__":
    import sys, os
    prog = open(sys.argv[1]).read()
    ast = parse(prog)
    print(ast)
    compiled = "let context = document.getElementById('canvas').getContext('2d');\n"
    compiled += ast.compile()
    print(compiled)

    '''BASE_OUTPUT_DIR = "outputs/"
    OUTPUT_FILENAME = "compiled_code.js"
    name = BASE_OUTPUT_DIR + OUTPUT_FILENAME    
    outfile = open(name, 'w')
    outfile.write(compiled)
    outfile.close()
    print ("Wrote output to", name)'''