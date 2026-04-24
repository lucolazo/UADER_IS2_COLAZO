#*------------------------------------------------------------------------
#* Ejemplo: Sistema de Reportes Multi-Formato
#* Patrón: Abstract Factory
#*------------------------------------------------------------------------
from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import datetime


#* ------------------- Productos Abstractos -------------------
class Header(ABC):
    """Encabezado del reporte"""
    @abstractmethod
    def renderizar(self) -> str:
        pass


class Body(ABC):
    """Cuerpo del reporte"""
    @abstractmethod
    def renderizar(self, datos: list) -> str:
        pass


class Footer(ABC):
    """Pie del reporte"""
    @abstractmethod
    def renderizar(self) -> str:
        pass


#* ------------------- Productos Concretos para PDF Corporativo -------------------
class PDFHeaderCorporativo(Header):
    def renderizar(self) -> str:
        return "[PDF] HEADER CORPORATIVO - Logo empresa + Nombre + Fecha"


class PDFBodyCorporativo(Body):
    def renderizar(self, datos: list) -> str:
        return f"[PDF] BODY CORPORATIVO - Tabla con bordes y colores institucionales\nDatos: {datos}"


class PDFFooterCorporativo(Footer):
    def renderizar(self) -> str:
        return f"[PDF] FOOTER CORPORATIVO - Pie de página con derechos reservados - Página 1/1"


#* ------------------- Productos Concretos para PDF Ejecutivo -------------------
class PDFHeaderEjecutivo(Header):
    def renderizar(self) -> str:
        return "[PDF] HEADER EJECUTIVO - Resumen ejecutivo + Indicadores clave"


class PDFBodyEjecutivo(Body):
    def renderizar(self, datos: list) -> str:
        return f"[PDF] BODY EJECUTIVO - Gráficos y tablas resumidas (solo totales)\nDatos: {datos[:2]}"  # Solo primeros 2


class PDFFooterEjecutivo(Footer):
    def renderizar(self) -> str:
        return "[PDF] FOOTER EJECUTIVO - Aprobado por: Gerencia General"


#* ------------------- Productos Concretos para HTML Corporativo -------------------
class HTMLHeaderCorporativo(Header):
    def renderizar(self) -> str:
        return "<div class='header'><h1>Reporte Corporativo</h1><hr/></div>"


class HTMLBodyCorporativo(Body):
    def renderizar(self, datos: list) -> str:
        html = "<table border='1'>"
        for dato in datos:
            html += f"<tr><td>{dato}</td></tr>"
        html += "</table>"
        return f"HTML BODY CORPORATIVO - {html}"


class HTMLFooterCorporativo(Footer):
    def renderizar(self) -> str:
        return "<div class='footer'>© 2024 - Todos los derechos reservados</div>"


#* ------------------- Abstract Factory -------------------
class ReporteFactory(ABC):
    """Fábrica abstracta que define la creación de una familia de productos"""

    @abstractmethod
    def crear_header(self) -> Header:
        pass

    @abstractmethod
    def crear_body(self) -> Body:
        pass

    @abstractmethod
    def crear_footer(self) -> Footer:
        pass


#* ------------------- Concrete Factories -------------------
class PDFReporteCorporativoFactory(ReporteFactory):
    def crear_header(self) -> Header:
        return PDFHeaderCorporativo()

    def crear_body(self) -> Body:
        return PDFBodyCorporativo()

    def crear_footer(self) -> Footer:
        return PDFFooterCorporativo()


class PDFReporteEjecutivoFactory(ReporteFactory):
    def crear_header(self) -> Header:
        return PDFHeaderEjecutivo()

    def crear_body(self) -> Body:
        return PDFBodyEjecutivo()

    def crear_footer(self) -> Footer:
        return PDFFooterEjecutivo()


class HTMLReporteCorporativoFactory(ReporteFactory):
    def crear_header(self) -> Header:
        return HTMLHeaderCorporativo()

    def crear_body(self) -> Body:
        return HTMLBodyCorporativo()

    def crear_footer(self) -> Footer:
        return HTMLFooterCorporativo()


#* ------------------- Cliente -------------------
class GeneradorReportes:
    """Cliente que trabaja con la fábrica abstracta"""

    def __init__(self, factory: ReporteFactory):
        self.factory = factory
        self.header = factory.crear_header()
        self.body = factory.crear_body()
        self.footer = factory.crear_footer()

    def generar(self, datos: list) -> str:
        """Genera el reporte completo usando los productos de la familia"""
        reporte = []
        reporte.append("=" * 50)
        reporte.append(self.header.renderizar())
        reporte.append("-" * 50)
        reporte.append(self.body.renderizar(datos))
        reporte.append("-" * 50)
        reporte.append(self.footer.renderizar())
        reporte.append("=" * 50)
        return "\n".join(reporte)


#*------------------- Código de prueba -------------------
if __name__ == "__main__":
    print("---- SISTEMA DE REPORTES CON ABSTRACT FACTORY ----")
    print("=" * 60)

    # Datos de ejemplo
    datos_ventas = ["Enero: $10,000", "Febrero: $12,000", "Marzo: $15,000", "Abril: $18,000"]

    # Diccionario de fábricas disponibles
    fabricas = {
        "pdf_corporativo": PDFReporteCorporativoFactory(),
        "pdf_ejecutivo": PDFReporteEjecutivoFactory(),
        "html_corporativo": HTMLReporteCorporativoFactory()
    }

    # Generar reportes con diferentes familias
    for nombre_fabrica, fabrica in fabricas.items():
        print(f"\n  Generando reporte: {nombre_fabrica.upper()}")
        print("-" * 40)

        generador = GeneradorReportes(fabrica)
        reporte = generador.generar(datos_ventas)
        print(reporte)
