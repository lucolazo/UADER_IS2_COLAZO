import subprocess
import sys

class Ping:
    """
    Clase que ejecuta ping a una dirección IP.
    - execute(string): realiza 10 intentos de ping solo si la IP comienza con "192."
    - executefree(string): realiza 10 intentos sin restricción de IP.
    """
    def execute(self, address: str) -> None:
        if not address.startswith("192."):
            print(f"Error: la dirección '{address}' no comienza con '192.'. Ping cancelado.")
            return
        self._do_ping(address)

    def executefree(self, address: str) -> None:
        self._do_ping(address)

    def _do_ping(self, address: str) -> None:
        """Realiza 10 intentos de ping. Aquí se simula con print por claridad.
        Para un ping real se puede usar subprocess, p.ej.:
        subprocess.run(["ping", "-c", "1", address], ...)
        """
        print(f"Iniciando 10 intentos de ping a {address}...")
        for i in range(1, 11):
            # Simulación de cada intento
            print(f"  Intento {i}: haciendo ping a {address}")
            # Descomentar la siguiente línea para hacer un ping real (Linux/Mac)
            # subprocess.run(["ping", "-c", "1", address], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"Ping a {address} completado.\n")


class PingProxy:
    """
    Proxy de la clase Ping.
    Si la dirección es '192.168.0.254', redirige el ping a www.google.com
    usando executefree(). En cualquier otro caso, reenvía la petición al execute() original.
    """
    def __init__(self, ping: Ping) -> None:
        self._ping = ping

    def execute(self, address: str) -> None:
        if address == "192.168.0.254":
            print(f"Proxy: IP especial '{address}' detectada. Redirigiendo a www.google.com")
            self._ping.executefree("www.google.com")
        else:
            # Reenvío al execute controlado
            self._ping.execute(address)


# Ejemplo de uso
if __name__ == "__main__":
    # Instanciamos la clase real
    real_ping = Ping()
    # Creamos el proxy
    proxy = PingProxy(real_ping)

    # Caso 1: IP normal que comienza con 192. (se ejecuta el ping controlado)
    print("--- Caso 1: 192.168.1.1 ---")
    proxy.execute("192.168.1.1")

    # Caso 2: IP que no comienza con 192. (el execute original rechaza)
    print("--- Caso 2: 10.0.0.1 ---")
    proxy.execute("10.0.0.1")

    # Caso 3: IP especial 192.168.0.254 (el proxy redirige a google)
    print("--- Caso 3: 192.168.0.254 ---")
    proxy.execute("192.168.0.254")

    # El método executefree sigue disponible sin control
    print("--- Caso 4: executefree directo a ejemplo.com ---")
    real_ping.executefree("ejemplo.com")
