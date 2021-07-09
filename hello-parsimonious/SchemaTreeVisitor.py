from parsimonious.nodes import NodeVisitor
from schema_ast.Schema import Schema
from schema_ast.FunctionDef import FunctionDef
from schema_ast.FieldDef import FieldDef
from schema_ast.FieldDefArg import FieldDefArg
from schema_ast.TypeSpec import TypeSpec

class SchemaTreeVisitor(NodeVisitor):

    def visit_schema(self, node, visited_children):
        _, _, _, _, _, def_list, *_ = visited_children
        return Schema(def_list)

    def visit_def(self, node, visited_children):
        # Passthrough
        return visited_children[0]

    # Function definition stuff

    def visit_function_def(self, node, visited_children):
        _, _, name, _, _, _, arg_def_list, _, _, _, _, _, return_type, *_ = visited_children
        # Since the argument list is optional we have some special handling here
        if not isinstance(arg_def_list, list):
            return FunctionDef(name, return_type, [])
        else:
            return FunctionDef(name, return_type, arg_def_list[0])

    def visit_function_def_arg_list(self, node, visited_children):
        child_list, last_field_def = visited_children
        def_list = []
        for child in child_list:
            def_list.append(child[0])
        def_list.append(last_field_def)
        return def_list

    def visit_type_def(self, node, visited_children):
        _, _, type_name, *_ = visited_children
        print("visit_type_def", type_name.get_name())
        return None

    def visit_field_def(self, node, visited_children):
        name, *_ = visited_children
        print("visit_field_def", name.text)
        return FieldDef(name.text)

    def visit_field_def_arg(self, node, visited_children):
        name, _, _, _, type_spec, *_ = visited_children
        print("visit_field_def_arg", name.text)
        return FieldDefArg(name.text, type_spec)

    def visit_type_spec(self, node, visited_children):
        # A simple pass-through
        return visited_children[0]

    def visit_scalar_type_spec(self, node, visited_children):
        name, bang, *_ = visited_children
        print("visit_scalar_type_spec")
        is_required = isinstance(bang, list)
        return TypeSpec(name, False, is_required)

    def visit_array_type_spec(self, node, visited_children):
        _, _, name, *_ = visited_children
        print("visit_array_type_spec")
        return TypeSpec(name, True, False)

    def visit_declaration(self, node, visited_children):
        _, id, *_ = visited_children
        print("visit_declaration", id.text)
        return None

    def visit_param(self, node, visited_children):
        id, *_ = visited_children
        print("visit_param", id.text)
        return None

    def visit_field_name(self, node, visited_children):
        print("visit_field_name")
        return visited_children or node

    def visit_type_name(self, node, visited_children):
        print("visit_type_name", node.text)
        return node.text

    def visit_identifier(self, node, visited_children):
        print("visit_identifier")
        return visited_children or node

    def visit_literal_string(self, node, visited_children):
        print("visit_literal_string", node.text)
        return visited_children or node

    def visit_literal_number(self, node, visited_children):
        print("visit_literal_number", node.text)
        return None

    def visit_query(self, node, visited_children):
        print("visit_query")
        return None

    def visit_field_arg(self, node, visited_children):
        print("visit_field_arg")
        return None

    def visit_comment(self, node, visited_children):
        print("visit_comment")
        return None


    def generic_visit(self, node, visited_children):
        return visited_children or node
