#!/usr/bin/python
#*-------------------------------------------------------------------------*
#* factorial.py                                                            *
#* calcula el factorial de un número                                       *
#* Dr.P.E.Colla (c) 2022                                                   *
#* Creative commons                                                        *
#*-------------------------------------------------------------------------*

import sys

class Factorial:

    def __init__(self):
        pass

    def calcular(self, num):
        if num < 0:
            print("Factorial de un número negativo no existe")
            return 0
        elif num == 0:
            return 1
        else:
            fact = 1
            while num > 1:
                fact *= num
                num -= 1
            return fact

    def run(self, desde, hasta):
        for i in range(desde, hasta + 1):
            print("Factorial", i, "es", self.calcular(i))


if __name__ == "__main__":

    f = Factorial()

    # Entrada
    if len(sys.argv) < 2:
        entrada = input("Ingrese un número o rango (ej: 4-8, -10, 5-): ")
    else:
        entrada = sys.argv[1]

    try:
        # Caso rango abierto: -10
        if entrada.startswith("-"):
            desde = 1
            hasta = int(entrada[1:])
            f.run(desde, hasta)

        # Caso rango abierto: 5-
        elif entrada.endswith("-"):
            desde = int(entrada[:-1])
            hasta = 60
            f.run(desde, hasta)

        # Caso rango normal: 4-8
        elif "-" in entrada:
            desde, hasta = entrada.split("-")
            desde = int(desde)
            hasta = int(hasta)
            f.run(desde, hasta)

        # Caso número único
        else:
            num = int(entrada)
            print("Factorial", num, "es", f.calcular(num))

    except ValueError:
        print("Error: entrada inválida")
