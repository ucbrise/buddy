import ast
import astor


class MainVisitor(ast.NodeVisitor):

    def __init__(self):
        self.symbol_table = {}

    def visit_Assign(self, node):
        """
        <name> = <>
        """
        raise SyntaxError(f"Invalid Syntax: {astor.dump_tree(node)}\n")
    
    # def generic_visit(self, node):
    #     # super(MainVisitor, self).generic_visit(node)
    #     raise SyntaxError(f"Invalid Syntax: {astunparse.unparse(node)}\n")
    #     # super(ast.NodeVisitor, self).generic_visit(node)


def parse(path):
    nv = MainVisitor()
    with open(path, 'r') as f:
        tree = ast.parse(f.read())
    nv.visit(tree)