# MiniLang - Analizador Sintáctico Ascendente (PLY)
# Fase 2 - Compiladores

import sys
import ply.yacc as yacc
from lexer import construir_lexer, tokens


# Clase para almacenar errores sintácticos
class RecolectorErrores:
    def __init__(self):
        self.errores = []

    def agregar(self, linea, columna, simbolo, descripcion):
        self.errores.append({
            'line': linea,
            'column': columna,
            'symbol': simbolo,
            'description': descripcion,
        })


# Obtiene columna del token
def obtener_columna(lexer_obj, token):
    return lexer_obj.find_column(token)


# Precedencia de operadores (de menor a mayor)
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('nonassoc', 'EQ', 'NE', 'LT', 'LE', 'GT', 'GE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MOD'),
    ('right', 'NOT'),
    ('right', 'UMINUS'),
)


# Regla inicial del programa
def p_programa(p):
    'programa : saltos_opcionales sentencias_opcionales'
    p[0] = ('programa', p[2])


# Lista de sentencias
def p_sentencias_opcionales_lista(p):
    'sentencias_opcionales : sentencias'
    p[0] = p[1]


def p_sentencias_opcionales_vacia(p):
    'sentencias_opcionales : vacio'
    p[0] = []


def p_sentencias_varias(p):
    'sentencias : sentencias sentencia'
    p[0] = p[1] + [p[2]]


def p_sentencias_una(p):
    'sentencias : sentencia'
    p[0] = [p[1]]


# Sentencias simples
def p_sentencia_simple(p):
    'sentencia : sentencia_simple saltos'
    p[0] = p[1]


def p_sentencia_simple_con_sobrante(p):
    'sentencia : sentencia_simple error saltos'
    p[0] = p[1]


# Sentencias compuestas
def p_sentencia_compuesta(p):
    'sentencia : sentencia_compuesta'
    p[0] = p[1]


# Recuperación básica
def p_sentencia_recuperada(p):
    'sentencia : error saltos'
    p[0] = ('error',)


# Tipos de datos
def p_tipo_dato(p):
    '''tipo_dato : INT_TYPE
                 | FLOAT_TYPE
                 | STRING_TYPE
                 | BOOL_TYPE'''
    p[0] = p[1]


# Declaraciones
def p_declaracion_simple(p):
    'declaracion : tipo_dato ID'
    p[0] = ('declaracion', p[1], p[2], None)


def p_declaracion_con_asignacion(p):
    'declaracion : tipo_dato ID ASSIGN expresion'
    p[0] = ('declaracion', p[1], p[2], p[4])


# Declaración incompleta → genera error real
def p_declaracion_sin_valor(p):
    'declaracion : tipo_dato ID ASSIGN'
    parser = p_error.parser_ref
    lexer_obj = p_error.lexer_ref
    recolector = p_error.recolector_ref

    columna = obtener_columna(lexer_obj, p.slice[3])
    recolector.agregar(
        p.lineno(3),
        columna,
        "'='",
        "falta expresión después de '='"
    )

    p[0] = ('declaracion_incompleta', p[1], p[2])


# Declaración con error en expresión
def p_declaracion_error(p):
    'declaracion : tipo_dato ID ASSIGN error'
    pass


# Asignación
def p_asignacion(p):
    'asignacion : ID ASSIGN expresion'
    p[0] = ('asignacion', p[1], p[3])


# Asignación incompleta
def p_asignacion_sin_valor(p):
    'asignacion : ID ASSIGN'
    parser = p_error.parser_ref
    lexer_obj = p_error.lexer_ref
    recolector = p_error.recolector_ref

    columna = obtener_columna(lexer_obj, p.slice[2])
    recolector.agregar(
        p.lineno(2),
        columna,
        "'='",
        "falta expresión después de '='"
    )

    p[0] = ('asignacion_incompleta', p[1])


def p_asignacion_error(p):
    'asignacion : ID ASSIGN error'
    pass


# Return
def p_retorno(p):
    'retorno : RETURN expresion'
    p[0] = ('return', p[2])


# Entrada / salida
def p_lectura(p):
    'lectura : READ LPAREN ID RPAREN'
    p[0] = ('read', p[3])


def p_escritura(p):
    'escritura : WRITE LPAREN expresion RPAREN'
    p[0] = ('write', p[3])


# If / Else
def p_sentencia_if_sin_else(p):
    'sentencia_if : IF expresion COLON bloque'
    p[0] = ('if', p[2], p[4], None)


def p_sentencia_if_con_else(p):
    'sentencia_if : IF expresion COLON bloque ELSE COLON bloque'
    p[0] = ('if', p[2], p[4], p[7])


# While
def p_sentencia_while(p):
    'sentencia_while : WHILE expresion COLON bloque'
    p[0] = ('while', p[2], p[4])


# Funciones
def p_definicion_funcion(p):
    'definicion_funcion : DEF ID LPAREN parametros_opcionales RPAREN COLON bloque'
    p[0] = ('def', p[2], p[4], p[7])


# Bloque indentado
def p_bloque(p):
    'bloque : NEWLINE INDENT saltos_opcionales sentencias_opcionales DEDENT'
    p[0] = p[4]


# Expresiones
def p_expresion_binaria(p):
    '''expresion : expresion OR expresion
                 | expresion AND expresion
                 | expresion EQ expresion
                 | expresion NE expresion
                 | expresion LT expresion
                 | expresion LE expresion
                 | expresion GT expresion
                 | expresion GE expresion
                 | expresion PLUS expresion
                 | expresion MINUS expresion
                 | expresion TIMES expresion
                 | expresion DIVIDE expresion
                 | expresion MOD expresion'''
    p[0] = ('binaria', p[2], p[1], p[3])


# Manejo de errores sintácticos con recuperación
def p_error(p):
    parser = p_error.parser_ref
    lexer_obj = p_error.lexer_ref
    recolector = p_error.recolector_ref

    if p is None:
        recolector.agregar(0, 0, 'EOF', 'fin de archivo inesperado')
        return

    columna = obtener_columna(lexer_obj, p)
    simbolo = p.value if p.value is not None else p.type
    recolector.agregar(p.lineno, columna, repr(simbolo), f'sintaxis no válida cerca de {p.type}')

    while True:
        tok = parser.token()
        if not tok:
            return
        if tok.type in ('NEWLINE', 'DEDENT'):
            parser.errok()
            return tok


# Construcción del parser
def construir_parser(lexer_obj, recolector=None):
    if recolector is None:
        recolector = RecolectorErrores()
    parser = yacc.yacc(start='programa', write_tables=False, debug=False)
    p_error.parser_ref = parser
    p_error.lexer_ref = lexer_obj
    p_error.recolector_ref = recolector
    return parser, recolector


# Función principal de análisis
def analizar_codigo(codigo_fuente):
    lexer = construir_lexer()
    lexer.input(codigo_fuente)
    parser, recolector = construir_parser(lexer)
    parser.parse(lexer=lexer)
    return lexer.errores, recolector.errores


# Formato de salida de errores
def formatear_error(error):
    return f"Línea {error['line']}, Columna {error['column']}, Símbolo {error['symbol']}, Error: {error['description']}"


# Punto de entrada
def main():
    if len(sys.argv) >= 2:
        ruta = sys.argv[1]
    else:
        ruta = input('Archivo de entrada (.mlng): ').strip()

    try:
        with open(ruta, 'r', encoding='utf-8') as f:
            codigo = f.read()
    except:
        print('No se pudo abrir el archivo')
        return

    lex, sint = analizar_codigo(codigo)
    errores = lex + sint

    if errores:
        for e in errores:
            print(formatear_error(e))
    else:
        print('OK')


if __name__ == '__main__':
    main()