#*------------------------------------------------------------------------
#* Ingeniería de Software II
#* Patrones de Creación - Prototype
#* Verificación simplificada: una clase derivada de un prototipo puede clonarse a sí misma
#*------------------------------------------------------------------------
import copy
from abc import ABC, abstractmethod


class Prototype(ABC):
    """Interfaz que define el método de clonación."""
    @abstractmethod
    def clone(self):
        pass


class Avion(Prototype):
    """Clase base que implementa Prototype (avión genérico)."""
    def __init__(self, modelo: str, velocidad: int, capacidad: int, componentes: list = None):
        self.modelo = modelo
        self.velocidad = velocidad
        self.capacidad = capacidad
        self.componentes = componentes if componentes is not None else []

    def agregar_componente(self, componente: str):
        self.componentes.append(componente)

    def clone(self):
        """Clona el avión usando copia profunda para independencia total."""
        return copy.deepcopy(self)

    def __str__(self):
        return f"Avión: {self.modelo} | Vel: {self.velocidad} km/h | Cap: {self.capacidad} | Comp: {self.componentes}"


class AvionCombate(Avion):
    """Clase derivada de Avion (generada a partir del prototipo). Debe poder clonarse."""
    def __init__(self, modelo: str, velocidad: int, capacidad: int, armamento: list = None, componentes: list = None):
        super().__init__(modelo, velocidad, capacidad, componentes)
        self.armamento = armamento if armamento is not None else []

    def agregar_arma(self, arma: str):
        self.armamento.append(arma)

    def __str__(self):
        return (f"AvionCombate: {self.modelo} | Vel: {self.velocidad} km/h | "
                f"Cap: {self.capacidad} | Arm: {self.armamento} | Comp: {self.componentes}")


def main():
    # ----- Prototipo base (Avion) -----
    avion_original = Avion("Boeing 747", 900, 300, ["Motor", "Alas"])
    avion_original.agregar_componente("Tren de aterrizaje")
    print("=== Avión Original ===")
    print(avion_original)

    clon_avion = avion_original.clone()
    clon_avion.modelo = "Boeing 747 - Copia"
    clon_avion.agregar_componente("Radar")
    print("\n=== Clon Modificado ===")
    print(clon_avion)
    print("\n=== Original (sin cambios) ===")
    print(avion_original)

    # ----- Clase derivada (AvionCombate) -----
    print("\n" + "=" * 50)
    combate_original = AvionCombate("F-16", 2400, 1, ["AIM-9"], ["Motor", "Alas"])
    combate_original.agregar_arma("Cañón M61")
    print("=== Avión de Combate Original (clase derivada de Avion) ===")
    print(combate_original)

    # Clonación de la clase derivada (demuestra que ella misma puede dar copias de sí)
    combate_copia1 = combate_original.clone()
    combate_copia1.modelo = "F-16 - Copia 1"
    combate_copia1.agregar_arma("Bomba JDAM")
    print("\n=== Primera Copia de Combate (modificada) ===")
    print(combate_copia1)

    # La copia también puede clonarse (segunda generación)
    combate_copia2 = combate_copia1.clone()
    combate_copia2.modelo = "F-16 - Copia 2"
    combate_copia2.agregar_arma("Misil extra")
    print("\n=== Segunda Copia (desde la primera copia) ===")
    print(combate_copia2)

    print("\n=== Original de Combate (sin cambios) ===")
    print(combate_original)


if __name__ == "__main__":
    main()
