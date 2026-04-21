# MiniLang - Fase 2: Analizador Sintáctico Ascendente con PLY

Compiladores, Primer Ciclo 2026 — Mgtr. Diana Gutiérrez

## Integrantes
- Velveth Anabella Ubedo Samayoa - 1107724
- Adonis Anthony David Hernández Pérez - 1086223

## ¿Qué hace el proyecto?

En esta fase se implementó el **analizador sintáctico ascendente** de MiniLang usando **PLY (Python Lex-Yacc)**. El proyecto quedó dividido en dos archivos principales:

- `lexer.py`: realiza el análisis léxico y genera los tokens
- `parser.py`: realiza el análisis sintáctico ascendente con `ply.yacc`

El programa recibe un archivo `.mlng`, primero ejecuta el lexer y luego el parser. Si todo está correcto imprime `OK`. Si encuentra errores, muestra la lista de errores léxicos y sintácticos con línea, columna, símbolo y descripción, sin detenerse en el primer problema.

## Cómo ejecutar

Se puede ejecutar de dos maneras.

### Opción 1: pasando el archivo por línea de comandos

```bash
python parser.py prueba1.mlng
```

### Opción 2: ejecutando el programa y escribiendo el nombre del archivo

```bash
python parser.py
```

Luego el programa pedirá:

```text
Archivo de entrada (.mlng):
```

Ahí se escribe por ejemplo:

```text
prueba1.mlng
```

## Estructura del proyecto

- `lexer.py`
- `parser.py`
- `README.md`
- `prueba1.mlng`
- `prueba2.mlng`
- `prueba3.mlng`
- `prueba4.mlng`
- `prueba5.mlng`
- `error1.mlng`
- `error2.mlng`
- `error3.mlng`

## Alcance del lenguaje soportado

La gramática implementada cubre lo solicitado para MiniLang en la Fase 2:

- Declaraciones de variables con tipos `int`, `float`, `string` y `bool`
- Asignaciones
- Expresiones aritméticas y booleanas
- Comparaciones con `==`, `!=`, `<`, `>`, `<=`, `>=`
- `if/else` anidados
- Ciclos `while`
- Definición de funciones con `def`
- Parámetros tipados en funciones
- `return`
- Llamadas a funciones
- `read(...)` y `write(...)`
- Bloques por indentación significativa con `INDENT` y `DEDENT`

## Decisiones de diseño

### 1. Uso de PLY para análisis ascendente

Se eligió **PLY** porque permite construir un parser **LALR(1)** de una forma cercana al enfoque clásico de `lex/yacc`. Para esta fase fue una buena decisión porque:

- permite escribir la gramática con producciones claras;
- separa bien el análisis léxico del sintáctico;
- facilita manejar precedencia y asociatividad;
- deja una base más formal y mantenible que un parser manual.

En la Fase 1 el reconocimiento sintáctico se hacía de forma manual. En esta fase el parser ascendente ya se construye con `ply.yacc`, que consume directamente los tokens producidos por `lexer.py`.

### 2. Separación entre lexer y parser

El archivo `parser.py` importa la lista `tokens` desde `lexer.py`, como lo requiere PLY. Así cada parte del proyecto tiene una responsabilidad definida:

- el lexer reconoce lexemas y genera tokens;
- el parser consume esos tokens y valida la gramática.

### 3. Indentación significativa

MiniLang usa bloques por espacios, estilo Python. Por eso el lexer mantiene una **pila de indentación** para emitir tokens `INDENT` y `DEDENT`.

Cuando el nivel de espacios aumenta, se genera `INDENT`.
Cuando disminuye, se generan uno o varios `DEDENT`.

De esta manera el parser puede reconocer correctamente bloques como los de `if`, `else`, `while` y `def`.

### 4. Precedencia y asociatividad

Para evitar ambigüedades se definió en el parser la precedencia solicitada en el enunciado, de menor a mayor:

1. `or`
2. `and`
3. comparaciones
4. `+` y `-`
5. `*`, `/`, `%`
6. `not` con asociatividad derecha

También se agregó el menos unario para expresiones negativas.

### 5. Recuperación de errores

La función `p_error(p)` no aborta el análisis en el primer error. En lugar de eso:

- registra el error con línea, columna, símbolo y descripción;
- descarta tokens hasta encontrar un punto razonable de sincronización;
- continúa el análisis para detectar más errores en la misma ejecución.

La sincronización se hace principalmente con:

- `NEWLINE`
- `DEDENT`
- fin de archivo

Esto permite reportar varios errores en una sola corrida, como pide la fase.

## Formato de errores

Los errores se muestran así:

```text
Línea X, Columna Y, Símbolo Z, Error: descripción
```

Se reportan tanto errores léxicos como errores sintácticos.

## Resumen de la gramática

La gramática reconoce, entre otras, las siguientes construcciones:

```bnf
programa            -> sentencias_opcionales
sentencia           -> sentencia_simple NEWLINE | sentencia_compuesta
sentencia_simple    -> declaracion | asignacion | retorno | lectura | escritura | llamada_funcion
sentencia_compuesta -> sentencia_if | sentencia_while | definicion_funcion
bloque              -> NEWLINE INDENT sentencias_opcionales DEDENT
```

Las expresiones incluyen operadores aritméticos, relacionales y lógicos con precedencia declarada en PLY.

## Casos de prueba exitosos

Se trabajó con cinco pruebas correctas, alineadas con el enunciado oficial:

### Prueba 1: Hola Mundo
Archivo: `prueba1.mlng`

Valida declaración de `string` y uso de `write` para imprimir texto.

### Prueba 2: Operación aritmética básica
Archivo: `prueba2.mlng`

Prueba declaraciones `int` y `float`, asignaciones y expresiones con `+`, `-`, `*`, `/` y `%`.

### Prueba 3: Entrada de datos y decisión con if
Archivo: `prueba3.mlng`

Valida `read`, comparaciones, `if/else` anidados e indentación significativa.

### Prueba 4: Función con parámetros y retorno
Archivo: `prueba4.mlng`

Comprueba `def`, parámetros tipados, `return`, llamadas a funciones y uso del resultado en asignaciones.

### Prueba 5: Variables, entrada/salida y while
Archivo: `prueba5.mlng`

Valida `while`, comparaciones, uso combinado de variables, `read` y `write`.

## Escenarios de error

También se incluyeron tres archivos de prueba con errores para verificar recuperación y reporte:

### Error 1: Declaración incompleta y símbolo inválido
Archivo: `error1.mlng`

Incluye una asignación incompleta y un carácter ilegal, útil para probar errores léxicos y sintácticos en la misma corrida.

### Error 2: if mal formado y llamada incompleta
Archivo: `error2.mlng`

Prueba ausencia de `:` en un `if` y una llamada sin cierre correcto.

### Error 3: Función mal definida y while sin condición
Archivo: `error3.mlng`

Valida errores en el encabezado de una función y en un `while` sin expresión de control.

## Resultado esperado

- Si el archivo no tiene errores léxicos ni sintácticos: `OK`
- Si hay errores: listado de errores encontrados hasta EOF

