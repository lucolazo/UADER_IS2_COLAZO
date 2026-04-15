#!/usr/bin/env python3
"""
Calculadora RPN con pila, funciones matemáticas, trigonometría en grados,
comandos de pila y memorias 00-09.
"""

import math
import sys

# Una excepción personalizada para capturar errores específicos (como división por cero
# o falta de operandos) y mostrarlos amigablemente al usuario.
class RPNError(Exception):
    """Excepción personalizada para errores de la calculadora RPN."""


# Define constantes como π, e y el número áureo (φ).
CONST = {"p": math.pi, "e": math.e, "j": (1 + math.sqrt(5)) / 2}  # φ

# Mapea nombres de funciones (como sin, sqrt, log) a su aridad (cuántos números necesita)
# y su implementación matemática usando el módulo math o funciones lambda para operaciones específicas.
FUNC = {
    "sqrt": (1, math.sqrt),
    "log": (1, math.log10),
    "ln": (1, math.log),
    "ex": (1, math.exp),
    "10x": (1, lambda x: 10**x),
    "1/x": (1, lambda x: 1 / x),
    "chs": (1, lambda x: -x),
    "sin": (1, lambda x: math.sin(math.radians(x))),
    "cos": (1, lambda x: math.cos(math.radians(x))),
    "tg": (1, lambda x: math.tan(math.radians(x))),
    "asin": (1, lambda x: math.degrees(math.asin(x))),
    "acos": (1, lambda x: math.degrees(math.acos(x))),
    "atg": (1, lambda x: math.degrees(math.atan(x))),
    "yx": (2, lambda y, x: y**x),
}

# Un diccionario que simula 10 registros de memoria (00 al 09).
MEM = {f"{i:02d}": 0.0 for i in range(10)}


def evaluate(expr):
    """
    Evalúa una expresión en notación RPN y retorna el resultado numérico.

    Args:
        expr (str): Expresión RPN con tokens separados por espacios.

    Returns:
        float: Resultado de la evaluación.

    Raises:
        RPNError: Si la expresión es inválida o hay errores matemáticos.
    """
    stack = []
    tokens = expr.strip().split()
    i = 0
    while i < len(tokens):
        t = tokens[i]

        # Memoria separada: STO 01, RCL 09
        # Gestiona comandos especiales como STO (guardar en memoria) y RCL (recuperar de memoria).
        if t.upper() in ("STO", "RCL"):
            if i + 1 >= len(tokens):
                raise RPNError(f"Falta número de memoria tras '{t}'")
            m = tokens[i + 1]
            if m not in MEM:
                raise RPNError(f"Memoria inválida: '{m}'. Use 00-09.")
            if t.upper() == "STO":
                if not stack:
                    raise RPNError("Pila vacía para STO")
                MEM[m] = float(stack.pop())
            else:
                stack.append(MEM[m])
            i += 2
            continue

        # Token compuesto: STO01, RCL09
        if len(t) >= 5 and t[:3].upper() in ("STO", "RCL"):
            cmd = t[:3].upper()
            m = t[3:]
            if m not in MEM:
                raise RPNError(
                    f"Memoria inválida en '{t}'. Use STO00-STO09 o RCL00-RCL09."
                )
            if cmd == "STO":
                if not stack:
                    raise RPNError("Pila vacía para STO")
                MEM[m] = float(stack.pop())
            else:
                stack.append(MEM[m])
            i += 1
            continue

        # Números (enteros, reales, notación científica)
        try:
            if "." in t or ("e" in t.lower() and t.lower() != "e"):
                num = float(t)
            else:
                num = int(t)
            stack.append(float(num))
            i += 1
            continue
        except ValueError:
            pass

        # Constantes
        if t in CONST:
            stack.append(CONST[t])
            i += 1
            continue

        # Operadores aritméticos
        if t in ("+", "-", "*", "/"):
            if len(stack) < 2:
                raise RPNError(f"Faltan operandos para '{t}'")
            b = stack.pop()
            a = stack.pop()
            if t == "+":
                stack.append(a + b)
            elif t == "-":
                stack.append(a - b)
            elif t == "*":
                stack.append(a * b)
            elif t == "/":
                if b == 0:
                    raise RPNError("División por cero")
                stack.append(a / b)
            i += 1
            continue

        # Comandos de pila
        if t == "dup":
            if not stack:
                raise RPNError("'dup' requiere al menos un elemento")
            stack.append(stack[-1])
        elif t == "swap":
            if len(stack) < 2:
                raise RPNError("'swap' requiere al menos dos elementos")
            stack[-1], stack[-2] = stack[-2], stack[-1]
        elif t == "drop":
            if not stack:
                raise RPNError("'drop' requiere al menos un elemento")
            stack.pop()
        elif t == "clear":
            stack.clear()
        elif t in FUNC:
            arity, func = FUNC[t]
            if len(stack) < arity:
                raise RPNError(f"'{t}' necesita {arity} operandos")
            try:
                if arity == 1:
                    x = stack.pop()
                    stack.append(func(x))
                else:  # yx
                    x = stack.pop()
                    y = stack.pop()
                    stack.append(func(y, x))
            except ValueError as e:
                raise RPNError(f"Error dominio en '{t}': {e}") from e
            except ZeroDivisionError as e:
                raise RPNError(f"División por cero en '{t}'") from e
        else:
            raise RPNError(f"Token no reconocido: '{t}'")

        i += 1

    if len(stack) != 1:
        raise RPNError(
            f"Expresión incompleta: quedaron {len(stack)} valores (debe ser 1)"
        )
    return stack[0]


def main():
    """Punto de entrada principal. Permite que la calculadora reciba datos de dos formas:
    por argumentos de línea de comandos (ej. python rpn.py "3 4 +") o de forma interactiva
    pidiendo un input()."""
    if len(sys.argv) > 1:
        expr = " ".join(sys.argv[1:])
    else:
        try:
            expr = input("Ingrese expresión RPN: ")
        except EOFError:
            print("Error: sin entrada", file=sys.stderr)
            sys.exit(1)

    try:
        res = evaluate(expr)
        if isinstance(res, float) and res.is_integer():
            print(int(res))
        else:
            print(res)
    except RPNError as e:
        print(f"Error RPN: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error inesperado: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
