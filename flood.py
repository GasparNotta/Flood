import random
from cola import Cola

class Flood:
    """
    Clase para administrar un tablero de N colores.
    """

    def __init__(self, alto, ancho):
        """
        Genera un nuevo Flood de un mismo color con las dimensiones dadas.

        Args:
            alto (int): Altura de la grilla.
            ancho (int): Ancho de la grilla.
        """
        self.alto = alto
        self.ancho = ancho
        self.tablero = [[None] * ancho for _ in range(alto)]
        self.mezclar_tablero(5)

    def mezclar_tablero(self, n_colores):
        """
        Asigna de forma completamente aleatoria hasta `n_colores` a lo largo de
        las casillas del tablero.

        Args:
            n_colores (int): Cantidad máxima de colores a incluir en la grilla.
        """
        colores_posibles = list(range(1, n_colores + 1))
        for fila in range(self.alto):
            for col in range(self.ancho):
                self.tablero[fila][col] = random.choice(colores_posibles)

    def obtener_color(self, fil, col):
        """
        Devuelve el color que se encuentra en las coordenadas solicitadas.

        Args:
            fil (int): Posición de la fila en la grilla.
            col (int): Posición de la columna en la grilla.

        Returns:
            int: Color asignado.
        """
        if 0 <= fil < self.alto and 0 <= col < self.ancho:
            return self.tablero[fil][col]
        else:
            raise ValueError("Coordenadas fuera de los límites del tablero")

    def obtener_posibles_colores(self):
        """
        Devuelve una secuencia ordenada de todos los colores posibles del juego.

        Returns:
            iterable: Secuencia ordenada de colores.
        """
        colores_presentes = {color for fila in self.tablero for color in fila}
        return sorted(colores_presentes)

    def dimensiones(self):
        """
        Dimensiones de la grilla (filas y columnas)

        Returns:
            tuple: Alto y ancho de la grilla en ese orden.
        """
        return self.alto, self.ancho

    def cambiar_color(self, color_nuevo):
        """
        Asigna el nuevo color al Flood de la grilla. Es decir, a todas las
        coordenadas que formen un camino continuo del mismo color comenzando
        desde la coordenada origen en (0, 0) se les asignará `color_nuevo`

        Args:
            color_nuevo (int): Valor del nuevo color a asignar al Flood.
        """
        color_actual = self.obtener_color(0, 0)
 
        if color_actual == color_nuevo:
            return

        visitado = [[False] * self.ancho for _ in range(self.alto)]
        self._cambiar_color_recursivo(0, 0, color_actual, color_nuevo, visitado)

    def _cambiar_color_recursivo(self, fila, col, color_actual, color_nuevo, visitado):
        if 0 <= fila < self.alto and 0 <= col < self.ancho:
            if not visitado[fila][col] and self.obtener_color(fila, col) == color_actual:
                visitado[fila][col] = True
                self.tablero[fila][col] = color_nuevo
                self._cambiar_color_recursivo(fila - 1, col, color_actual, color_nuevo, visitado)  # Arriba
                self._cambiar_color_recursivo(fila + 1, col, color_actual, color_nuevo, visitado)  # Abajo
                self._cambiar_color_recursivo(fila, col - 1, color_actual, color_nuevo, visitado)  # Izquierda
                self._cambiar_color_recursivo(fila, col + 1, color_actual, color_nuevo, visitado)  # Derecha

    def clonar(self):
        """
        Returns:
            Flood: Copia del Flood actual.
        """
        nueva_instancia = Flood(self.alto, self.ancho)
        nueva_instancia.tablero = [fila.copy() for fila in self.tablero]
        return nueva_instancia

    def esta_completado(self):
        """
        Indica si todas las coordenadas de grilla tienen el mismo color.

        Returns:
            bool: True si toda la grilla tiene el mismo color.
        """
        color_base = self.obtener_color(0, 0)
        for fila in range(self.alto):
            for col in range(self.ancho):
                color_actual = self.obtener_color(fila, col)
                if color_actual != color_base:
                    return False
        return True

    def obtener_celdas_flood(self):
        """
        Returns:
            set: Conjunto de coordenadas (fil, col) que representan las celdas del Flood.
        """
        color_flood = self.obtener_color(0, 0)
        cola = Cola()
        visitadas = set()
        coordenadas_flood = set()

        cola.encolar((0, 0))
        visitadas.add((0, 0))

        while not cola.esta_vacia():
            fila, col = cola.desencolar()
            coordenadas_flood.add((fila, col))

            for fila_vecina, col_vecina in [(fila - 1, col), (fila + 1, col), (fila, col - 1), (fila, col + 1)]:
                if 0 <= fila_vecina < self.alto and 0 <= col_vecina < self.ancho:
                    vecina_color = self.obtener_color(fila_vecina, col_vecina)
                    if (fila_vecina, col_vecina) not in visitadas and vecina_color == color_flood:
                        cola.encolar((fila_vecina, col_vecina))
                        visitadas.add((fila_vecina, col_vecina))
        return coordenadas_flood

    def obtener_color_mas_adyacentes(self):
        """
        Returns:
            int: Color que tiene más celdas adyacentes al Flood en el estado actual del juego.
        """
        color_flood = self.obtener_color(0, 0)
        colores_adyacentes = {}

        coordenadas_flood = self.obtener_celdas_flood()

        for fila, col in coordenadas_flood:
            for fila_vecina, col_vecina in [(fila - 1, col), (fila + 1, col), (fila, col - 1), (fila, col + 1)]:
                if 0 <= fila_vecina < self.alto and 0 <= col_vecina < self.ancho:
                    vecina_color = self.obtener_color(fila_vecina, col_vecina)
                    if vecina_color != color_flood:
                        colores_adyacentes[vecina_color] = colores_adyacentes.get(vecina_color, 0) + 1
                        
        color_mas_adyacentes = max(colores_adyacentes, key=colores_adyacentes.get, default=None)

        return color_mas_adyacentes