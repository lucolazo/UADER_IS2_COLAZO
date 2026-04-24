#*------------------------------------------------------------------------
#* Ingeniería de Software II
#* Patrones de Creación - Builder
#* Extendido para construir AVIONES en lugar de vehículos
#*------------------------------------------------------------------------

from typing import NamedTuple

#* ------------------- Producto final -------------------
class Avion(NamedTuple):
    """Clase que representa un avión con sus componentes"""
    body: str
    turbinas: int
    alas: int
    tren_aterrizaje: str


#* ------------------- Builder Base -------------------
class AvionBuilder:
    """Builder base para construir aviones paso a paso"""

    def __init__(self):
        self.body = None
        self.turbinas = 0
        self.alas = 0
        self.tren_aterrizaje = None

    def set_body(self, body: str):
        self.body = body
        return self

    def set_turbinas(self, cantidad: int):
        self.turbinas = cantidad
        return self

    def set_alas(self, cantidad: int):
        self.alas = cantidad
        return self

    def set_tren_aterrizaje(self, tren: str):
        self.tren_aterrizaje = tren
        return self

    def build(self) -> Avion:
        """Construye y retorna el avión"""
        return Avion(
            body=self.body,
            turbinas=self.turbinas,
            alas=self.alas,
            tren_aterrizaje=self.tren_aterrizaje
        )


#* ------------------- Builders Específicos -------------------
class AvionComercialBuilder(AvionBuilder):
    """Builder para aviones comerciales (ej: Boeing 737)"""

    def __init__(self):
        super().__init__()
        self.body = "Fuselaje ancho (comercial)"
        self.turbinas = 2
        self.alas = 2
        self.tren_aterrizaje = "Triciclo (3 ruedas)"


class AvionMilitarBuilder(AvionBuilder):
    """Builder para aviones militares (ej: F-16)"""

    def __init__(self):
        super().__init__()
        self.body = "Fuselaje aerodinámico (militar)"
        self.turbinas = 2
        self.alas = 2
        self.tren_aterrizaje = "Tren reforzado (2 ruedas)"


class AvionCargaBuilder(AvionBuilder):
    """Builder para aviones de carga (ej: C-130 Hercules)"""

    def __init__(self):
        super().__init__()
        self.body = "Fuselaje robusto (carga)"
        self.turbinas = 2
        self.alas = 2
        self.tren_aterrizaje = "Tren multipropósito (4 ruedas)"


#* ------------------- Director (Opcional) -------------------
class DirectorAviones:
    """Director que guía la construcción de aviones"""

    @staticmethod
    def construir_avion_comercial() -> Avion:
        builder = AvionComercialBuilder()
        return builder.build()

    @staticmethod
    def construir_avion_militar() -> Avion:
        builder = AvionMilitarBuilder()
        return builder.build()

    @staticmethod
    def construir_avion_carga() -> Avion:
        builder = AvionCargaBuilder()
        return builder.build()

    @staticmethod
    def construir_avion_personalizado(
        body: str,
        turbinas: int,
        alas: int,
        tren: str
    ) -> Avion:
        builder = AvionBuilder()
        return (builder
                .set_body(body)
                .set_turbinas(turbinas)
                .set_alas(alas)
                .set_tren_aterrizaje(tren)
                .build())


#*------------------- Código de prueba -------------------
if __name__ == "__main__":
    print("=" * 60)
    print("--  SISTEMA DE CONSTRUCCIÓN DE AVIONES --")
    print("=" * 60)
    print()

    # Método 1: Usando builders específicos
    print("1. CONSTRUCCIÓN CON BUILDERS ESPECÍFICOS:")
    print("-" * 40)

    avion1 = AvionComercialBuilder().build()
    print(f"------ Avión Comercial: ------")
    print(f"   Body: {avion1.body}")
    print(f"   Turbinas: {avion1.turbinas}")
    print(f"   Alas: {avion1.alas}")
    print(f"   Tren de aterrizaje: {avion1.tren_aterrizaje}")
    print()

    avion2 = AvionMilitarBuilder().build()
    print(f"------ Avión Militar: ------")
    print(f"   Body: {avion2.body}")
    print(f"   Turbinas: {avion2.turbinas}")
    print(f"   Alas: {avion2.alas}")
    print(f"   Tren de aterrizaje: {avion2.tren_aterrizaje}")
    print()

    avion3 = AvionCargaBuilder().build()
    print(f"------ Avión de Carga: ------")
    print(f"   Body: {avion3.body}")
    print(f"   Turbinas: {avion3.turbinas}")
    print(f"   Alas: {avion3.alas}")
    print(f"   Tren de aterrizaje: {avion3.tren_aterrizaje}")
    print()

    # Método 2: Usando Director (más organizado)
    print("2. CONSTRUCCIÓN CON DIRECTOR:")
    print("-" * 40)

    avion4 = DirectorAviones.construir_avion_comercial()
    print(f"(Director) Avión Comercial: {avion4.body}")

    avion5 = DirectorAviones.construir_avion_militar()
    print(f"(Director) Avión Militar: {avion5.body}")

    avion6 = DirectorAviones.construir_avion_carga()
    print(f"(Director) Avión de Carga: {avion6.body}")
    print()

    # Método 3: Construcción paso a paso personalizada (como el builder.py original)
    print("3. CONSTRUCCIÓN PASO A PASO (como en builder.py):")
    print("-" * 40)

    builder = AvionBuilder()
    builder.body = "Fuselaje deportivo"
    builder.turbinas = 2
    builder.alas = 2
    builder.tren_aterrizaje = "Tren simple"
    avion7 = builder.build()

    print(f"------ Avión Personalizado paso a paso: ------")
    print(f"   Body: {avion7.body}")
    print(f"   Turbinas: {avion7.turbinas}")
    print(f"   Alas: {avion7.alas}")
    print(f"   Tren de aterrizaje: {avion7.tren_aterrizaje}")
    print()

    # Método 4: Construcción con encadenamiento de métodos (fluent interface)
    print("4. CONSTRUCCIÓN CON ENCADENAMIENTO (Fluent Interface):")
    print("-" * 40)

    avion8 = (AvionBuilder()
              .set_body("Fuselaje ejecutivo")
              .set_turbinas(2)
              .set_alas(2)
              .set_tren_aterrizaje("Tren de alta velocidad")
              .build())

    print(f"✈️ Avión Fluent Interface:")
    print(f"   Body: {avion8.body}")
    print(f"   Turbinas: {avion8.turbinas}")
    print(f"   Alas: {avion8.alas}")
    print(f"   Tren de aterrizaje: {avion8.tren_aterrizaje}")

    print("\n" + "=" * 60)
