import ply.lex as lex
import re
from symbol_table import SymbolTable

input_string = " "


def col_no(pos, val):
    last_new_line_pos = input_string.rfind("\n", 0, pos)
    final_pos = pos-len(val)-last_new_line_pos
    return final_pos


states = (
    ('php', 'exclusive'),
    ('singleQuoted', 'exclusive'),
    ('doubleQuoted', 'exclusive'),
    ('quotedvar', 'exclusive'),
    ('varname', 'exclusive'),
    ('offset', 'exclusive'),
    ('heredoc', 'exclusive'),
    ('nowdoc', 'exclusive'),

)

reserved = (
    'ARRAY',  'BREAK', 'CASE',  'CONST', 'CONTINUE',
    'DEFAULT', 'DIE', 'DO', 'ECHO', 'ELSE', 'ELSEIF', 'EMPTY',
    'ENDFOR',  'ENDIF', 'ENDSWITCH', 'ENDWHILE', 'EVAL', 'EXIT',
    'FOR',  'FUNCTION', 'GLOBAL', 'IF', 'INCLUDE',
    'INCLUDE_ONCE', 'INSTANCEOF', 'ISSET', 'LIST',  'PRINT', 'REQUIRE',
    'REQUIRE_ONCE', 'RETURN', 'STATIC', 'SWITCH', 'UNSET',
    'WHILE',  'CLONE',  'YIELD'
)
unparsed = (
    'WHITESPACE',
    'COMMENT',
    'OPEN_TAG', 'OPEN_TAG_WITH_ECHO', 'CLOSE_TAG'
)

tokens = reserved+unparsed+(


    'PLUS', 'MINUS', 'MUL', 'DIV', 'MOD', 'AND', 'OR', 'NOT', 'XOR', 'SL',
    'SR', 'BOOLEAN_AND', 'BOOLEAN_OR', 'BOOLEAN_NOT', 'LESS_THAN', 'GREATER_THAN', 'LESS_THAN_OR_EQUAL', 'GRATER_THAN_OR_EQUAL', 'IS_EQUAL_TO', 'IS_NOT_EQUAL', 'IS_IDENTICAL',
    'IS_NOT_IDENTICAL',

    'EQUALS', 'MUL_EQUAL', 'DIV_EQUAL', 'MOD_EQUAL', 'PLUS_EQUAL', 'MINUS_EQUAL',
    'SL_EQUAL', 'SR_EQUAL', 'AND_EQUAL', 'OR_EQUAL', 'XOR_EQUAL', 'CONCAT_EQUAL',

    'INC', 'DEC',
    "DOUBLE_ARROW",

    'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET', 'LBRACE', 'RBRACE', 'DOLLAR',
    'COMMA', 'CONCAT', 'QUESTION', 'COLON', 'SEMI_COLON', 'AT',

    'INLINE_HTML',

    'DIR', 'FILE', 'LINE', 'METHOD_C',  'LOGICAL_AND', 'LOGICAL_OR', 'LOGICAL_XOR',
    'VARIABLE', 'INT_NUMBER', 'FLOAT_NUMBER',  'DOUBLE_QUOTE', 'IDENTIFIER',
    'NUM_STRING', 'FUNC_C', 'HALT_COMPILER', 'CONSTANT_ENCAPSED_STRING',

    'ARRAY_CAST', 'BINARY_CAST', 'BOOL_CAST', 'DOUBLE_CAST', 'INT_CAST',
    'STRING_CAST', 'UNSET_CAST', 'ENCAPSED_AND_WHITESPACE', 'STRING_VARNAME', 'START_HEREDOC', 'END_HEREDOC',
    'CURLY_OPEN', 'DOLLAR_OPEN_CURLY_BRACES', 'START_NOWDOC', 'END_NOWDOC', 'SPACESHIP'

    #'STRING','SINGLE_QUOTE','OBJECT_CAST', 'CLASS_C','NS_SEPARATOR','NS_C',
    # ,'UNQUOTED_STRING','NULL_COALESCING',(implment if time is available)

)

reserved_map = {}
for r in reserved:
    reserved_map[r] = r


def t_ANY_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_OPEN_TAG(t):
    r'<[?%](([Pp][Hh][Pp][ \t\r\n]?)|=)?'
    if '=' in t.value:
        t.type = 'OPEN_TAG_WITH_ECHO'
    t.lexer.lineno += t.value.count("\n")
    t.lexer.push_state('php')
    return t


def t_php_CLOSE_TAG(t):
    r'[?%]>\r?\n?'
    t.lexer.lineno += t.value.count("\n")
    t.lexer.pop_state()
    return t


def t_php_reserved_words(t):
    r'[a-zA-Z_][\w\d_]*'
    t.type = reserved_map.get((t.value).upper(), "IDENTIFIER")
    if(t.type == "IDENTIFIER"):
        if(t.lexer.symbol_table.insert(t.value) != None):
            t.lexer.symbol_table.set_attribute(t.value, 'type', t.type)
            t.lexer.symbol_table.set_attribute(
                t.value, 'line_no', t.lexer.lineno)
            t.lexer.symbol_table.set_attribute(
                t.value, 'col', col_no(t.lexer.lexpos, t.value))
        t.value = (t.value, t.lexer.symbol_table.lookup(t.value))
    else:
        t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})
    return t


def t_php_VARIABLE(t):
    r'\$[A-Za-z_][\w_]*'

    if(t.lexer.symbol_table.insert(t.value) != None):
        t.lexer.symbol_table.set_attribute(t.value, 'type', t.type)
        t.lexer.symbol_table.set_attribute(t.value, 'line_no', t.lexer.lineno)
        t.lexer.symbol_table.set_attribute(
            t.value, 'col', col_no(t.lexer.lexpos, t.value))
    t.value = (t.value, t.lexer.symbol_table.lookup(t.value))

    return t


t_php_ignore_WHITESAPCE = r'\s'

def t_php_COMMENT(t):
    r'/\*(.|\n)*?\*/ | //([^?%\n]|[?%](?!>))*\n? | \#([^?%\n]|[?%](?!>))*\n?'
    t.lexer.lineno += t.value.count("\n")
    t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})
    return t
    

def t_php_RBRACE(t):
    r'\}'
    t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})
    t.lexer.pop_state()
    return t


def t_php_LBRACKET(t):
    r'\['
    t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})
    t.lexer.push_state('php')
    return t


def t_php_RBRACKET(t):
    r'\]'
    t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})
    t.lexer.pop_state()
    return t

# String literal


def t_php_CONSTANT_ENCAPSED_STRING(t):
    r"'([^\\']|\\(.|\n))*'"
    t.lexer.lineno += t.value.count("\n")
    if(t.lexer.symbol_table.insert(t.value) != None):
        t.lexer.symbol_table.set_attribute(t.value, 'type', t.type)
        t.lexer.symbol_table.set_attribute(t.value, 'line_no', t.lexer.lineno)
        t.lexer.symbol_table.set_attribute(
            t.value, 'col', col_no(t.lexer.lexpos, t.value))
    t.value = (t.value, t.lexer.symbol_table.lookup(t.value))
    return t


def t_php_DOUBLE_QUOTE(t):
    r'"'
    t.lexer.push_state('doubleQuoted')
    t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})

    return t


def t_doubleQuoted_VARIABLE(t):
    r'\$[A-Za-z_][\w_]*'

    if(t.lexer.symbol_table.insert(t.value) != None):
        t.lexer.symbol_table.set_attribute(t.value, 'type', t.type)
        t.lexer.symbol_table.set_attribute(t.value, 'line_no', t.lexer.lineno)
        t.lexer.symbol_table.set_attribute(
            t.value, 'col', col_no(t.lexer.lexpos, t.value))
    t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})
    t.lexer.push_state('quotedvar')
    return t


def t_doubleQuoted_DOUBLE_QUOTE(t):
    r'(?<!\\)"'
    t.lexer.pop_state()
    t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})
    return t


def t_doubleQuoted_ENCAPSED_AND_WHITESPACE(t):
    r'( [^"\\${] | \\(.|\n) | \$(?![A-Za-z_{]) | \{(?!\$) )+'
    t.lexer.lineno += t.value.count("\n")
    t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})
    return t


def t_doubleQuoted_CURLY_OPEN(t):
    r'\{(?=\$)'
    t.lexer.push_state('php')
    t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})
    return t


def t_doubleQuoted_DOLLAR_OPEN_CURLY_BRACES(t):
    r'\$\{'
    if re.match(r'[A-Za-z_]', peek(t.lexer)):
        t.lexer.push_state('varname')
    else:
        t.lexer.push_state('php')
    t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})
    return t


def t_varname_STRING_VARNAME(t):
    r'[A-Za-z_][\w_]*'
    t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})
    return t


t_varname_RBRACE = t_php_RBRACE
t_varname_LBRACKET = t_php_LBRACKET


def t_quotedvar_QUOTE(t):
    r'"'
    t.lexer.pop_state()
    t.lexer.pop_state()
    t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})
    return t


def t_quotedvar_LBRACKET(t):
    r'\['
    t.lexer.begin('offset')
    t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})
    return t


def t_quotedvar_ENCAPSED_AND_WHITESPACE(t):
    r'( [^"\\${] | \\(.|\n) | \$(?![A-Za-z_{]) | \{(?!\$) )+'
    t.lexer.lineno += t.value.count("\n")
    t.lexer.pop_state()
    t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})
    return t


t_quotedvar_VARIABLE = t_php_VARIABLE


def t_quotedvar_CURLY_OPEN(t):
    r'\{(?=\$)'
    t.lexer.begin('php')
    t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})
    return t


def t_quotedvar_DOLLAR_OPEN_CURLY_BRACES(t):
    r'\$\{'
    if re.match(r'[A-Za-z_]', peek(t.lexer)):
        t.lexer.begin('varname')
    else:
        t.lexer.begin('php')
    t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})
    return t


def t_offset_IDENTIFIER(t):
    r'[A-Za-z_][\w_]*'
    t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})
    return t


def t_offset_NUM_STRING(t):
    r'\d+'
    t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})
    return t


t_offset_VARIABLE = t_php_VARIABLE
t_offset_RBRACKET = t_php_RBRACKET


# HEREDOCS
def t_php_LBRACE(t):
    r'\{'
    
    t.lexer.push_state('php')
    t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})
    return t


def t_php_START_HEREDOC(t):
    r'<<<[ \t]*(?P<label>[A-Za-z_][\w_]*)\r?\n'
    t.lexer.lineno += t.value.count("\n")
    t.lexer.push_state('heredoc')
    t.lexer.heredoc_label = t.lexer.lexmatch.group('label')
    
    t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})
    return t


t_heredoc_CURLY_OPEN = t_doubleQuoted_CURLY_OPEN
t_heredoc_DOLLAR_OPEN_CURLY_BRACES = t_doubleQuoted_DOLLAR_OPEN_CURLY_BRACES
t_heredoc_LBRACKET = t_php_LBRACKET
t_heredoc_LBRACE = t_php_LBRACE


def t_heredoc_END_HEREDOC(t):
    r'([^$\"\'\n;\{\}]+|((?<=\\)\")+|((?<=\\)\')+|((?<=\\)$)+)|(^[\s]*\s)'
    if t.value == t.lexer.heredoc_label:
        del t.lexer.heredoc_label
        t.lexer.pop_state()
        t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})

    else:
        t.type = 'ENCAPSED_AND_WHITESPACE'
        if(t.lexer.symbol_table.insert(t.value) != None):
            t.lexer.symbol_table.set_attribute(t.value, 'type', t.type)
            t.lexer.symbol_table.set_attribute(
                t.value, 'line_no', t.lexer.lineno)
            t.lexer.symbol_table.set_attribute(
                t.value, 'col', col_no(t.lexer.lexpos, t.value))
        t.value = (t.value, t.lexer.symbol_table.lookup(t.value))

    return t


def t_heredoc_ENCAPSED_AND_WHITESPACE(t):
    r'( [^\n\\${] | \\. | \$(?![A-Za-z_{]) | \{(?!\$) )+\n? | \\?\n'
    t.lexer.lineno += t.value.count("\n")
    t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})
    return t


def t_heredoc_VARIABLE(t):
    r'\$[A-Za-z_][\w_]*'
    t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})
    return t


# NOWDOCS

def t_php_START_NOWDOC(t):
    r'''<<<[ \t]*'(?P<label>[A-Za-z_][\w_]*)'\r?\n'''
    t.lexer.lineno += t.value.count("\n")
    t.lexer.push_state('nowdoc')
    t.lexer.nowdoc_label = t.lexer.lexmatch.group('label')
    t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})
    return t


def t_nowdoc_END_NOWDOC(t):
    r'(?<=\n)[A-Za-z_][\w_]*'
    if t.value == t.lexer.nowdoc_label:
        del t.lexer.nowdoc_label
        t.lexer.pop_state()
    else:
        t.type = 'ENCAPSED_AND_WHITESPACE'
    t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})
    return t


def t_nowdoc_ENCAPSED_AND_WHITESPACE(t):
    r'[^\n]*\n'
    t.lexer.lineno += t.value.count("\n")
    t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})
    return t


def t_php_SPACESHIP(t):
    r'<=>'
    t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})
    return t


def t_php_INC(t):
    r'\+\+'
    t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})
    return t


def t_php_DEC(t):
    r'--'
    t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})
    return t


def t_php_DOUBLE_ARROW(t):
    r'=>'
    t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})
    return t


def t_php_BOOLEAN_AND(t):
    r'&&'
    t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})
    return t


def t_php_BOOLEAN_OR(t):
    r'\|\|'
    t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})
    return t


def t_php_BOOLEAN_NOT(t):
    r'!'
    t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})
    return t


def t_php_LESS_THAN_OR_EQUAL(t):
    r'<='
    t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})
    return t


def t_php_GREATER_THAN_OR_EQUAL(t):
    r'>='
    t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})
    return t


def t_php_LESS_THAN(t):
    r'<'
    t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})
    return t


def t_php_GREATER_THAN(t):
    r'>'
    t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})
    return t


def t_php_IS_EQUAL_TO(t):
    r'=='
    t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})
    return t


def t_php_IS_NOT_EQUAL(t):
    r'(!=(?!=))|(<>)'
    t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})
    return t


def t_php_IS_IDENTICAL(t):
    r'==='
    t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})
    return t


def t_php_IS_NOT_IDENTICAL(t):
    r'!=='
    t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})
    return t


def t_php_EQUALS(t):
    r'='
    t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})
    return t


def t_php_MUL_EQUAL(t):
    r'\*='
    t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})
    return t


def t_php_DIV_EQUAL(t):
    r'/='
    t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})
    return t


def t_php_MOD_EQUAL(t):
    r'%='
    t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})
    return t


def t_php_PLUS_EQUAL(t):
    r'\+='
    t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})
    return t


def t_php_MINUS_EQUAL(t):
    r'-='
    t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})
    return t


def t_php_SL_EQUAL(t):
    r'<<='
    t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})
    return t


def t_php_SR_EQUAL(t):
    r'>>='
    t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})
    return t


def t_php_AND_EQUAL(t):
    r'&='
    t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})
    return t


def t_php_OR_EQUAL(t):
    r'\|='
    t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})
    return t


def t_php_XOR_EQUAL(t):
    r'\^='
    t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})
    return t


def t_php_CONCAT_EQUAL(t):
    r'\.='
    t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})
    return t


def t_HERE_NOW_DOC(t):
    r'<<<'
    t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})
    return t


def t_php_PLUS(t):
    r'\+'
    t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})
    return t


def t_php_MINUS(t):
    r'-'
    t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})
    return t


def t_php_MUL(t):
    r'\*'
    t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})
    return t


def t_php_DIV(t):
    r'/'
    t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})
    return t


def t_php_MOD(t):
    r'%'
    t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})
    return t


def t_php_AND(t):
    r'&'
    t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})
    return t


def t_php_OR(t):
    r'\|'
    t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})
    return t


def t_php_NOT(t):
    r'~'
    t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})
    return t


def t_php_XOR(t):
    r'\^'
    t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})
    return t


def t_php_SL(t):
    r'<<'
    t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})
    return t


def t_php_SR(t):
    r'>>'
    t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})
    return t


def t_php_CONCAT(t):
    r'\.(?!\d|=)'
    t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})
    return t


def t_php_LPAREN(t):
    r'\('
    t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})
    return t


def t_php_RPAREN(t):
    r'\)'
    t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})
    return t


def t_php_DOLLAR(t):
    r'\$'
    t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})
    return t


def t_php_COMMA(t):
    r','
    t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})
    return t


def t_php_QUESTION(t):
    r'\?'
    t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})
    return t


def t_php_COLON(t):
    r':'
    t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})
    return t


def t_php_SEMI_COLON(t):
    r';'
    t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})
    return t


def t_php_AT(t):
    r'@'
    t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})
    return t


def t_php_NS_SEPARATOR(t):
    r'\\'
    t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})
    return t


def t_php_ARRAY_CAST(t):
    r'\([\t]*[Aa][Rr][Rr][Aa][Yy][\t]*\)'
    t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})
    return t


def t_php_BINARY_CAST(t):
    r'\([ \t]*[Bb][Ii][Nn][Aa][Rr][Yy][ \t]*\)'
    t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})
    return t


def t_php_BOOL_CAST(t):
    r'\([\t]*[Bb][Oo][Oo][Ll]([Ee][Aa][Nn])?[\t]*\)'
    t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})
    return t


def t_php_DOUBLE_CAST(t):
    r'\([\t]*([Rr][Ee][Aa][Ll]|[Dd][Oo][Uu][Bb][Ll][Ee]|[Ff][Ll][Oo][Aa][Tt])[\t]*\)'
    t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})
    return t


def t_php_INT_CAST(t):
    r'\([\t]*[Ii][Nn][Tt]([Ee][Gg][Ee][Rr])?[\t]*\)'
    t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})
    return t


def t_php_OBJECT_CAST(t):
    r'\([\t]*[Oo][Bb][Jj][Ee][Cc][Tt][\t]*\)'
    t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})
    return t


def t_php_STRING_CAST(t):
    r'\([\t]*[Ss][Tt][Rr][Ii][Nn][Gg][\t]*\)'
    t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})
    return t


def t_php_UNSET_CAST(t):
    r'\([\t]*[Uu][Nn][Ss][Ee][Tt][\t]*\)'
    t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})
    return t


def t_INLINE_HTML(t):
    r'<\w+[^>]*>(.|\s)+?<\/\w+>|<\w+[^>]*(.|\s)+?\/?>'
    t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})
    t.lexer.lineno += t.value.count('\n')
    return t


def t_php_FLOAT_NUMBER(t):
    r'\d*\.\d+([eE][*-]?\d+)?'

    if(t.lexer.symbol_table.insert(t.value) != None):
        t.lexer.symbol_table.set_attribute(t.value, 'type', t.type)
        t.lexer.symbol_table.set_attribute(t.value, 'line_no', t.lexer.lineno)
        t.lexer.symbol_table.set_attribute(
            t.value, 'col', col_no(t.lexer.lexpos, t.value))
    t.value = (t.value, t.lexer.symbol_table.lookup(t.value))

    return t


def t_php_INT_NUMBER(t):
    r'(\d+([eE][*-]?\d+)?)|(0b[01]+)|(0x[0-9A-Fa-f]+)'
    if(t.lexer.symbol_table.insert(t.value) != None):
        t.lexer.symbol_table.set_attribute(t.value, 'type', t.type)
        t.lexer.symbol_table.set_attribute(t.value, 'line_no', t.lexer.lineno)
        t.lexer.symbol_table.set_attribute(
            t.value, 'col', col_no(t.lexer.lexpos, t.value))
    t.value = (t.value, t.lexer.symbol_table.lookup(t.value))
    return t


def t_ANY_error(t):
    print('Illegal character at line no. %d and position no. %d, character:%s' % (
        t.lexer.lineno, col_no(t.lexer.lexpos, t.value), t.value))
    t.lexer.skip(1)


def peek(lexer):
    try:
        return lexer.lexdata[lexer.lexpos]
    except IndexError:
        return ''


class FilteredLexer(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.last_token = None

    @property
    def lineno(self):
        return self.lexer.lineno

    @lineno.setter
    def lineno(self, value):
        self.lexer.lineno = value

    @property
    def lexpos(self):
        return self.lexer.lexpos

    @lexpos.setter
    def lexpos(self, value):
        self.lexer.lexpos = value

    def clone(self):
        return FilteredLexer(self.lexer.clone())

    def current_state(self):
        return self.lexer.current_state()

    def input(self, input):
        self.lexer.input(input)
        input_string = input

    def next_lexer_token(self):
        """Return next lexer token.
        Can be useful to customize parser behavior without need to touch
        parser code in the token method."""
        return self.lexer.token()

    def token(self):
        t = self.next_lexer_token()

        # Filter out tokens that the parser is not expecting.
        while t and t.type in unparsed:

            # Skip over open tags, but keep track of when we see them.
            if t.type == 'OPEN_TAG':
                if self.last_token and self.last_token.type == 'SEMI_COLON':
                    # Rewrite ?><?php as a semicolon.
                    t.type = 'SEMI_COLON'
                    t.value = (t.value, {'type': t.type ,'line_no':t.lexer.lineno ,'col': col_no(t.lexer.lexpos, t.value)})
                    break
                self.last_token = t
                t = self.next_lexer_token()
                continue

            # Rewrite <?= to yield an "echo" statement.
            if t.type == 'OPEN_TAG_WITH_ECHO':
                t.type = 'ECHO'
                break

            # Insert semicolons in place of close tags where necessary.
            if t.type == 'CLOSE_TAG':
                if self.last_token and \
                    self.last_token.type in ('OPEN_TAG', 'SEMI_COLON', 'COLON',
                                             'LBRACE', 'RBRACE'):
                    # Dont insert semicolons after these tokens.
                    pass
                else:
                    # Rewrite close tag as a semicolon.
                    t.type = 'SEMI_COLON'
                    break

            t = self.next_lexer_token()

        self.last_token = t
        return t

    # Iterator interface
    def __iter__(self):
        return self

    def __next__(self):
        t = self.token()
        if t is None:
            raise StopIteration
        return t

    __next__ = next


full_lexer = lex.lex()
full_lexer.symbol_table = SymbolTable()
lexer = FilteredLexer(full_lexer)

full_tokens = tokens
tokens = [token for token in tokens if token not in unparsed]


def run_on_argv1():
    lex.runmain(full_lexer)


# lexer=lex.lex()
# lexer.symbol_table=SymbolTable()

# with open('./variables.php') as f:
#     lines=f.readlines()
#     string="".join(lines)

# lexer.input(string)
# while(True):
#     tok=lexer.token()
#     if(tok!=None):
#         print(tok.value)
#     else:
#         break
