from schema_ast.ASTNode import ASTNode


class TypeName(ASTNode):

    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name




