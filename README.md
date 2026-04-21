# MiniLang - Fase 2: Analizador Sintáctico Ascendente

Compiladores, Primer Ciclo 2026 — Mgtr. Diana Gutiérrez

## Integrantes

- Velveth Anabella Ubedo Samayoa - 1107724  
- Adonis Anthony David Hernández Pérez - 1086223  

## Descripción del proyecto

En esta fase se implementó el analizador sintáctico ascendente del lenguaje MiniLang utilizando PLY (Python Lex-Yacc).

El sistema recibe un archivo .mlng, realiza análisis léxico y sintáctico, valida la estructura del programa y reporta errores sin detener la ejecución, permitiendo continuar hasta el final del archivo.

## Requisitos

Este proyecto utiliza Python y la librería PLY.

Para instalarla, ejecutar:

pip install ply

## Ejecución

Ejecutar desde la terminal:

python parser.py archivo.mlng

También se puede ejecutar sin argumentos:

python parser.py

Y luego ingresar el nombre del archivo cuando el programa lo solicite.

## Estructura del proyecto

- lexer.py → Analizador léxico  
- parser.py → Analizador sintáctico (PLY)  
- README.md → Documentación  
- prueba1.mlng … prueba5.mlng → Casos correctos  
- error1.mlng … → Casos con errores  

## Decisiones de diseño

- Se utilizó PLY para implementar un parser ascendente tipo LALR.
- Se mantuvo separación entre análisis léxico y sintáctico.
- Se implementó precedencia de operadores para evitar ambigüedades.
- Se utilizó indentación significativa (INDENT / DEDENT).
- Se implementó recuperación de errores para continuar el análisis.

## Manejo de errores

El sistema detecta:

- Errores léxicos (caracteres inválidos)
- Errores sintácticos (estructura incorrecta)
- Expresiones incompletas

Formato de salida:

Línea X, Columna Y, Símbolo Z, Error: descripción

El análisis no se detiene en el primer error.

## Casos de prueba

Correctos:

- prueba1.mlng → Hola Mundo  
- prueba2.mlng → Operaciones aritméticas  
- prueba3.mlng → Uso de read e if  
- prueba4.mlng → Funciones con parámetros  
- prueba5.mlng → Uso de while  

Con errores:

- error1.mlng → Declaraciones incompletas  
- error2.mlng → Errores de estructura  
- error3.mlng → Funciones incorrectas

## Salida del programa

Si el archivo es correcto:
OK

Si contiene errores:
Se muestra el listado de errores con su línea, columna y descripción.


