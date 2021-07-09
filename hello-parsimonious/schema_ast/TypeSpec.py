from schema_ast.ASTNode import ASTNode


class TypeSpec(ASTNode):

    def __init__(self, name, is_vector, is_required):
        self.name = name
        self.is_vector = is_vector
        self.is_required = is_required

    def get_name(self):
        return self.name

    def __str__(self):
        return "(type name:" + self.get_name() + ", is_vector:" + str(self.is_vector) + ", is_required:" \
               + str(self.is_required) + ")"
