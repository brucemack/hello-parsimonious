from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor

grammar = Grammar(
    """
    schema            = emptyline* def*
    
    # Schema Definition Language
    def               = (type_def)
    type_def          = kw_type wsc identifier wsc? lbrace wsc? field_def* rbrace wsc?
    
    # Definition of a field in a type.  Format examples:
    #
    #   temperature: Float
    #   temperature: Float @f(a: 1, b: { field1 { field2 }})
    #   temperature(offset: Float = 0, scale: Float): Float
    #
    field_def         = field_name wsc? (lparen wsc? field_arg_list wsc? rparen)? wsc? colon wsc? 
                        (scalar_type / array_type) wsc? declaration? wsc?
    field_arg_list    = (field_arg wsc? comma wsc?)* field_arg
    field_arg         = arg_name wsc? colon wsc? type_name wsc? ("=" wsc? constant)?
    scalar_type       = type_name bang?
    array_type        = lbracket wsc? type_name bang? wsc? rbracket bang?
    declaration       = at_sign identifier wsc? lparen wsc? param_list? wsc? rparen wsc?
    param_list        = (param wsc? comma wsc?)* param   
    # Declaration parameter with optional default values
    param             = identifier wsc? colon wsc? expr2 
    expr2             = query / identifier / literal_number / literal_string
    
    # Query Language
    query             = lbrace wsc? (selector wsc)+ rbrace wsc?
    selector          = identifier wsc? query?
    
    # Fundamentals
    type_name         = ~"[A-Z_][A-Z_0-9]*"i
    field_name        = ~"[A-Z_][A-Z_0-9]*"i
    arg_name          = ~"[A-Z_][A-Z_0-9]*"i
    identifier        = ~"[A-Z_][A-Z_0-9]*"i
    constant          = literal_string / literal_number
    literal_number    = ~"[0-9]+([.][0-9]+)?"
    literal_string    = dquote text_no_quote dquote
    text              = ~"[A-Za-z0-9 _]*"i
    # Match everything except quote and newline
    text_no_quote     = ~"[^\\"\\n]*"i
    # We need two backslashes here since we are in a tripple quote.  It
    # is important that the backslash get passed into the library.
    dquote            = "\\u0022"
    kw_type           = "type"
    at_sign           = "@"
    lbrace            = "{"
    rbrace            = "}"
    lbracket          = "["
    rbracket          = "]"
    lparen            = "("
    rparen            = ")"
    bang              = "!"
    comma             = ","
    colon             = ":"
    
    # Whitespace of arbitrary length
    ws                = ~"\s*"
    # A comment that starts with a pound and goes to the end of the line
    comment           = ~"#.*$"m
    # This is a kind of whitespace that includes comments
    wsc               = (comment / ws)*

    emptyline         = wsc+
    """)

test_document = """
# Test comment
type Instrument { 
  id: ID!
  # Useful comment
  name: String @derrived(a: 5, b: "henry!", c: 6 ,d : { test { a b } })
  list: [Float!]
  list1(env: MarketEnv): [Float!]
  list2(env1: MarketEnv = 66, env2: MarketEnv = "test%4"): [Float!]
}
type Position {
  id: ID
}
"""

print(grammar.parse(test_document))


# Demonstrate visitation
class Visitor(NodeVisitor):

    def visit_type_def(self, node, visited_children):
        _, _, id, *_ = visited_children
        print("visit_type_def", id.text)
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
        print("visit_type_name")
        return visited_children or node

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

tree = grammar.parse(test_document)
v = Visitor()
v.visit(tree)
