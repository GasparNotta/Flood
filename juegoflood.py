from flood import Flood
from pila import Pila
from cola import Cola


class JuegoFlood:
    """
    Clase para administrar un Flood, junto con sus estados y acciones
    """

    def __init__(self, alto, ancho, n_colores):
        """
        Genera un nuevo JuegoFlood con un Flood y otros atributos para realizar las acciones del juego.

        Args:
            alto (int): Altura de la grilla del Flood.
            ancho (int): Ancho de la grilla del Flood.
            n_colores (int): Cantidad máxima de colores a incluir en la grilla.
        """
        self.flood = Flood(alto, ancho)
        self.flood.mezclar_tablero(n_colores)
        self.mejor_n_movimientos, _ = self._calcular_movimientos()
        self.n_movimientos = 0
        self.pasos_solucion = Cola()
        self.estados_anteriores = Pila()
        self.estados_posteriores = Pila()

    def cambiar_color(self, color):
        """
        Realiza la acción para seleccionar un color en el Flood, suma la cantidad de movimientos
        y maneja las estructuras para deshacer y rehacer.

        Args:
            color (int): Nuevo color a seleccionar.
        """
        # Realizar una copia del estado actual del juego
        estado_actual = self.flood.clonar()

        self.n_movimientos += 1
        self.flood.cambiar_color(color)

        if not self.pasos_solucion.esta_vacia() and self.pasos_solucion.ver_frente() == color:
            self.pasos_solucion.desencolar()
        else:
            self.pasos_solucion = Cola()

        # Apilar el estado actual en la pila de estados anteriores
        self.estados_anteriores.apilar(estado_actual)

    def deshacer(self):
        """
        Deshace el último movimiento realizado si existen pasos previos,
        manejando las estructuras para deshacer y rehacer.
        """
        if not self.estados_anteriores.esta_vacia():
            # Desapilar el estado actual
            estado_actual = self.flood.clonar()
            self.estados_posteriores.apilar(estado_actual)

            # Restaurar el estado anterior desde la pila
            estado_anterior = self.estados_anteriores.desapilar()
            self.flood = estado_anterior

            # Decrementar el contador de movimientos
            self.n_movimientos -= 1

    def rehacer(self):
        """
        Rehace el movimiento que fue deshecho si existe, manejando las
        estructuras para deshacer y rehacer.
        """
        if not self.estados_posteriores.esta_vacia():
            # Desapilar el estado actual
            estado_actual = self.flood.clonar()
            self.estados_anteriores.apilar(estado_actual)

            # Restaurar el estado siguiente desde la pila de estados posteriores
            estado_siguiente = self.estados_posteriores.desapilar()
            self.flood = estado_siguiente

            # Incrementar el contador de movimientos
            self.n_movimientos += 1

    def _calcular_movimientos(self):
        """
        Realiza una solución de pasos contra el Flood actual (en una Cola)
        y devuelve la cantidad de movimientos que llevó a esa solución.

        Criterio del algoritmo de solución:
        Se evalúa cada color adyacente y se selecciona el color que agrega más casillas al flood actual.

        Returns:
            int: Cantidad de movimientos que llevó a la solución encontrada.
            Cola: Pasos utilizados para llegar a dicha solución.
        """
        juego_copia = self.flood.clonar()
        movimientos = 0
        pasos = Cola()

        while not juego_copia.esta_completado():
            movimientos += 1

            # Obtener el color que tiene más celdas adyacentes
            mejor_color = juego_copia.obtener_color_mas_adyacentes()

            # Cambiar el color del Flood y registrar el movimiento
            juego_copia.cambiar_color(mejor_color)
            pasos.encolar(mejor_color)

        return movimientos, pasos

    def hay_proximo_paso(self):
        """
        Devuelve un booleano indicando si hay una solución calculada.
        """
        return not self.pasos_solucion.esta_vacia()

    def proximo_paso(self):
        """
        Si hay una solución calculada, devuelve el próximo paso.
        Caso contrario, devuelve ValueError.

        Returns:
            Color: Color del próximo paso de la solución.
        """
        return self.pasos_solucion.ver_frente()

    def calcular_nueva_solucion(self):
        """
        Calcula una secuencia de pasos que solucionan el estado actual
        del flood, de tal forma que se pueda llamar al método `proximo_paso()`.
        """
        _, self.pasos_solucion = self._calcular_movimientos()

    def dimensiones(self):
        return self.flood.dimensiones()

    def obtener_color(self, fil, col):
        return self.flood.obtener_color(fil, col)

    def obtener_posibles_colores(self):
        return self.flood.obtener_posibles_colores()

    def esta_completado(self):
        return self.flood.esta_completado()