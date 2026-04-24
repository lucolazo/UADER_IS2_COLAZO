#*------------------------------------------------------------------------
#* Ingeniería de Software II
#* Patrones de Creación - Factory Method
#* Aplicado a FACTURAS según condición impositiva
#*------------------------------------------------------------------------

from abc import ABC, abstractmethod

# -------------------- Producto abstracto --------------------
class Factura(ABC):
    """Interfaz común para todas las facturas."""
    def __init__(self, importe: float):
        self.importe = importe

    @abstractmethod
    def generar(self) -> str:
        """Retorna la representación de la factura."""
        pass

# -------------------- Productos concretos --------------------
class FacturaResponsable(Factura):
    def generar(self) -> str:
        iva = 21
        total = self.importe + (self.importe * iva / 100)
        return (f"FACTURA - IVA RESPONSABLE\n"
                f"   Importe neto: ${self.importe:.2f}\n"
                f"   IVA {iva}%: ${self.importe * iva / 100:.2f}\n"
                f"   TOTAL: ${total:.2f}")

class FacturaNoInscripto(Factura):
    def generar(self) -> str:
        return (f"FACTURA - IVA NO INSCRIPTO\n"
                f"   Importe total: ${self.importe:.2f}\n"
                f"   (No corresponde IVA)")

class FacturaExento(Factura):
    def generar(self) -> str:
        return (f"FACTURA - IVA EXENTO\n"
                f"   Importe total: ${self.importe:.2f}\n"
                f"   (Exento de IVA)")

# -------------------- Creador (Factory Method) --------------------
class CreadorFacturas:
    """Factory que instancia la factura adecuada según la condición impositiva."""
    @staticmethod
    def crear_factura(importe: float, condicion: str) -> Factura:
        """
        Retorna una instancia concreta de Factura según la condición.
        
        Args:
            importe: monto base de la factura.
            condicion: "responsable", "no_inscripto" o "exento".
        
        Returns:
            Factura concreta.
        
        Raises:
            ValueError: si la condición no es válida.
        """
        condicion = condicion.strip().lower()
        if condicion == "responsable":
            return FacturaResponsable(importe)
        elif condicion == "no_inscripto":
            return FacturaNoInscripto(importe)
        elif condicion == "exento":
            return FacturaExento(importe)
        else:
            raise ValueError(f"Condición impositiva '{condicion}' no válida")

#*------------------- Código de prueba -------------------
if __name__ == "__main__":
    print("=" * 50)
    print("SISTEMA DE FACTURACIÓN (Factory Method)")
    print("=" * 50)
    print()

    condiciones = ["responsable", "no_inscripto", "exento", "monotributo"]
    importe = 1000.00

    for condicion in condiciones:
        print(f"\n--- Cliente: {condicion.upper()} ---")
        try:
            factura = CreadorFacturas.crear_factura(importe, condicion)
            print(factura.generar())
        except ValueError as e:
            print(f"Error: {e}")
        print()
