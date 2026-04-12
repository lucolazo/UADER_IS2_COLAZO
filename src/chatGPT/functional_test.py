#!/usr/bin/env python3
"""
Test funcional para rpn.py
Ejecuta el programa como proceso externo y verifica salidas y códigos de retorno.
"""

import subprocess
import sys
import math

# Lista de casos de prueba: (expresión, salida_esperada, código_salida_esperado)
test_cases = [
    # Operaciones básicas
    ("3 4 +", "7", 0),
    ("-5 3 -", "-8.0", 0),
    ("2.5 4 *", "10.0", 0),
    ("7 2 /", "3.5", 0),
    # Expresiones compuestas (ejemplos del enunciado)
    ("5 1 2 + 4 * + 3 -", "14", 0),
    ("2 3 4 * +", "14", 0),
    # Constantes
    ("p", str(math.pi), 0),
    ("e", str(math.e), 0),
    ("j", str((1+math.sqrt(5))/2), 0),
    # Funciones matemáticas
    ("16 sqrt", "4.0", 0),
    ("100 log", "2.0", 0),
    ("e ln", "1.0", 0),
    ("1 ex", str(math.e), 0),
    ("2 10x", "100.0", 0),
    ("4 1/x", "0.25", 0),
    ("5 chs", "-5", 0),
    ("2 3 yx", "8.0", 0),
    # Trigonométricas (grados)
    ("90 sin", "1.0", 0),
    ("0 cos", "1.0", 0),
    ("45 tg", "0.9999999999999999", 0),
    ("1 asin", "90.0", 0),
    ("0.5 acos", "60.00000000000001", 0),
    ("1 atg", "45.0", 0),
    # Comandos de pila
    ("5 dup +", "10", 0),
    ("3 4 swap -", "1", 0),
    ("2 3 drop", "2", 0),
    ("1 2 3 clear 4 5 +", "9", 0),
    # Memorias
    ("100 STO 00 50 STO 01 RCL 00 RCL 01 +", "150", 0),
    ("42 STO07 RCL07", "42", 0),
    ("RCL 05", "0.0", 0),
    # Notación científica
    ("1.5e-1 2 *", "0.3", 0),
    # Errores (la salida relevante va a stderr)
    ("5 0 /", "Error RPN: División por cero", 1),
    ("3 4 &", "Error RPN: Token no reconocido: '&'", 1),
    ("3 +", "Error RPN: Faltan operandos para '+'", 1),
    ("3 4", "Error RPN: Expresión incompleta: quedaron 2 valores (debe ser 1)", 1),
    ("-1 sqrt", "Error RPN: Error dominio en 'sqrt': math domain error", 1),
    ("5 STO 10", "Error RPN: Memoria inválida: '10'. Use 00-09.", 1),
    ("STO 01", "Error RPN: Pila vacía para STO", 1),
    ("", "Error RPN: Expresión incompleta: quedaron 0 valores (debe ser 1)", 1),
]

def run_test(expression, expected_output, expected_retcode):
    """Ejecuta rpn.py con la expresión y retorna (éxito, salida_obtenida, código_obtenido)."""
    cmd = [sys.executable, "rpn.py", expression]
    result = subprocess.run(cmd, capture_output=True, text=True)
    stdout = result.stdout.strip()
    stderr = result.stderr.strip()
    retcode = result.returncode

    # Para errores, la salida relevante está en stderr; para éxito, en stdout
    output = stderr if expected_retcode != 0 else stdout

    # Comparación flexible: para éxito numérico usamos isclose, para errores verificamos substring
    success = False
    if expected_retcode != 0:
        success = expected_output in output
    else:
        try:
            expected_val = float(expected_output)
            actual_val = float(output)
            success = math.isclose(expected_val, actual_val, rel_tol=1e-9, abs_tol=1e-9)
        except ValueError:
            success = (output == expected_output)
    return success, output, retcode

def main():
    passed = 0
    failed = 0
    for expr, expected, retcode in test_cases:
        success, output, actual_ret = run_test(expr, expected, retcode)
        if success and actual_ret == retcode:
            passed += 1
            print(f"✓ {expr}")
        else:
            failed += 1
            print(f"✗ {expr}")
            print(f"  Esperado: {expected} (código {retcode})")
            print(f"  Obtenido: {output} (código {actual_ret})")
    print(f"\nResultados: {passed} pasaron, {failed} fallaron.")
    return failed == 0

if __name__ == "__main__":
    sys.exit(0 if main() else 1)
