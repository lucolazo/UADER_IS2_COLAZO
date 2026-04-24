#*------------------------------------------------------------------------
#* Ingeniería de Software II
#* Patrones de Creación - Singleton
#*------------------------------------------------------------------------

import threading

class SingletonFactorial:
    _instancia = None
    _lock = threading.Lock()
    _memoria = {}

    def new(cls):
        if cls._instancia is None:
            with cls._lock:
                if cls._instancia is None:
                    cls._instancia = super().new(cls)
        return cls._instancia

    def factorial(self, n):
        if n < 0:
            raise ValueError("Factorial no definido para negativos")

        if n in self._memoria:
            return self._memoria[n]

        with self._lock:
            if n in self._memoria:
                return self._memoria[n]

            if n == 0 or n == 1:
                resultado = 1
            else:
                resultado = 1
                for i in range(2, n + 1):
                    resultado *= i
            self._memoria[n] = resultado
            return resultado


calc1 = SingletonFactorial()
calc2 = SingletonFactorial()
print(calc1 is calc2)
print(calc1.factorial(5))
print(calc2.factorial(6))
