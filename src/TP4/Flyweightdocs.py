class FormatoCaracter:
    """Flyweight: estado compartible (fuente, tamaño, color, estilo)."""
    def __init__(self, fuente: str, tam: int, color: str, negrita: bool = False, cursiva: bool = False):
        self.fuente = fuente
        self.tam = tam
        self.color = color
        self.negrita = negrita
        self.cursiva = cursiva

    def __repr__(self):
        return f"Formato({self.fuente}, {self.tam}pt, {self.color}, negrita={self.negrita}, cursiva={self.cursiva})"


class FabricaFormato:
    """FlyweightFactory: almacena y reutiliza formatos ya creados."""
    _formatos = {}

    @classmethod
    def obtener(cls, fuente: str, tam: int, color: str, negrita=False, cursiva=False) -> FormatoCaracter:
        clave = (fuente, tam, color, negrita, cursiva)
        if clave not in cls._formatos:
            cls._formatos[clave] = FormatoCaracter(fuente, tam, color, negrita, cursiva)
            print(f"  [Nuevo flyweight] {cls._formatos[clave]}")
        else:
            print(f"  [Reutilizando]   {cls._formatos[clave]}")
        return cls._formatos[clave]


class Caracter:
    """Contexto: estado extrínseco (carácter, posición) + referencia al flyweight."""
    def __init__(self, simbolo: str, fila: int, col: int, formato: FormatoCaracter):
        self.simbolo = simbolo
        self.fila = fila
        self.col = col
        self.formato = formato

    def mostrar(self):
        print(f"'{self.simbolo}' en ({self.fila},{self.col}) con {self.formato}")


# --- Simulación ---
if __name__ == "__main__":
    doc = [
        Caracter('H', 1, 1, FabricaFormato.obtener("Arial", 12, "negro")),
        Caracter('o', 1, 2, FabricaFormato.obtener("Arial", 12, "negro")),
        Caracter('l', 1, 3, FabricaFormato.obtener("Arial", 12, "negro")),
        Caracter('a', 1, 4, FabricaFormato.obtener("Arial", 12, "negro", negrita=True)),
        Caracter('!', 1, 5, FabricaFormato.obtener("Arial", 12, "negro", negrita=True)),
        Caracter('M', 2, 1, FabricaFormato.obtener("Times", 10, "azul", cursiva=True)),
        Caracter('u', 2, 2, FabricaFormato.obtener("Times", 10, "azul", cursiva=True)),
        Caracter('n', 2, 3, FabricaFormato.obtener("Times", 10, "azul", cursiva=True)),
        Caracter('d', 2, 4, FabricaFormato.obtener("Times", 10, "azul", cursiva=True)),
        Caracter('o', 2, 5, FabricaFormato.obtener("Arial", 12, "negro")),   # Reutiliza el primer formato
    ]

    print("\nDocumento:")
    for c in doc:
        c.mostrar()

    print(f"\nTotal flyweights creados: {len(FabricaFormato._formatos)}")
