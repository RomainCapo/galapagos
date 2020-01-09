import AST

class Evaluator:

    def __init__(self):
        self.cache = {}

    def _get_val_from_node(self, node):
        val = node
        if isinstance(val, str):
            val = self.cache[val]["variable"].compile()
        return val

    def eval_op_node(self, node):
        if isinstance(node.children[1], AST.OpNode):

            right_value = node.children[1]
            left_value = self._get_val_from_node(node.children[0].compile())

            return str(left_value) + node.op + self.eval_op_node(right_value)

        left_value = self._get_val_from_node(node.children[0].compile())
        right_value = self._get_val_from_node(node.children[1].compile())

        return str(left_value) + node.op + str(right_value)
