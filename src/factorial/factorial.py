#!/usr/bin/python
#*-------------------------------------------------------------------------*
#* factorial.py                                                            *
#* calcula el factorial de un número                                       *
#* Dr.P.E.Colla (c) 2022                                                   *
#* Creative commons                                                        *
#*-------------------------------------------------------------------------*
import sys
def factorial(num):
    if num < 0:
        print("Factorial de un número negativo no existe")
        return 0
    elif num == 0:
        return 1

    else:
        fact = 1
        while(num > 1):
            fact *= num
            num -= 1
        return fact

# si el número no se informa por línea de comandos, se solicita al usuario que lo ingrese por teclado
if len(sys.argv) < 2:
   print("Debe informar un número!")
   num = int(input("Ingrese un número: "))
# si el número se informa por línea de comandos, se convierte a entero
else:
    num=int(sys.argv[1])
print("Factorial ",num,"! es ", factorial(num))
