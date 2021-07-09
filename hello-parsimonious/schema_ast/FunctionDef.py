from schema_ast.ASTNode import ASTNode
from schema_ast.FieldDef import FieldDef


class FunctionDef(ASTNode):

    def __init__(self, name: str, return_type, arg_list: [FieldDef]):
        self.name = name
        self.return_type = return_type
        self.arg_list = arg_list

    def get_name(self):
        return self.name

    def __str__(self):
        return "(FunctionDef name:" + self.name + ", return_type:" + str(self.return_type) + ", arg_list:" + \
               str([str(arg_item) for arg_item in self.arg_list]) + ")"

