from schema_ast.ASTNode import ASTNode


class Schema(ASTNode):

    def __init__(self, def_list):
        self.def_list = def_list

    def __str__(self):
        return "schema: " + str([str(def_item) for def_item in self.def_list])
