from schema_ast.ASTNode import ASTNode


class FieldDef(ASTNode):

    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def __str__(self):
        return "(FieldDef name:" + self.name + ")"
