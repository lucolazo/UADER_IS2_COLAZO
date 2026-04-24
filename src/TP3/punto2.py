#*------------------------------------------------------------------------
#* Ingeniería de Software II
#* Patrones de Creación - Singleton
#*------------------------------------------------------------------------

import threading

class CalculadoraImpuestos:
    """
    Clase Singleton que centraliza el cálculo de impuestos.
    IVA: 21%, IIBB: 5%, Contribuciones Municipales: 1.2%
    """
    _instancia = None
    _lock = threading.Lock()

    # Porcentajes como constantes de clase
    IVA = 0.21
    IIBB = 0.05
    CONTRIB_MUNICIPAL = 0.012

    def new(cls):
        if cls._instancia is None:
            with cls._lock:
                if cls._instancia is None:
                    cls._instancia = super().new(cls)
        return cls._instancia

    def calcular_impuestos(self, base_imponible: float) -> float:
        """
        Calcula y retorna la suma total de impuestos sobre una base imponible.

        Args:
            base_imponible (float): Importe sobre el cual aplicar los impuestos.

        Returns:
            float: Total de impuestos (IVA + IIBB + Contribuciones Municipales).

        Raises:
            ValueError: Si la base imponible es negativa.
        """
        if base_imponible < 0:
            raise ValueError("La base imponible no puede ser negativa.")

        iva = base_imponible * self.IVA
        iibb = base_imponible * self.IIBB
        municipal = base_imponible * self.CONTRIB_MUNICIPAL

        return iva + iibb + municipal



# Ejemplo de uso
calc_impuestos1 = CalculadoraImpuestos()
calc_impuestos2 = CalculadoraImpuestos()

base = 4570.0
total_impuestos = calc_impuestos1.calcular_impuestos(base)
print(f"Base: ${base:.2f}")
print(f"IVA (21%): ${base * CalculadoraImpuestos.IVA:.2f}")
print(f"IIBB (5%): ${base * CalculadoraImpuestos.IIBB:.2f}")
print(f"Contribuciones Municipales (1.2%): ${base * CalculadoraImpuestos.CONTRIB_MUNICIPAL:.2f}")
print(f"Total impuestos: ${total_impuestos:.2f}")
