from parsimonious.grammar import Grammar
from SchemaTreeVisitor import SchemaTreeVisitor

grammar = Grammar(
    """
    schema            = wsc? "schema" wsc? LBRACE wsc? def+ RBRACE wsc?
    
    # Schema Definition Language
    def               = type_def / enum_def / union_def / function_def
    
    # Enum Definition
    # ---------------
    enum_def          = KW_ENUM wsc type_name wsc? LBRACE wsc? (literal_enum wsc?)+ RBRACE wsc?
    
    # Union Definition
    # ----------------
    union_def         = KW_UNION wsc type_name wsc? EQUAL wsc? union_type_list wsc?
    union_type_list   = (type_name wsc? BAR wsc?)* type_name
    
    # Type Definition
    # ---------------
    # Format examples:
    #
    #   temperature: Float
    #   temperature: Float @f(a: 1, b: { field1 { field2 }})
    #   # Field arguments with some default values
    #   temperature(offset: Float = 0, scale: String = "f"): Float
    #
    type_def          = KW_TYPE wsc type_name wsc? LBRACE wsc? field_def+ RBRACE wsc?
    field_def         = field_name wsc? (lparen wsc? field_def_arg_list wsc? rparen)? wsc? COLON wsc? 
                        type_spec wsc? declaration? wsc?
    field_def_arg_list = (field_def_arg wsc? COMMA wsc?)* field_def_arg
    field_def_arg      = arg_name wsc? COLON wsc? type_spec wsc? (EQUAL wsc? constant)?
    declaration        = at_sign identifier wsc? lparen wsc? param_list? wsc? rparen wsc?
    param_list         = (param wsc? COMMA wsc?)* param   
    # Declaration parameter passing
    param              = identifier wsc? COLON wsc? expr2 
    expr2              = query / identifier / literal_number / literal_string / var_name
    
    # Function Definition
    # -------------------
    # Format examples:
    #
    #   function GetTransactions(account: String, other: Float): [Transaction!]
    #
    function_def          = KW_FUNCTION wsc? type_name wsc? lparen wsc? function_def_arg_list? wsc? rparen wsc? COLON wsc? 
                            type_spec wsc? 
    function_def_arg_list = (field_def_arg wsc? COMMA wsc?)* field_def_arg

    # Query Language
    # { 
    #    field1
    #    field2 {
    #      subfield1(a: 7, b: $u, c: ENUM_CHOICE_1, d: "izzy!")
    #    }
    #  }    
    query              = LBRACE wsc? (field_sel wsc)+ RBRACE wsc?
    field_sel          = field_name wsc? (lparen wsc? field_sel_arg_list wsc? rparen)? wsc? query?
    field_sel_arg_list = (field_sel_arg wsc? COMMA wsc?)* field_sel_arg
    field_sel_arg      = arg_name wsc? COLON wsc? (constant / var_name / identifier)
    
    type_spec         = (scalar_type_spec / array_type_spec)
    scalar_type_spec  = type_name bang?
    array_type_spec   = lbracket wsc? type_name bang? wsc? rbracket bang?

    # Fundamentals
    type_name         = ~"[A-Z_][A-Z_0-9]*"i
    field_name        = ~"[A-Z_][A-Z_0-9]*"i
    arg_name          = ~"[A-Z_][A-Z_0-9]*"i
    identifier        = ~"[A-Z_][A-Z_0-9]*"i
    var_name          = "$" arg_name
    constant          = literal_string / literal_number / literal_enum
    literal_number    = ~"[0-9]+([.][0-9]+)?"
    # Match everything except quote and newline.  We need two backslashes so
    # that one gets fed into the library.
    literal_string    = DQUOTE ~"[^\\"\\n]*"i DQUOTE
    literal_enum      = ~"[A-Z_][A-Z_0-9]*"i
    # We need two backslashes here since we are in a triple quote.  It
    # is important that the backslash get passed into the library.
    DQUOTE            = "\\u0022"
    KW_TYPE           = "type"
    KW_ENUM           = "enum"
    KW_UNION          = "union"
    KW_FUNCTION       = "function"
    BAR               = "|"
    EQUAL             = "="
    at_sign           = "@"
    LBRACE            = "{"
    RBRACE            = "}"
    lbracket          = "["
    rbracket          = "]"
    lparen            = "("
    rparen            = ")"
    bang              = "!"
    COMMA             = ","
    COLON             = ":"
    
    # Whitespace of arbitrary length
    ws                = ~"[ \\t\\n\\r]"
    # A comment that starts with a pound and goes to the end of the line
    comment           = ~"#.*$"m
    # This is a kind of whitespace that includes comments
    wsc               = (ws / comment)*

    emptyline         = wsc+
    """)

test_document_1 = """ 
# A test schema
schema {
    enum Scales {
      BASE
      TREBLE
    }
    union MultiType = Instrument | Position
    type Instrument { 
      id: ID!
      scale: Scale
      # A comment between fields.  Also demonstrating that the declaration 
      # can be split across lines.
      name: String @derrived(a: 5, b: "henry!", 
        c: 6,
        # Here we are passing the result of a query into the function
        d: { test(fa: 7, bf: $passed_in, g: BASE) { a b } },
        e: $another_passed_in)
      list: [Float!]
      list1(env: MarketEnv): [Float!]
      list2(env1: MarketEnv = 66, env2: MarketEnv = "test%4"): [Float!]
    }
    # A comment between types
    type Position {
      id: ID!
    }
}
"""


test_document_2 = """schema {
    function f0(): [String]
    function f1(a: String!, b: String, c:String): String
    function f2(a: [String]): [String]
}
"""

# Load from file
with open("../../model/risk.graphql", "r") as myfile:
    test_document_3 = myfile.read()

print(grammar.parse(test_document_2))

tree = grammar.parse(test_document_2)
v = SchemaTreeVisitor()
root = v.visit(tree)
print("Root:", root)