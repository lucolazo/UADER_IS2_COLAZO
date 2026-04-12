#!/usr/bin/env python3
"""
Pruebas unitarias para rpn.py
Cobertura objetivo: >= 90%
"""

import unittest
import math
import sys
from io import StringIO
from unittest.mock import patch

import rpn


class TestRPNBasicOperations(unittest.TestCase):
    """Pruebas de operaciones básicas y pila."""

    def test_addition(self):
        self.assertEqual(rpn.evaluate("3 4 +"), 7.0)
        self.assertEqual(rpn.evaluate("2.5 1.5 +"), 4.0)

    def test_subtraction(self):
        self.assertEqual(rpn.evaluate("10 4 -"), 6.0)
        self.assertEqual(rpn.evaluate("-5 3 -"), -8.0)

    def test_multiplication(self):
        self.assertEqual(rpn.evaluate("6 7 *"), 42.0)
        self.assertEqual(rpn.evaluate("-2 3 *"), -6.0)

    def test_division(self):
        self.assertEqual(rpn.evaluate("8 2 /"), 4.0)
        self.assertEqual(rpn.evaluate("5 2 /"), 2.5)

    def test_division_by_zero_error(self):
        with self.assertRaises(rpn.RPNError) as cm:
            rpn.evaluate("5 0 /")
        self.assertIn("División por cero", str(cm.exception))

    def test_mixed_expression(self):
        self.assertEqual(rpn.evaluate("5 1 2 + 4 * + 3 -"), 14.0)
        self.assertEqual(rpn.evaluate("2 3 4 * +"), 14.0)

    def test_negative_numbers(self):
        self.assertEqual(rpn.evaluate("-3 -4 +"), -7.0)
        self.assertEqual(rpn.evaluate("-2.5 -1.5 *"), 3.75)

    def test_scientific_notation(self):
        self.assertAlmostEqual(rpn.evaluate("1e2 2e1 +"), 120.0)
        self.assertAlmostEqual(rpn.evaluate("1.5e-1 2 *"), 0.3)


class TestRPNStackCommands(unittest.TestCase):
    """Pruebas de comandos de manipulación de pila."""

    def test_dup(self):
        self.assertEqual(rpn.evaluate("5 dup +"), 10.0)
        self.assertEqual(rpn.evaluate("3 dup *"), 9.0)

    def test_dup_error_empty_stack(self):
        with self.assertRaises(rpn.RPNError) as cm:
            rpn.evaluate("dup")
        self.assertIn("'dup' requiere al menos un elemento", str(cm.exception))

    def test_swap(self):
        self.assertEqual(rpn.evaluate("3 4 swap -"), 1.0)
        self.assertEqual(rpn.evaluate("10 5 swap /"), 0.5)

    def test_swap_error_insufficient_stack(self):
        with self.assertRaises(rpn.RPNError) as cm:
            rpn.evaluate("3 swap")
        self.assertIn("'swap' requiere al menos dos elementos", str(cm.exception))

    def test_drop(self):
        self.assertEqual(rpn.evaluate("2 3 drop"), 2.0)
        self.assertEqual(rpn.evaluate("7 8 drop 2 +"), 9.0)

    def test_drop_error_empty_stack(self):
        with self.assertRaises(rpn.RPNError) as cm:
            rpn.evaluate("drop")
        self.assertIn("'drop' requiere al menos un elemento", str(cm.exception))

    def test_clear(self):
        self.assertEqual(rpn.evaluate("1 2 3 clear 4 5 +"), 9.0)

    def test_clear_on_empty_stack(self):
        self.assertEqual(rpn.evaluate("clear 5"), 5.0)


class TestRPNConstants(unittest.TestCase):
    """Pruebas de constantes predefinidas."""

    def test_pi(self):
        self.assertAlmostEqual(rpn.evaluate("p"), math.pi)
        self.assertAlmostEqual(rpn.evaluate("2 p *"), 2 * math.pi)

    def test_e(self):
        self.assertAlmostEqual(rpn.evaluate("e"), math.e)
        self.assertAlmostEqual(rpn.evaluate("e e *"), math.e ** 2)

    def test_phi(self):
        phi = (1 + math.sqrt(5)) / 2
        self.assertAlmostEqual(rpn.evaluate("j"), phi)
        self.assertAlmostEqual(rpn.evaluate("j dup * j -"), 1.0)


class TestRPNFunctions(unittest.TestCase):
    """Pruebas de funciones matemáticas."""

    def test_sqrt(self):
        self.assertEqual(rpn.evaluate("9 sqrt"), 3.0)
        self.assertEqual(rpn.evaluate("2 sqrt"), math.sqrt(2))

    def test_sqrt_negative_error(self):
        with self.assertRaises(rpn.RPNError) as cm:
            rpn.evaluate("-1 sqrt")
        self.assertIn("Error dominio en 'sqrt'", str(cm.exception))

    def test_log(self):
        self.assertEqual(rpn.evaluate("100 log"), 2.0)
        self.assertEqual(rpn.evaluate("1 log"), 0.0)

    def test_log_non_positive_error(self):
        with self.assertRaises(rpn.RPNError):
            rpn.evaluate("0 log")
        with self.assertRaises(rpn.RPNError):
            rpn.evaluate("-10 log")

    def test_ln(self):
        self.assertEqual(rpn.evaluate("1 ln"), 0.0)
        self.assertAlmostEqual(rpn.evaluate("e ln"), 1.0)

    def test_ex(self):
        self.assertEqual(rpn.evaluate("0 ex"), 1.0)
        self.assertAlmostEqual(rpn.evaluate("1 ex"), math.e)

    def test_10x(self):
        self.assertEqual(rpn.evaluate("0 10x"), 1.0)
        self.assertEqual(rpn.evaluate("2 10x"), 100.0)
        self.assertEqual(rpn.evaluate("3 10x"), 1000.0)

    def test_inverse(self):
        self.assertEqual(rpn.evaluate("4 1/x"), 0.25)
        self.assertEqual(rpn.evaluate("2 1/x"), 0.5)

    def test_inverse_zero_error(self):
        with self.assertRaises(rpn.RPNError) as cm:
            rpn.evaluate("0 1/x")
        self.assertIn("División por cero en '1/x'", str(cm.exception))

    def test_chs(self):
        self.assertEqual(rpn.evaluate("5 chs"), -5.0)
        self.assertEqual(rpn.evaluate("-3.2 chs"), 3.2)
        self.assertEqual(rpn.evaluate("0 chs"), 0.0)

    def test_yx(self):
        self.assertEqual(rpn.evaluate("2 3 yx"), 8.0)
        self.assertEqual(rpn.evaluate("4 0.5 yx"), 2.0)
        self.assertEqual(rpn.evaluate("9 0.5 yx"), 3.0)


class TestRPNTrigonometric(unittest.TestCase):
    """Pruebas de funciones trigonométricas (en grados)."""

    def test_sin(self):
        self.assertAlmostEqual(rpn.evaluate("90 sin"), 1.0)
        self.assertAlmostEqual(rpn.evaluate("0 sin"), 0.0)
        self.assertAlmostEqual(rpn.evaluate("30 sin"), 0.5)

    def test_cos(self):
        self.assertAlmostEqual(rpn.evaluate("0 cos"), 1.0)
        self.assertAlmostEqual(rpn.evaluate("60 cos"), 0.5)

    def test_tg(self):
        self.assertAlmostEqual(rpn.evaluate("45 tg"), 1.0)
        self.assertAlmostEqual(rpn.evaluate("0 tg"), 0.0)

    def test_asin(self):
        self.assertAlmostEqual(rpn.evaluate("1 asin"), 90.0)
        self.assertAlmostEqual(rpn.evaluate("0 asin"), 0.0)
        self.assertAlmostEqual(rpn.evaluate("0.5 asin"), 30.0)

    def test_asin_domain_error(self):
        with self.assertRaises(rpn.RPNError):
            rpn.evaluate("2 asin")
        with self.assertRaises(rpn.RPNError):
            rpn.evaluate("-2 asin")

    def test_acos(self):
        self.assertAlmostEqual(rpn.evaluate("1 acos"), 0.0)
        self.assertAlmostEqual(rpn.evaluate("0 acos"), 90.0)
        self.assertAlmostEqual(rpn.evaluate("0.5 acos"), 60.0)

    def test_acos_domain_error(self):
        with self.assertRaises(rpn.RPNError):
            rpn.evaluate("1.5 acos")

    def test_atg(self):
        self.assertAlmostEqual(rpn.evaluate("0 atg"), 0.0)
        self.assertAlmostEqual(rpn.evaluate("1 atg"), 45.0)


class TestRPNMemory(unittest.TestCase):
    """Pruebas de memorias y comandos STO / RCL."""

    def setUp(self):
        # Reiniciar memorias antes de cada prueba
        rpn.MEM = {f"{i:02d}": 0.0 for i in range(10)}

    def test_store_and_recall_separate_tokens(self):
        # Expresión completa que termina con un valor
        self.assertEqual(rpn.evaluate("100 STO 00 50 STO 01 RCL 00 RCL 01 +"), 150.0)

    def test_store_and_recall_compound_tokens(self):
        self.assertEqual(rpn.evaluate("42 STO07 RCL07"), 42.0)

    def test_recall_default_zero(self):
        self.assertEqual(rpn.evaluate("RCL 05"), 0.0)

    def test_overwrite_memory(self):
        # Almacenar dos veces y recuperar al final para que quede un valor en pila
        self.assertEqual(rpn.evaluate("10 STO 03 20 STO 03 RCL 03"), 20.0)

    def test_memory_persistence(self):
        # Se evalúa una expresión que almacena y devuelve el valor (para que no falle)
        rpn.evaluate("3.1416 STO 09 RCL 09")
        self.assertAlmostEqual(rpn.evaluate("2 RCL 09 *"), 6.2832)

    def test_sto_missing_memory_number(self):
        with self.assertRaises(rpn.RPNError) as cm:
            rpn.evaluate("5 STO")
        self.assertIn("Falta número de memoria tras 'STO'", str(cm.exception))

    def test_rcl_missing_memory_number(self):
        with self.assertRaises(rpn.RPNError) as cm:
            rpn.evaluate("RCL")
        self.assertIn("Falta número de memoria tras 'RCL'", str(cm.exception))

    def test_invalid_memory_separate(self):
        with self.assertRaises(rpn.RPNError) as cm:
            rpn.evaluate("5 STO 10")
        self.assertIn("Memoria inválida: '10'", str(cm.exception))

    def test_invalid_memory_compound(self):
        with self.assertRaises(rpn.RPNError) as cm:
            rpn.evaluate("5 STO15")
        self.assertIn("Memoria inválida en 'STO15'", str(cm.exception))

    def test_sto_empty_stack(self):
        with self.assertRaises(rpn.RPNError) as cm:
            rpn.evaluate("STO 01")
        self.assertIn("Pila vacía para STO", str(cm.exception))

    def test_sto_empty_stack_compound(self):
        with self.assertRaises(rpn.RPNError) as cm:
            rpn.evaluate("STO01")
        self.assertIn("Pila vacía para STO", str(cm.exception))


class TestRPNErrors(unittest.TestCase):
    """Pruebas de manejo de errores generales."""

    def test_insufficient_operands_operator(self):
        with self.assertRaises(rpn.RPNError) as cm:
            rpn.evaluate("3 +")
        self.assertIn("Faltan operandos para '+'", str(cm.exception))

    def test_insufficient_operands_function(self):
        with self.assertRaises(rpn.RPNError) as cm:
            rpn.evaluate("sqrt")
        self.assertIn("'sqrt' necesita 1 operandos", str(cm.exception))

    def test_insufficient_operands_yx(self):
        with self.assertRaises(rpn.RPNError) as cm:
            rpn.evaluate("2 yx")
        self.assertIn("'yx' necesita 2 operandos", str(cm.exception))

    def test_stack_not_single_element_final(self):
        with self.assertRaises(rpn.RPNError) as cm:
            rpn.evaluate("3 4")
        self.assertIn("quedaron 2 valores", str(cm.exception))

        with self.assertRaises(rpn.RPNError) as cm:
            rpn.evaluate("1 2 3 +")
        self.assertIn("quedaron 2 valores", str(cm.exception))

    def test_empty_expression(self):
        with self.assertRaises(rpn.RPNError) as cm:
            rpn.evaluate("")
        self.assertIn("quedaron 0 valores", str(cm.exception))

    def test_invalid_token(self):
        with self.assertRaises(rpn.RPNError) as cm:
            rpn.evaluate("3 4 &")
        self.assertIn("Token no reconocido: '&'", str(cm.exception))

    def test_invalid_function_name(self):
        with self.assertRaises(rpn.RPNError) as cm:
            rpn.evaluate("3 cube")
        self.assertIn("Token no reconocido: 'cube'", str(cm.exception))


class TestRPNMainFunction(unittest.TestCase):
    """Pruebas de la función main() y entrada/salida."""

    def test_main_with_command_line_argument(self):
        test_args = ["rpn.py", "3 4 +"]
        with patch.object(sys, 'argv', test_args):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                rpn.main()
                self.assertEqual(mock_stdout.getvalue().strip(), "7")

    def test_main_with_multiple_arguments(self):
        test_args = ["rpn.py", "5", "1", "2", "+", "4", "*", "+", "3", "-"]
        with patch.object(sys, 'argv', test_args):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                rpn.main()
                self.assertEqual(mock_stdout.getvalue().strip(), "14")

    def test_main_with_stdin_input(self):
        with patch.object(sys, 'argv', ["rpn.py"]):
            with patch('sys.stdin', StringIO("10 2 /\n")):
                with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                    rpn.main()
                    output = mock_stdout.getvalue()
                    prompt = "Ingrese expresión RPN: "
                    self.assertIn(prompt, output)
                    # Eliminar el prompt para quedarnos con el resultado
                    result_str = output.replace(prompt, "").strip()
                    self.assertEqual(result_str, "5")
    
    def test_main_eof_error(self):
        with patch.object(sys, 'argv', ["rpn.py"]):
            with patch('builtins.input', side_effect=EOFError):
                with patch('sys.stderr', new_callable=StringIO):
                    with self.assertRaises(SystemExit) as cm:
                        rpn.main()
                    self.assertEqual(cm.exception.code, 1)

    def test_main_rpn_error(self):
        with patch.object(sys, 'argv', ["rpn.py", "3 +"]):
            with patch('sys.stderr', new_callable=StringIO):
                with self.assertRaises(SystemExit) as cm:
                    rpn.main()
                self.assertEqual(cm.exception.code, 1)

    def test_main_unexpected_exception(self):
        with patch.object(sys, 'argv', ["rpn.py", "1 1 +"]):
            with patch('rpn.evaluate', side_effect=Exception("Error inesperado")):
                with patch('sys.stderr', new_callable=StringIO):
                    with self.assertRaises(SystemExit) as cm:
                        rpn.main()
                    self.assertEqual(cm.exception.code, 1)


if __name__ == '__main__':
    unittest.main()
