# MiniLang - Analizador Léxico (PLY)
# Fase 2 - Compiladores


import ply.lex as lex


# ---------------------------------------------------------
# Palabras reservadas
# ---------------------------------------------------------
reservadas = {
    'int': 'INT_TYPE',
    'float': 'FLOAT_TYPE',
    'string': 'STRING_TYPE',
    'bool': 'BOOL_TYPE',
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'def': 'DEF',
    'return': 'RETURN',
    'read': 'READ',
    'write': 'WRITE',
    'true': 'TRUE',
    'false': 'FALSE',
    'and': 'AND',
    'or': 'OR',
    'not': 'NOT',
}


# ---------------------------------------------------------
# Lista de tokens
# ---------------------------------------------------------
tokens = [
    'ID',
    'INT_LIT',
    'FLOAT_LIT',
    'STRING_LIT',

    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MOD',

    'ASSIGN',
    'EQ', 'NE', 'LT', 'LE', 'GT', 'GE',

    'LPAREN', 'RPAREN',
    'COMMA',
    'COLON',

    'NEWLINE',
    'INDENT',
    'DEDENT',
] + list(reservadas.values())


# ---------------------------------------------------------
# Expresiones regulares simples
# ---------------------------------------------------------
t_PLUS   = r'\+'
t_MINUS  = r'-'
t_TIMES  = r'\*'
t_DIVIDE = r'/'
t_MOD    = r'%'

t_EQ     = r'=='
t_NE     = r'!='
t_LE     = r'<='
t_GE     = r'>='
t_LT     = r'<'
t_GT     = r'>'

t_ASSIGN = r'='

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COMMA  = r','
t_COLON  = r':'


# Ignorar espacios y tabs (indentación se maneja aparte)
t_ignore = ' \t'


# ---------------------------------------------------------
# Manejo de saltos de línea
# ---------------------------------------------------------
def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    t.type = 'NEWLINE'
    return t


# ---------------------------------------------------------
# Comentarios (se ignoran)
# ---------------------------------------------------------
def t_COMMENT(t):
    r'\#.*'
    pass


# ---------------------------------------------------------
# Literales
# ---------------------------------------------------------
def t_FLOAT_LIT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t


def t_INT_LIT(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_STRING_LIT(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = t.value[1:-1]
    return t


# ---------------------------------------------------------
# Identificadores y palabras reservadas
# ---------------------------------------------------------
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reservadas.get(t.value, 'ID')
    return t


# ---------------------------------------------------------
# Manejo de indentación (estilo Python)
# ---------------------------------------------------------
def construir_lexer():
    lexer = lex.lex()

    lexer.indent_stack = [0]
    lexer.tokens_queue = []

    def input_con_indent(data):
        lexer.input(data)
        lexer.indent_stack = [0]
        lexer.tokens_queue = []

    def token_con_indent():
        if lexer.tokens_queue:
            return lexer.tokens_queue.pop(0)

        t = lexer.token()
        if not t:
            return None

        # Detectar inicio de línea para indentación
        if t.type == 'NEWLINE':
            lexer.tokens_queue.append(t)

            # Calcular espacios siguientes
            pos = lexer.lexpos
            espacios = 0

            while pos < len(lexer.lexdata) and lexer.lexdata[pos] == ' ':
                espacios += 1
                pos += 1

            nivel_actual = lexer.indent_stack[-1]

            if espacios > nivel_actual:
                lexer.indent_stack.append(espacios)
                tok = lex.LexToken()
                tok.type = 'INDENT'
                tok.value = None
                tok.lineno = t.lineno
                tok.lexpos = t.lexpos
                lexer.tokens_queue.append(tok)

            elif espacios < nivel_actual:
                while lexer.indent_stack and espacios < lexer.indent_stack[-1]:
                    lexer.indent_stack.pop()
                    tok = lex.LexToken()
                    tok.type = 'DEDENT'
                    tok.value = None
                    tok.lineno = t.lineno
                    tok.lexpos = t.lexpos
                    lexer.tokens_queue.append(tok)

            return lexer.tokens_queue.pop(0)

        return t

    lexer.input = input_con_indent
    lexer.token = token_con_indent
    lexer.errores = []

    # ---------------------------------------------------------
    # Error léxico
    # ---------------------------------------------------------
    def t_error(t):
        lexer.errores.append({
            'line': t.lineno,
            'column': t.lexpos,
            'symbol': repr(t.value[0]),
            'description': f"carácter inesperado {repr(t.value[0])}"
        })
        t.lexer.skip(1)

    lexer.t_error = t_error

    return lexer