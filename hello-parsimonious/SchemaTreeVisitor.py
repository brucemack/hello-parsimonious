from parsimonious.nodes import NodeVisitor
from schema_ast.TypeName import TypeName

class SchemaTreeVisitor(NodeVisitor):

    def visit_type_def(self, node, visited_children):
        _, _, type_name, *_ = visited_children
        print("visit_type_def", type_name.get_name())
        return None

    def visit_field_def(self, node, visited_children):
        id, *_ = visited_children
        print("visit_field_def", id.text)
        return None

    def visit_declaration(self, node, visited_children):
        _, id, *_ = visited_children
        print("visit_declaration", id.text)
        return None

    def visit_comment(self, node, visited_children):
        print("visit_comment")
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
        return TypeName(node.text)

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

    def generic_visit(self, node, visited_children):
        return visited_children or node
