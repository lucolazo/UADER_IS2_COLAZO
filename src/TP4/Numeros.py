from abc import ABC, abstractmethod

# ---------- Componente (interfaz común) ----------
class NumeroBase(ABC):
    """Interfaz para números y decoradores."""
    @abstractmethod
    def obtener_valor(self) -> float:
        pass

    @abstractmethod
    def imprimir(self) -> None:
        pass


# ---------- Componente concreto (número original) ----------
class Numero(NumeroBase):
    """Representa un número cualquiera."""
    def __init__(self, valor: float):
        self._valor = valor

    def obtener_valor(self) -> float:
        return self._valor

    def imprimir(self) -> None:
        print(f"Valor base: {self._valor}")


# ---------- Decorador base ----------
class OperacionDecorador(NumeroBase):
    """Decorador abstracto que envuelve un NumeroBase."""
    def __init__(self, numero: NumeroBase):
        self._numero = numero

    def obtener_valor(self) -> float:
        return self._numero.obtener_valor()

    def imprimir(self) -> None:
        self._numero.imprimir()


# ---------- Decoradores concretos ----------
class Sumar2(OperacionDecorador):
    """Suma 2 al valor del componente."""
    def obtener_valor(self) -> float:
        return self._numero.obtener_valor() + 2

    def imprimir(self) -> None:
        print(f"Sumar2: {self.obtener_valor()}")


class Multiplicar2(OperacionDecorador):
    """Multiplica por 2 el valor del componente."""
    def obtener_valor(self) -> float:
        return self._numero.obtener_valor() * 2

    def imprimir(self) -> None:
        print(f"Multiplicar2: {self.obtener_valor()}")


class Dividir3(OperacionDecorador):
    """Divide por 3 el valor del componente."""
    def obtener_valor(self) -> float:
        return self._numero.obtener_valor() / 3

    def imprimir(self) -> None:
        print(f"Dividir3: {self.obtener_valor()}")


# ---------- Demostración ----------
if __name__ == "__main__":
    # Clase sin agregados
    numero = Numero(10)
    print("=== Sin agregados ===")
    numero.imprimir()
    print()

    # Agregados individuales (cada decorador aplicado al número original)
    print("=== Operaciones individuales sobre el número base ===")
    Sumar2(numero).imprimir()
    Multiplicar2(numero).imprimir()
    Dividir3(numero).imprimir()
    print()

    # Invocación anidada: Sumar2 -> Multiplicar2 -> Dividir3
    print("=== Invocación anidada (Sumar2 -> Multiplicar2 -> Dividir3) ===")
    anidado = Dividir3(Multiplicar2(Sumar2(numero)))
    anidado.imprimir()
