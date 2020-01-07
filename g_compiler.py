import AST
from AST import addToClass
from g_parser import parse
from g_semantic import semantic
import logging
import argparse

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
    elif var_type == "REASSIGN":
        js_code += "{0} = {1}".format(var_name, self.children[1].compile())

    return js_code

@addToClass(AST.AvancerNode)
def compile(self):
    return "animator.animate({0}.moveStraight.bind({0}), {1})".format(self.children[0].compile(), self.children[1].compile())

@addToClass(AST.ReculerNode)
def compile(self):
    return "animator.animate({0}.moveBack.bind({0}), {1})".format(self.children[0].compile(), self.children[1].compile())

@addToClass(AST.DecollerNode)
def compile(self):
    return "animator.animate({0}.takeOff.bind({0}), null)".format(self.children[0].compile())

@addToClass(AST.AtterrirNode)
def compile(self):
    return "animator.animate({0}.landing.bind({0}), null)".format(self.children[0].compile())

@addToClass(AST.TournerGaucheNode)
def compile(self):
    return "animator.animate({0}.turnLeft.bind({0}), {1})".format(self.children[0].compile(), self.children[1].compile())

@addToClass(AST.TournerDroiteNode)
def compile(self):
    return "animator.animate({0}.turnRight.bind({0}), {1})".format(self.children[0].compile(), self.children[1].compile())

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

def read_cli_args():
    LOGGER_LEVELS = [
        logging.NOTSET,
        logging.DEBUG,
        logging.INFO,
        logging.WARNING,
        logging.ERROR,
        logging.CRITICAL
    ]

    parser = argparse.ArgumentParser(description='Compile a galapagos code file')
    parser.add_argument('-d', '--debug-level', required=False, type=int, choices=range(0, 6),
                        default=5,
                        help="""logger level : \n
                        [0] -> NOTSET \n
                        [1] -> DEBUG \n
                        [2] -> INFO \n
                        [3] -> WARNING \n
                        [4] -> ERROR \n
                        [5] -> CRITICAL""")
    parser.add_argument('-r', '--run', required=False, default=False, help='run the input code', action='store_true')
    parser.add_argument('-f', '--file', required=True, help="input file path")

    args = parser.parse_args()
    return LOGGER_LEVELS[args.debug_level], args.file, args.run


if __name__ == "__main__":
    import sys, os

    debug_level, file_path, run_browser = read_cli_args()
    print(debug_level)
    logging.basicConfig()
    logger = logging.getLogger('compiler')
    logger.setLevel(debug_level)
    #logger.addHandler(logging.StreamHandler())

    try:
        # DEBUG = True if len(sys.argv) == 3 and sys.argv[2].upper() == 'DEBUG' else False
        # TODO : Get log level as cli argument
        # TODO : Set open web as cli argument
        BASE_DIR = "outputs/pdf/"

        prog = open(file_path).read()
        logger.info("\n## PARSING: start")
        ast = parse(prog)

        graph = ast.makegraphicaltree()

        path_name = BASE_DIR + os.path.splitext(sys.argv[1])[0].split("/")[-1] + '-ast.pdf'
        graph.write_pdf(path_name)
        logger.debug(f"{ast}")
        logger.info("## PARSING: end - success")
        logger.info(f"wrote ast to : {path_name}")

        logger.info("## SEMANTIC: start")
        #ast.semantic()
        logger.info("## SEMANTIC: end - success")

        compiled = "let context = document.getElementById('canvas').getContext('2d');\n"
        compiled += "let animator = new Animator();\n"
        logger.info("## COMPILER: start")
        compiled += ast.compile()
        compiled += "animator.animationsDone();"
        logger.debug(compiled)
        logger.info("## COMPILER: end - success")

        BASE_OUTPUT_DIR = "outputs/"
        OUTPUT_FILENAME = "compiled_code.js"
        name = BASE_OUTPUT_DIR + OUTPUT_FILENAME
        outfile = open(name, 'w')
        outfile.write(compiled)
        outfile.close()
        logger.info(f"Wrote code to : {name}")

        if run_browser:
            logger.info("Opening " + os.path.realpath("ouputs\Galapagos.html") + " ...")
            import webbrowser
            webbrowser.open_new_tab('file://' + os.path.realpath("outputs/Galapagos.html"))

        sys.exit(0)
    except BaseException as be:
        logger.error(be)
        sys.exit(1)
