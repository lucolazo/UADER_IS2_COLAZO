from abc import ABC, abstractmethod

# ---------- Componente (interfaz común) ----------
class Componente(ABC):
    """Clase abstracta para todos los elementos (hojas y compuestos)."""
    @abstractmethod
    def mostrar(self, nivel: int = 0) -> None:
        pass


# ---------- Hoja (Leaf) ----------
class Pieza(Componente):
    """Representa una pieza indivisible."""
    def __init__(self, nombre: str):
        self.nombre = nombre

    def mostrar(self, nivel: int = 0) -> None:
        indentacion = "  " * nivel
        print(f"{indentacion}- Pieza: {self.nombre}")


# ---------- Compuesto (Composite) ----------
class Ensamblado(Componente):
    """Representa un sub-conjunto o producto que puede contener otras piezas o ensamblados."""
    def __init__(self, nombre: str):
        self.nombre = nombre
        self._componentes = []

    def agregar(self, componente: Componente) -> None:
        self._componentes.append(componente)

    def mostrar(self, nivel: int = 0) -> None:
        indentacion = "  " * nivel
        print(f"{indentacion}+ {self.nombre}")
        for componente in self._componentes:
            componente.mostrar(nivel + 1)


# ---------- Construcción y demostración ----------
if __name__ == "__main__":
    # 1. Crear el producto principal con 3 sub-conjuntos de 4 piezas cada uno
    producto_principal = Ensamblado("Producto Principal")

    for i in range(1, 4):
        subconjunto = Ensamblado(f"Subconjunto {i}")
        for j in range(1, 5):
            subconjunto.agregar(Pieza(f"Pieza {i}.{j}"))
        producto_principal.agregar(subconjunto)

    # 2. Agregar un subconjunto opcional adicional con 4 piezas
    subconjunto_opcional = Ensamblado("Subconjunto Opcional")
    for j in range(1, 5):
        subconjunto_opcional.agregar(Pieza(f"Pieza Opcional {j}"))
    producto_principal.agregar(subconjunto_opcional)

    # 3. Mostrar la estructura jerárquica completa
    print("Estructura del ensamblado:\n")
    producto_principal.mostrar()
