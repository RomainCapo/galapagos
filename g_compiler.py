import AST 
from AST import addToClass
from g_parser import parse
from g_semantic import semantic

@addToClass(AST.ProgramNode)
def compile(self):
    js_code = ""
    for c in self.children:
        js_code += c.compile() + ";\n"
    return js_code

@addToClass(AST.TokenNode)
def compile(self):
    return self.tok

@addToClass(AST.OpNode)
def compile(self):

    return "{0} {1} {2}".format(self.children[0].compile(), self.op, self.children[1].compile())

@addToClass(AST.AssignNode)
def compile(self):
    js_code = ""

    var_type = self.children[0].tok[0]
    var_name = self.children[0].tok[1]

    if var_type == "Tortue":
        js_code += "let {0} = new Turtle(context, {1}, {2}, {3}, {4})".format(var_name, self.children[1].compile(), self.children[2].compile(), self.children[3].compile(), self.children[4].compile())
    elif var_type == "Galapagos":
        js_code += "let {0} = new Galapagos(context, {1}, {2}, {3}, {4})".format(var_name, self.children[1].compile(), self.children[2].compile(), self.children[3].compile(), self.children[4].compile())
    elif var_type == "Entier":
        js_code += "let {0} = {1}".format(var_name, self.children[1].compile())

    return js_code

@addToClass(AST.AvancerNode)
def compile(self):
    return "{0}.moveStraight({1})".format(self.children[0].compile(), self.children[1].compile())

@addToClass(AST.ReculerNode)
def compile(self):
    return "{0}.moveBack({1})".format(self.children[0].compile(), self.children[1].compile())

@addToClass(AST.DecollerNode)
def compile(self):
    return "{0}.takeOff()".format(self.children[0].compile())

@addToClass(AST.AtterrirNode)
def compile(self):
    return "{0}.landing()".format(self.children[0].compile())

@addToClass(AST.TournerGaucheNode)
def compile(self):
    return "{0}.turnLeft({1})".format(self.children[0].compile(), self.children[1].compile())

@addToClass(AST.TournerDroiteNode)
def compile(self):
    return "{0}.turnRight({1})".format(self.children[0].compile(), self.children[1].compile())

@addToClass(AST.PositionXNode)
def compile(self):
    return "{0}.getPosX()".format(self.children[0].compile())

@addToClass(AST.PositionYNode)
def compile(self):
    return "{0}.getPosY()".format(self.children[0].compile())

@addToClass(AST.SiNode)
def compile(self):
    js_code = ""
    js_code += "if({0})".format(self.children[0].compile())
    js_code += "{\n"
    js_code += "\t" + self.children[1].compile()
    js_code += "}"
    return js_code

@addToClass(AST.TqNode)
def compile(self):
    js_code = ""
    js_code += "while({0})".format(self.children[0].compile())
    js_code += "{\n"
    js_code += "\t" + self.children[1].compile()
    js_code += "}"
    return js_code



if __name__ == "__main__":
    import sys, os

    DEBUG = True if len(sys.argv) == 3 and sys.argv[2].upper() == 'DEBUG' else False
    BASE_DIR = "outputs/pdf/"

    prog = open(sys.argv[1]).read()
    print("\n## PARSING: start")
    ast = parse(prog)

    graph = ast.makegraphicaltree()
    
    path_name = BASE_DIR + os.path.splitext(sys.argv[1])[0].split("/")[-1] + '-ast.pdf'
    graph.write_pdf(path_name)
    print("\n"+str(ast)) if DEBUG else 0
    print("\n## PARSING: end - success")
    print("\twrote ast to", path_name)

    print("\n## SEMANTIC: start\n")
    ast.semantic(DEBUG)
    print("## SEMANTIC: end - success\n")

    compiled = "let context = document.getElementById('canvas').getContext('2d');\n"
    print("\n## COMPILER: start\n")
    compiled += ast.compile()
    print(compiled) if DEBUG else 0
    print("## COMPILER: end - success")

    BASE_OUTPUT_DIR = "outputs/"
    OUTPUT_FILENAME = "compiled_code.js"
    name = BASE_OUTPUT_DIR + OUTPUT_FILENAME
    outfile = open(name, 'w')
    outfile.write(compiled)
    outfile.close()
    print ("\tWrote code to", name)

    print("\nOpening " + os.path.realpath("ouputs\Galapagos.html") + " ...")
    import webbrowser
    webbrowser.open_new_tab('file://' + os.path.realpath("outputs/Galapagos.html"))