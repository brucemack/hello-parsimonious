from schema_ast.ASTNode import ASTNode


class FieldDefArg(ASTNode):

    def __init__(self, name, type_spec):
        self.name = name
        self.type_spec = type_spec

    def get_name(self):
        return self.name

    def __str__(self):
        return "(FieldDefArg name:" + self.name + ", type:" + str(self.type_spec) + ")"
