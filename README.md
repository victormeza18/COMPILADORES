# Validador de Constantes Numéricas mediante Autómata Finito (FSA) en C++

Este repositorio contiene una implementación robusta, limpia y orientada a objetos en **C++** de un **Autómata Finito / Diagrama de Transiciones (FSA)** diseñado específicamente para la fase de Análisis Léxico dentro de un Compilador. Su objetivo principal es validar con precisión absoluta constantes numéricas sin signo (enteros, decimales de punto fijo y números en notación científica/exponencial).

El diseño y la matriz de transiciones de estados de este software modelan fielmente las especificaciones teóricas descritas en la diapositiva 13 de la presentación de *"Regular Expressions"* del curso de Compiladores.

---

## 📌 Contexto Teórico y Objetivos

En el diseño de compiladores, el **Analizador Léxico (Scanner)** se encarga de leer el flujo de caracteres del programa fuente y agruparlos en unidades significativas llamadas **lexemas**. Cada lexema se clasifica en una categoría gramatical denominada **token** mediante un patrón definido por **Expresiones Regulares**.

Para el token `number`, la definición regular extendida es la siguiente:
* `digit` -> `[0-9]`
* `digits` -> `digit+`
* `number` -> `digits ( . digits )? ( E [+-]? digits )?`

Para implementar este reconocimiento de manera eficiente y determinista, el patrón se traduce en un **Diagrama de Transiciones**. Este proyecto encapsula dicho diagrama dentro de una máquina de estados secuencial en C++.

---

## 🗺️ Arquitectura del Autómata (Diagrama de Estados)

El código emula el comportamiento del flujo de control basado en transiciones explícitas indexadas desde el estado inicial estipulado en el material de clase:

1.  **Estado 12 (Inicio):** El punto de entrada del análisis léxico. Evalúa el primer carácter del flujo. Si recibe un dígito numérico `[0-9]`, se desplaza al **Estado 13**. Cualquier otro carácter (letras, puntos descolocados, signos) provoca el rechazo inmediato de la cadena.
2.  **Estado 13 (Parte Entera / Aceptación):** Consume secuencialmente todos los dígitos pertenecientes a la sección entera del número. 
    * Si encuentra un punto `.`, transiciona al **Estado 14**.
    * Si encuentra el indicador de exponente `E` o `e`, transiciona al **Estado 16**.
    * Si la cadena de entrada finaliza en este punto, el lexema se valida con éxito como un **Número Entero**.
3.  **Estado 14 (Punto Decimal Intermedio):** Estado de transición estricto alcanzado tras detectar un punto decimal. Para evitar aceptar cadenas truncadas o inválidas como `42.`, exige obligatoriamente un dígito `[0-9]` a continuación para avanzar al **Estado 15**.
4.  **Estado 15 (Parte Decimal Fraccionaria / Aceptación):** Sigue consumiendo los dígitos fraccionarios del número decimal.
    * Si encuentra la constante de exponente `E` o `e`, transiciona al **Estado 16**.
    * Si la entrada concluye aquí, la cadena se acepta como un **Número Decimal de Punto Fijo**.
5.  **Estado 16 (Prefijo de Exponente):** Estado alcanzado tras la lectura de una `E`. Soporta dos flujos lógicos válidos:
    * Un modificador de signo explícito (`+` o `-`), el cual traslada el autómata al **Estado 17**.
    * Un dígito numérico directo, el cual traslada el autómata al **Estado 18**.
6.  **Estado 17 (Signo del Exponente Intermedio):** Se alcanza tras procesar el operador del exponente (ej. `6.02E+`). Requiere obligatoriamente un dígito numérico inmediato para validar la potencia. Si se provee, avanza al **Estado 18**.
7.  **Estado 18 (Valor del Exponente / Aceptación):** Consume los dígitos numéricos finales que representan la magnitud exponencial. Si el flujo se agota en este estado, la cadena se valida con éxito como un **Número en Notación Científica/Exponencial**.

Cualquier transición fuera de estas reglas definidas o cualquier carácter no anticipado en un estado intermedio derivará en un fallo léxico instantáneo (retornando `false`).

---

## 🚀 Características del Proyecto

* **Enfoque Orientado a Objetos Puro:** Toda la infraestructura interna, las transiciones y el estado del autómata están estrictamente encapsulados en la clase `NumberValidatorFSA`, garantizando código reutilizable, aislado y fácil de integrar en un proyecto de compilador más grande.
* **Eficiencia Óptima:** El procesamiento de la cadena se realiza en una sola pasada carácter por carácter, asegurando una complejidad temporal lineal O(N) con respecto a la longitud de la entrada y una complejidad espacial constante O(1).
* **Validación de Sintaxis Rigurosa:** Discrimina de forma exacta errores comunes de escaneo que los analizadores simplistas omiten (como la validación de operadores huérfanos o exponentes incompletos).
* **Casos de Prueba Exhaustivos:** La función constructora del punto de entrada (`main`) implementa pruebas automatizadas para asegurar la cobertura total de los flujos del autómata.

---

## 💻 Compilación e Instalación

Este proyecto utiliza el estándar ANSI C++ estándar, haciéndolo multiplataforma y compatible con cualquier entorno moderno.

### Prerrequisitos
Tener instalado un compilador de C++ como `g++` (GCC), `clang++` o el compilador de Microsoft Visual Studio.

### Compilación desde la Terminal (usando GCC)
Navega hasta el directorio que contiene tu archivo fuente y ejecuta:

```bash
g++ -std=c++11 main.cpp -o validador_fsa
