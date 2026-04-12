#!/usr/bin/env python3
import sys, math

class RPNError(Exception): pass

CONST = {'p': math.pi, 'e': math.e, 'j': (1+math.sqrt(5))/2}
FUNC = {
    'sqrt': (1, math.sqrt), 'log': (1, math.log10), 'ln': (1, math.log),
    'ex': (1, math.exp), '10x': (1, lambda x: 10**x), '1/x': (1, lambda x: 1/x),
    'chs': (1, lambda x: -x), 'sin': (1, lambda x: math.sin(math.radians(x))),
    'cos': (1, lambda x: math.cos(math.radians(x))),
    'tg': (1, lambda x: math.tan(math.radians(x))),
    'asin': (1, lambda x: math.degrees(math.asin(x))),
    'acos': (1, lambda x: math.degrees(math.acos(x))),
    'atg': (1, lambda x: math.degrees(math.atan(x))),
    'yx': (2, lambda y,x: y**x)
}
MEM = {f"{i:02d}": 0.0 for i in range(10)}

def evaluate(expr):
    stack = []
    tokens = expr.strip().split()
    i = 0
    while i < len(tokens):
        t = tokens[i]
        # Memoria separada: STO 01, RCL 09
        if t.upper() in ('STO','RCL'):
            if i+1 >= len(tokens): raise RPNError(f"Falta número de memoria tras '{t}'")
            m = tokens[i+1]
            if m not in MEM: raise RPNError(f"Memoria inválida: '{m}'")
            if t.upper() == 'STO':
                if not stack: raise RPNError("Pila vacía para STO")
                MEM[m] = float(stack.pop())
            else: stack.append(MEM[m])
            i += 2; continue
        # Token compuesto: STO01, RCL09
        if len(t)>=5 and t[:3].upper() in ('STO','RCL'):
            cmd, m = t[:3].upper(), t[3:]
            if m not in MEM: raise RPNError(f"Memoria inválida en '{t}'")
            if cmd == 'STO':
                if not stack: raise RPNError("Pila vacía para STO")
                MEM[m] = float(stack.pop())
            else: stack.append(MEM[m])
            i += 1; continue
        # Números
        try:
            n = float(t) if '.' in t or 'e' in t.lower() else int(t)
            stack.append(float(n)); i += 1; continue
        except ValueError: pass
        # Constantes
        if t in CONST:
            stack.append(CONST[t]); i += 1; continue
        # Operadores básicos
        if t in '+-*/':
            if len(stack) < 2: raise RPNError(f"Faltan operandos para '{t}'")
            b, a = stack.pop(), stack.pop()
            if t == '+': stack.append(a+b)
            elif t == '-': stack.append(a-b)
            elif t == '*': stack.append(a*b)
            elif t == '/':
                if b == 0: raise RPNError("División por cero")
                stack.append(a/b)
            i += 1; continue
        # Comandos de pila
        if t == 'dup':
            if not stack: raise RPNError("'dup' requiere al menos un elemento")
            stack.append(stack[-1])
        elif t == 'swap':
            if len(stack) < 2: raise RPNError("'swap' requiere al menos dos elementos")
            stack[-1], stack[-2] = stack[-2], stack[-1]
        elif t == 'drop':
            if not stack: raise RPNError("'drop' requiere al menos un elemento")
            stack.pop()
        elif t == 'clear':
            stack.clear()
        # Funciones
        elif t in FUNC:
            arity, func = FUNC[t]
            if len(stack) < arity: raise RPNError(f"'{t}' necesita {arity} operandos")
            try:
                if arity == 1:
                    x = stack.pop()
                    stack.append(func(x))
                else:  # yx
                    x = stack.pop()
                    y = stack.pop()
                    stack.append(func(y, x))
            except ValueError as e: raise RPNError(f"Error dominio en '{t}': {e}")
            except ZeroDivisionError: raise RPNError(f"División por cero en '{t}'")
        else:
            raise RPNError(f"Token no reconocido: '{t}'")
        i += 1
    if len(stack) != 1:
        raise RPNError(f"Expresión incompleta: quedaron {len(stack)} valores (debe ser 1)")
    return stack[0]

def main():
    if len(sys.argv) > 1:
        expr = ' '.join(sys.argv[1:])
    else:
        try: expr = input("Ingrese expresión RPN: ")
        except EOFError: print("Error: sin entrada"); sys.exit(1)
    try:
        res = evaluate(expr)
        print(int(res) if isinstance(res, float) and res.is_integer() else res)
    except RPNError as e: print(f"Error RPN: {e}"); sys.exit(1)
    except Exception as e: print(f"Error inesperado: {e}"); sys.exit(1)

if __name__ == "__main__": main()
