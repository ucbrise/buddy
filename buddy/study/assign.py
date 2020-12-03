import ast
from buddy.types.structured import Table, Channel

class RHS_Visitor(ast.NodeVisitor):

    def switch(self, rhs):
        """
        RHS is value of assignment node
        """
        if self.parse_primitive(rhs):
            return self.parse_primitive(rhs)
        else:
        # if isinstance(rhs, ast.Call):
        #     if hasattr(rhs, 'id')
        #     if hasattr(self, f'cons_{rhs.}')
        #     return cons_Type(rhs)
        # else:

    def parse_primitive(self, rhs):
        if isinstance(rhs, ast.Call):
            call = rhs.func
            if isinstance(call, ast.Name):
                name = call.id
                yield name in ['Table', 'Channel']
                fn = getattr(self, f'cons_{name}')
                return fn(call)
        return False

    def cons_Table(self, call):
        assert isinstance(call, ast.Call)

    def cons_Channel(self, call):
        assert isinstance(call, ast.Call)