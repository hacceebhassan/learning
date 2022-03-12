import os
import sys
import php_lex
import ply.yacc as yacc


tokens = php_lex.tokens

precedence = (
    ('left', 'INCLUDE', 'INCLUDE_ONCE', 'EVAL', 'REQUIRE', 'REQUIRE_ONCE'),
    ('left', 'COMMA'),
    ('left', 'LOGICAL_OR'),
    ('left', 'LOGICAL_XOR'),
    ('left', 'LOGICAL_AND'),
    ('right', 'PRINT'),
    ('left', 'EQUALS', 'PLUS_EQUAL', 'MINUS_EQUAL', 'MUL_EQUAL', 'DIV_EQUAL', 'CONCAT_EQUAL',
     'MOD_EQUAL', 'AND_EQUAL', 'OR_EQUAL', 'XOR_EQUAL', 'SL_EQUAL', 'SR_EQUAL'),
    ('left', 'QUESTION', 'COLON'),
    ('left', 'BOOLEAN_OR'),
    ('left', 'BOOLEAN_AND'),
    ('left', 'OR'),
    ('left', 'XOR'),
    ('left', 'AND'),
    ('nonassoc', 'IS_EQUAL_TO', 'IS_NOT_EQUAL', 'IS_IDENTICAL', 'IS_NOT_IDENTICAL'),
    ('nonassoc', 'LESS_THAN', 'LESS_THAN_OR_EQUAL',
     'GREATER_THAN', 'GRATER_THAN_OR_EQUAL', 'SPACESHIP'),
    ('left', 'SL', 'SR'),
    ('left', 'PLUS', 'MINUS', 'CONCAT'),
    ('left', 'MUL', 'DIV', 'MOD'),
    ('right', 'BOOLEAN_NOT'),
    ('nonassoc', 'INSTANCEOF'),
    ('right', 'NOT', 'INC', 'DEC', 'INT_CAST', 'DOUBLE_CAST', 'STRING_CAST',
     'ARRAY_CAST', 'BOOL_CAST', 'UNSET_CAST', 'BINARY_CAST', 'AT'),
    ('right', 'LBRACKET'),
    ('nonassoc',  'CLONE'),
    ('nonassoc', 'LOWER_THAN_ELSE', 'LOWER_THAN_ELSEIF'),
    ('nonassoc', 'ELSE', 'ELSEIF'),
    ('left', 'ENDIF'),
    ('right', 'STATIC'),
)



def p_start(p):
    'start : top_statement_list'
    print("The PHP code is syntactically correct")
    pass


def p_top_statement_list(p):
    '''top_statement_list : top_statement_list top_statement
                          | empty'''
    pass


def p_top_statement(p):
    '''top_statement : statement
                     | function_declaration_statement
                     | HALT_COMPILER LPAREN RPAREN SEMI_COLON
                     | CONST constant_declarations SEMI_COLON'''
    pass


def p_constant_declartions(p):
    ''' constant_declarations : constant_declarations COMMA constant_declaration
                             | constant_declaration'''
    pass


def p_constant_declaration(p):
    '''constant_declaration : IDENTIFIER EQUALS static_expr'''
    pass


def p_inner_statment_list(p):
    ''' inner_statement_list : inner_statement_list inner_statement
                            | empty'''
    pass


def p_inner_statment(p):
    ''' inner_statement : statement
                       | function_declaration_statement'''
    pass


def p_inner_statement_yield(p):
    ''' inner_statement : YIELD SEMI_COLON
                       | YIELD expr SEMI_COLON'''
    pass


def p_statement_block(p):
    '''statement : LBRACE inner_statement_list RBRACE '''
    pass


def p_statement_if(p):
    '''statement : IF LPAREN expr RPAREN statement elseif_list     %prec LOWER_THAN_ELSE
                 |  IF LPAREN expr RPAREN statement elseif_list ELSE statement  
                 | IF LPAREN expr RPAREN COLON inner_statement_list new_elseif_list new_else_single ENDIF SEMI_COLON '''
    # print("reached if")

    pass


def p_statement_while(p):
    ''' statement : WHILE LPAREN expr RPAREN while_statement'''
    pass


def p_statement_do_while(p):
    '''statement : DO statement WHILE LPAREN expr RPAREN SEMI_COLON'''
    pass


def p_statement_for(p):
    ''' statement : FOR LPAREN for_expr SEMI_COLON for_expr SEMI_COLON for_expr RPAREN for_statement'''
    pass


def p_statement_switch(p):
    '''statement : SWITCH LPAREN expr RPAREN switch_case_list '''
    pass


def p_statement_break(p):
    '''statement : BREAK SEMI_COLON
                 | BREAK expr SEMI_COLON '''
    pass


def p_statement_continue(p):
    '''statement : CONTINUE SEMI_COLON
                 | CONTINUE expr SEMI_COLON '''
    pass


def p_statement_return(p):
    '''statement : RETURN SEMI_COLON
                 | RETURN expr SEMI_COLON '''
    pass


def p_statement_global(p):
    ''' statement : GLOBAL global_var_list SEMI_COLON'''
    pass


def p_statement_static(p):
    ''' statement : STATIC static_var_list SEMI_COLON'''
    pass


def p_statement_echo(p):
    '''statement : ECHO echo_expr_list SEMI_COLON '''
    


def p_statement_inline_html(p):
    ''' statement : INLINE_HTML'''
    


def p_statement_expr(p):
    ''' statement : expr SEMI_COLON'''
    


def p_statement_unset(p):
    '''statement : UNSET LPAREN unset_variables RPAREN SEMI_COLON '''
    pass


def p_statement_empty_stmt(p):
    '''statement : SEMI_COLON '''
    pass


def p_elif_list(p):
    '''elseif_list : empty     %prec LOWER_THAN_ELSEIF
                   | elseif_list ELSEIF LPAREN expr RPAREN statement'''
    pass


def p_new_elseif_list(p):
    ''' new_elseif_list : empty
                       | new_elseif_list ELSEIF LPAREN expr RPAREN COLON inner_statement_list'''
    pass


def p_new_else_single(p):
    '''new_else_single : empty
                       | ELSE COLON inner_statement_list '''
    pass


def p_while_statement(p):
    '''while_statement : statement
                       | COLON inner_statement_list ENDWHILE SEMI_COLON '''
    pass


def p_for_expr(p):
    '''for_expr : empty
                | non_empty_for_expr '''
    pass


def p_nonempty_for_expr(p):
    '''non_empty_for_expr : non_empty_for_expr COMMA expr
                          | expr '''
    pass


def p_for_statement(p):
    '''for_statement : statement
                     | COLON inner_statement_list ENDFOR SEMI_COLON '''
    pass


def p_switch_case_list(p):
    '''switch_case_list : LBRACE case_list RBRACE
                        | LBRACE SEMI_COLON case_list RBRACE '''

    pass


def p_switch_case_list_colon(p):
    '''switch_case_list : COLON case_list ENDSWITCH SEMI_COLON
                        | COLON SEMI_COLON case_list ENDSWITCH SEMI_COLON '''
    pass


def p_case_list(p):
    '''case_list : empty
                 | case_list_no_default CASE expr case_separator inner_statement_list
                 | case_list_no_default DEFAULT case_separator inner_statement_list '''
 # added case_list_no_default
    pass


def p_case_list_no_default(p):
    '''case_list_no_default : empty
                            | case_list_no_default CASE expr case_separator inner_statement_list '''
    pass


def p_case_separator(p):
    '''case_separator : COLON
                      | SEMI_COLON '''
    pass


def p_global_var_list(p):
    '''global_var_list : global_var_list COMMA global_var
                       | global_var '''
    pass


def p_global_var(p):
    '''global_var : VARIABLE
                  | DOLLAR variable
                  | DOLLAR LBRACE expr RBRACE '''
    pass


def p_static_var_list(p):
    '''static_var_list : static_var_list COMMA static_var
                       | static_var '''
    pass


def p_static_var(p):
    '''static_var : VARIABLE EQUALS static_scalar
                  | VARIABLE '''
    pass


def p_echo_expr_list(p):
    '''echo_expr_list : echo_expr_list COMMA expr
                      | expr '''
    pass


def p_unset_variables(p):
    '''unset_variables : unset_variables COMMA unset_variable
                       | unset_variable '''
    pass


def p_unset_variable(p):
    '''unset_variable : variable '''
    pass


def p_function_declaration_statment(p):
    '''function_declaration_statement : FUNCTION is_reference IDENTIFIER LPAREN parameter_list RPAREN LBRACE inner_statement_list RBRACE '''
    pass


def p_is_reference(p):
    '''is_reference : AND
                    | empty '''
    pass


def p_parameter_list(p):
    '''parameter_list : non_empty_parameter_list 
                      | empty '''
    pass


def p_non_empty_parameter_list(p):
    '''non_empty_parameter_list : non_empty_parameter_list COMMA parameter 
                                | parameter'''
    pass


def p_parameter(p):
    '''parameter : VARIABLE
                 | AND VARIABLE
                 | VARIABLE EQUALS static_scalar
                 | AND VARIABLE EQUALS static_scalar '''
    pass


def p_expr_variable(p):
    'expr : variable'
    pass


def p_expr_assign(p):
    '''expr : variable EQUALS expr
            | variable EQUALS AND expr '''
    pass


def p_expr_clone(p):
    'expr : CLONE expr'
    pass


def p_expr_list_assign(p):
    'expr : LIST LPAREN assignment_list RPAREN EQUALS expr'
    pass


def p_assignment_list(p):
    '''assignment_list : assignment_list COMMA assignment_list_element
                       | assignment_list_element'''
    pass


def p_assignment_list_element(p):
    '''assignment_list_element : variable
                               | empty
                               | LIST LPAREN assignment_list RPAREN'''
    pass


def p_variable(p):
    'variable :  base_variable_with_function_calls'
    pass


def p_base_variable_with_function_calls(p):
    '''base_variable_with_function_calls : base_variable
                                         | function_call'''
    pass


def p_function_call(p):
    ''' function_call : IDENTIFIER fucntion_call_body
                        '''
    pass


def p_function_call_body(p):
    ''' fucntion_call_body : LPAREN function_call_parameter_list RPAREN
                             '''


def p_function_call_variable(p):
    '''function_call : variable_without_objects LPAREN function_call_parameter_list RPAREN
                    '''
    pass




def p_base_variable(p):
    'base_variable : compound_variable'
    pass




def p_expr_string_offset(p):
    'expr : expr LBRACE dim_offset RBRACE'
    pass


def p_compound_variable(p):
    '''compound_variable : VARIABLE
                         | DOLLAR LBRACE expr RBRACE'''
    pass


def p_dim_offset(p):
    '''dim_offset : expr
                  | empty'''
    pass


def p_variable_without_objects(p):
    
    'variable_without_objects : compound_variable'
    pass


def p_expr_scalar(p):
    'expr : scalar'
    pass


def p_expr_array(p):
    '''expr : ARRAY LPAREN array_pair_list RPAREN
            | LBRACKET array_pair_list RBRACKET'''
    pass


def p_array_pair_list(p):
    '''array_pair_list : empty
                       | non_empty_array_pair_list possible_comma'''
    pass




def p_non_empty_array_pair_list_pair(p):
    '''non_empty_array_pair_list : non_empty_array_pair_list COMMA expr DOUBLE_ARROW AND variable
                                 | non_empty_array_pair_list COMMA expr DOUBLE_ARROW expr
                                 | expr DOUBLE_ARROW AND variable
                                 | expr DOUBLE_ARROW expr'''
    pass



def p_possible_comma(p):
    '''possible_comma : empty
                      | COMMA'''
    pass


def p_function_call_parameter_list(p):
    '''function_call_parameter_list : function_call_parameter_list COMMA function_call_parameter
                                    | function_call_parameter'''
                                    

def p_function_call_parameter_list_empty(p):
    'function_call_parameter_list : empty'


def p_function_call_parameter(p):
    '''function_call_parameter : expr
                               | AND variable'''
    pass


def p_expr_function(p):
    'expr : FUNCTION is_reference LPAREN parameter_list RPAREN LBRACE inner_statement_list RBRACE'
    pass


def p_expr_assign_op(p):
    '''expr : variable PLUS_EQUAL expr
            | variable MINUS_EQUAL expr
            | variable MUL_EQUAL expr
            | variable DIV_EQUAL expr
            | variable CONCAT_EQUAL expr
            | variable MOD_EQUAL expr
            | variable AND_EQUAL expr
            | variable OR_EQUAL expr
            | variable XOR_EQUAL expr
            | variable SL_EQUAL expr
            | variable SR_EQUAL expr'''
    pass


def p_expr_binary_op(p):
    '''expr : expr BOOLEAN_AND expr
            | expr BOOLEAN_OR expr
            | expr LOGICAL_AND expr
            | expr LOGICAL_OR expr
            | expr LOGICAL_XOR expr
            | expr AND expr
            | expr OR expr
            | expr XOR expr
            | expr CONCAT expr
            | expr PLUS expr
            | expr MINUS expr
            | expr MUL expr
            | expr DIV expr
            | expr SL expr
            | expr SR expr
            | expr MOD expr
            | expr IS_IDENTICAL expr
            | expr IS_NOT_IDENTICAL expr
            | expr IS_EQUAL_TO expr
            | expr IS_NOT_EQUAL expr
            | expr LESS_THAN expr
            | expr LESS_THAN_OR_EQUAL expr
            | expr GREATER_THAN expr
            | expr GRATER_THAN_OR_EQUAL expr
            | expr INSTANCEOF expr
            | expr SPACESHIP expr
            | expr INSTANCEOF STATIC'''
    # print("reached")
    pass


def p_expr_unary_op(p):
    '''expr : PLUS expr
            | MINUS expr
            | NOT expr
            | BOOLEAN_NOT expr'''
    pass


def p_expr_ternary_op(p):
    'expr : expr QUESTION expr COLON expr'
    pass


def p_expr_short_ternary_op(p):
    'expr : expr QUESTION COLON expr'
    pass


def p_expr_pre_incdec(p):
    '''expr : INC variable
            | DEC variable'''
    pass


def p_expr_post_incdec(p):
    '''expr : variable INC
            | variable DEC'''
    pass

def p_expr_cast_int(p):
    'expr : INT_CAST expr'
    pass

def p_expr_cast_array(p):
    'expr : ARRAY_CAST expr'
    pass


def p_expr_cast_string(p):
    'expr : STRING_CAST expr'


def p_expr_cast_double(p):
    'expr : DOUBLE_CAST expr'


def p_expr_cast_bool(p):
    'expr : BOOL_CAST expr'
    pass


def p_expr_cast_unset(p):
    'expr : UNSET_CAST expr'
    pass


def p_expr_cast_binary(p):
    'expr : BINARY_CAST expr'
    pass


def p_expr_isset(p):
    'expr : ISSET LPAREN isset_variables RPAREN'
    pass


def p_isset_variables(p):
    '''isset_variables : isset_variables COMMA variable
                       | variable'''
    pass


def p_expr_empty(p):
    'expr : EMPTY LPAREN expr RPAREN'
    pass


def p_expr_eval(p):
    'expr : EVAL LPAREN expr RPAREN'
    pass


def p_expr_include(p):
    'expr : INCLUDE expr'
    pass


def p_expr_include_once(p):
    'expr : INCLUDE_ONCE expr'
    pass


def p_expr_require(p):
    'expr : REQUIRE expr'
    pass


def p_expr_require_once(p):
    'expr : REQUIRE_ONCE expr'
    pass


def p_exit_or_die(p):
    '''exit_or_die : EXIT
                   | DIE'''
    pass


def p_expr_exit(p):
    '''expr : exit_or_die
            | exit_or_die LPAREN RPAREN
            | exit_or_die LPAREN expr RPAREN'''
    pass


def p_expr_print(p):
    'expr : PRINT expr'
    pass


def p_expr_silence(p):
    'expr : AT expr'
    pass


def p_expr_group(p):
    'expr : LPAREN expr RPAREN'
    pass


def p_nowdoc(p):
    'nowdoc : START_NOWDOC nowdoc_text_content END_NOWDOC'
    # print("reached nowdoc")
    pass


def p_scalar(p):
    '''scalar :  common_scalar
              | DOUBLE_QUOTE encaps_list DOUBLE_QUOTE
              | IDENTIFIER DOUBLE_QUOTE encaps_list DOUBLE_QUOTE
              | scalar_heredoc
              | nowdoc'''
    pass


def p_scalar_heredoc(p):
    'scalar_heredoc : START_HEREDOC encaps_list END_HEREDOC'
    pass


def p_nowdoc_text_content(p):
    '''nowdoc_text_content : nowdoc_text_content ENCAPSED_AND_WHITESPACE
                           | empty'''
    
    pass


def p_scalar_namespace_name(p):
    '''scalar : IDENTIFIER'''   
    pass


def p_common_scalar_number(p):
    ''' common_scalar : INT_NUMBER 
                      | FLOAT_NUMBER'''
    pass


def p_common_scalar_string(p):
    '''common_scalar : CONSTANT_ENCAPSED_STRING
                     | IDENTIFIER CONSTANT_ENCAPSED_STRING'''
    pass

def p_common_scalar_magic_func(p):
    'common_scalar : FUNC_C'
    pass


def p_common_scalar_magic_method(p):
    'common_scalar : METHOD_C'
    pass


def p_common_scalar_magic_line(p):
    'common_scalar : LINE'
    pass


def p_common_scalar_magic_file(p):
    'common_scalar : FILE'
    pass


def p_common_scalar_magic_dir(p):
    'common_scalar : DIR'
    pass


def p_static_scalar(p):
    '''static_scalar : common_scalar
                     | DOUBLE_QUOTE DOUBLE_QUOTE
                     | DOUBLE_QUOTE ENCAPSED_AND_WHITESPACE DOUBLE_QUOTE
                     | static_heredoc
                     | nowdoc'''
    print("recahed2")
    pass


def p_static_heredoc(p):
    '''static_heredoc : START_HEREDOC multiple_encapsed END_HEREDOC
                        '''
    pass


def p_multiple_encapsed(p):
    '''multiple_encapsed : multiple_encapsed ENCAPSED_AND_WHITESPACE
                         | empty'''
    # print("reached3")
    pass


def p_static_scalar_identifier(p):
    '''static_scalar : IDENTIFIER'''  
    pass


def p_static_scalar_unary_op(p):
    '''static_scalar : PLUS static_scalar
                     | MINUS static_scalar'''
    pass


def p_static_scalar_array(p):
    '''static_scalar : ARRAY LPAREN static_array_pair_list RPAREN
                     | LBRACKET static_array_pair_list RBRACKET'''
    pass


def p_static_array_pair_list(p):
    '''static_array_pair_list : empty
                              | static_non_empty_array_pair_list possible_comma'''
    pass


def p_static_non_empty_array_pair_list_item(p):
    '''static_non_empty_array_pair_list : static_non_empty_array_pair_list COMMA static_expr
                                        | static_expr'''
    pass


def p_static_non_empty_array_pair_list_pair(p):
    '''static_non_empty_array_pair_list : static_non_empty_array_pair_list COMMA static_scalar DOUBLE_ARROW static_expr
                                        | static_scalar DOUBLE_ARROW static_expr'''
    pass


def p_static_expr(p):
    '''static_expr : static_scalar
                   | static_expr BOOLEAN_AND static_expr
                   | static_expr BOOLEAN_OR static_expr
                   | static_expr LOGICAL_AND static_expr
                   | static_expr LOGICAL_OR static_expr
                   | static_expr LOGICAL_XOR static_expr
                   | static_expr AND static_expr
                   | static_expr OR static_expr
                   | static_expr XOR static_expr
                   | static_expr CONCAT static_expr
                   | static_expr PLUS static_expr
                   | static_expr MINUS static_expr
                   | static_expr MUL static_expr
                   | static_expr DIV static_expr
                   | static_expr SL static_expr
                   | static_expr SR static_expr
                   | static_expr MOD static_expr
                   | static_expr IS_IDENTICAL static_expr
                   | static_expr IS_NOT_IDENTICAL static_expr
                   | static_expr IS_EQUAL_TO static_expr
                   | static_expr IS_NOT_EQUAL static_expr
                   | static_expr LESS_THAN static_expr
                   | static_expr LESS_THAN_OR_EQUAL static_expr
                   | static_expr GREATER_THAN static_expr
                   | static_expr GRATER_THAN_OR_EQUAL static_expr'''
    pass


def p_static_expr_group(p):
    'static_expr : LPAREN static_expr RPAREN'
    pass


def p_encaps_list(p):
    '''encaps_list : encaps_list encaps_var
                   | empty'''
    pass


def p_encaps_var(p):
    'encaps_var : VARIABLE'
    pass


def p_encaps_var_array_offset(p):
    'encaps_var : VARIABLE LBRACKET encaps_var_offset RBRACKET'
    pass


def p_encaps_var_dollar_curly_expr(p):
    'encaps_var : DOLLAR_OPEN_CURLY_BRACES expr RBRACE'
    pass

def p_encaps_list_string(p):
    'encaps_list : encaps_list ENCAPSED_AND_WHITESPACE'
    # print("reached4")

def p_encaps_var_dollar_curly_array_offset(p):
    'encaps_var : DOLLAR_OPEN_CURLY_BRACES STRING_VARNAME LBRACKET expr RBRACKET RBRACE'
    pass


def p_encaps_var_curly_variable(p):
    'encaps_var : CURLY_OPEN variable RBRACE'
    pass


def p_encaps_var_offset_identifier(p):
    'encaps_var_offset : IDENTIFIER'
    pass


def p_encaps_var_offset_num_string(p):
    'encaps_var_offset : NUM_STRING'
    pass


def p_encaps_var_offset_variable(p):
    'encaps_var_offset : VARIABLE'
    pass


def p_empty(p):
    'empty : '
    pass

# Error rule for syntax errors


def p_error(t):
    # print(parser.state)
    if t:
        raise SyntaxError('invalid syntax', (None, t.lineno, None, t.value[1]['col']))
    else:
        raise SyntaxError('unexpected EOF while parsing',
                          (None, None, None, None))

# Build the grammar


def make_parser(debug=True):
    return yacc.yacc(debug=debug)


def main():
    import argparse
    import os
    ap = argparse.ArgumentParser(description="Parser test tool")
    ap.add_argument('-g', '--generate', dest='generate', action='store_true')
    ap.add_argument('-r', '--recursive', dest='recursive', action='store_true')
    ap.add_argument('-q', '--quiet', dest='quiet', action='store_true')
    ap.add_argument('-d', '--debug', dest='debug', action='store_true')
    ap.add_argument('path', metavar='PATH', nargs='?', type=str)
    args = ap.parse_args()

    if args.generate:
        make_parser(args.debug)
        return

    parser = make_parser(True)
    if args.path is None:
        run_parser(parser, sys.stdin, args.quiet, args.debug)
    elif os.path.isfile(args.path):
        with open(args.path, 'r') as f:
            run_parser(parser, f, args.quiet, args.debug)
    elif os.path.isdir(args.path):
        if not args.recursive:
            print('directory path given, use -r for recursive processing')
        else:
            for root, dirs, files in os.walk(args.path):
                for fpath in files:
                    if not fpath.endswith('.php'):
                        continue
                    with open(os.path.join(root, fpath), 'r') as f:
                        run_parser(parser, f, args.quiet, args.debug)


def run_parser(parser, source, quiet, debug):
    s = source.read()
    lexer = php_lex.lexer
    lexer.lineno = 1

    try:
        result = parser.parse(s, lexer=lexer.clone(), debug=debug)
    except SyntaxError as e:
        if e.lineno is not None:
            print(source.name, e, 'near', repr(e.text))
        else:
            print(source.name, e)
        sys.exit(1)
    except:
        print("Critical error in:", source.name)
        raise

    parser.restart()


main()

