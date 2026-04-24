#*------------------------------------------------------------------------
#* Ingeniería de Software II
#* Patrones de Creación - Factory Method
#*------------------------------------------------------------------------

from abc import ABC, abstractmethod

# -------------------- Producto abstracto --------------------
class Hamburguesa(ABC):
    """Interfaz común para todas las hamburguesas."""
    @abstractmethod
    def entregar(self) -> None:
        """Imprime el método de entrega específico."""
        pass

# -------------------- Productos concretos --------------------
class HamburguesaMostrador(Hamburguesa):
    def entregar(self) -> None:
        print("Hamburguesa entregada en MOSTRADOR")

class HamburguesaRetiro(Hamburguesa):
    def entregar(self) -> None:
        print("Hamburguesa RETIRADA por el cliente")

class HamburguesaDelivery(Hamburguesa):
    def entregar(self) -> None:
        print("Hamburguesa enviada por DELIVERY")

# -------------------- Creador (Factory Method) --------------------
class CreadorHamburguesas:
    """
    Clase que actúa como Factory Method.
    Centraliza la creación de hamburguesas según el método de entrega.
    """
    @staticmethod
    def crear_hamburguesa(metodo_entrega: str) -> Hamburguesa:
        """
        Método fábrica que retorna la instancia adecuada según el método.
        
        Args:
            metodo_entrega: "mostrador", "retiro" o "delivery"
        
        Returns:
            Hamburguesa concreta correspondiente
        
        Raises:
            ValueError: si el método no es válido
        """
        metodo = metodo_entrega.strip().lower()
        if metodo == "mostrador":
            return HamburguesaMostrador()
        elif metodo == "retiro":
            return HamburguesaRetiro()
        elif metodo == "delivery":
            return HamburguesaDelivery()
        else:
            raise ValueError(f"Método de entrega '{metodo_entrega}' no válido")


#*------------------- Código de prueba -------------------
if __name__ == "__main__":
    print("=" * 50)
    print("PEDIDOS DE HAMBURGUESAS (Factory Method)")
    print("=" * 50)

    # Lista de métodos de entrega
    metodos_entrega = ["mostrador", "retiro", "delivery", "moto"]

    # Se utiliza el creador (factory) para obtener la hamburguesa adecuada
    for metodo in metodos_entrega:
        try:
            hamburguesa = CreadorHamburguesas.crear_hamburguesa(metodo)
            hamburguesa.entregar()
        except ValueError as e:
            print(f"Error: {e}")
