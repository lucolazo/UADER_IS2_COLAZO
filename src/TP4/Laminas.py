from abc import ABC, abstractmethod

# ---------- Implementador ----------
class Laminador(ABC):
    """Interfaz del tren laminador (Implementador)."""
    @abstractmethod
    def get_length(self) -> float:
        pass


class Mill5Meters(Laminador):
    """Tren que produce planchas de 5 metros."""
    def get_length(self) -> float:
        return 5.0


class Mill10Meters(Laminador):
    """Tren que produce planchas de 10 metros."""
    def get_length(self) -> float:
        return 10.0


# ---------- Abstracción ----------
class lamina:
    """
    Lámina de acero genérica de 0.5" de espesor y 1.5 m de ancho.
    Su largo depende del tren laminador asignado.
    """
    def __init__(self):
        self.thickness_inches = 0.5
        self.width_meters = 1.5
        self._rolling_mill = None  # El puente hacia la implementación

    def set_rolling_mill(self, mill: Laminador):
        """Indica a qué tren laminador se envía la lámina para producir."""
        self._rolling_mill = mill

    def produce(self):
        """Produce la lámina usando el tren laminador asignado y muestra las dimensiones."""
        if self._rolling_mill is None:
            raise ValueError("No se ha asignado un tren laminador. Use set_rolling_mill().")
        length = self._rolling_mill.get_length()
        print(f"Lámina producida: {self.thickness_inches}\" espesor, "
              f"{self.width_meters} m ancho, {length} m largo.")


# ---------- Cliente ----------
if __name__ == "__main__":
    lamina = lamina()

    # Usar el tren de 5 m
    lamina.set_rolling_mill(Mill5Meters())
    lamina.produce()

    # Cambiar al tren de 10 m (sin modificar la clase lamina)
    lamina.set_rolling_mill(Mill10Meters())
    lamina.produce()
