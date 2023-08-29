class configuracion():
    """Sirve para almacenar todas las configuraciones de el juego"""

    def __init__(self):
        """Inicializa las configuraciones del  juego"""
        self.screen_width = 1280
        self.screen_height = 720
        self.bg_color = (230, 230, 230)

        # Configuraciones de la nave

        # Cantidad de vidas para el jugador
        self.cantidad_naves = 3

        # configuraciones de balas

        # Ancho de la bala
        self.bala_width = 3
        # Largo de la bala
        self.bala_height = 15
        # Color de la bala
        self.bala_color = 60, 60, 60
        # Cantidad de balas
        self.balas_allowed = 4

        # Configuraciones de alien

        # velocidad a la que los aliens van bajando cuando llegan al borde de la pantalla
        self.fleet_drop_speed = 1
        # Que tan rápido se acelera el juego
        self.escala_aceleracion = 1.1
        # Que tan rápido aumentan los valores de puntos por aliens
        self.escala_puntaje = 1.5

        self.inicializa_configuraciones_dinamicas()

    def inicializa_configuraciones_dinamicas(self):
        """Inicializa la configuración que cambia  a lo largo del juego"""
        # Velocidad de la nave
        self.factor_velocidad_nave = 1
        # Velocidad de las balas
        self.balas_factor_velocidad = 0.5
        # Velocidad de los aliens
        self.alien_speed_factor = 0.5
        # Fleet_direction, si es 1 representa a la derecha; si es -1 representa a la izquierda
        self.fleet_direction = 1
        # Puntuación
        self.puntos_alien = 50

    def aumentar_velocidad(self):
        """Aumenta la configuración de velocidad y los valores de puntos por aliens"""
        self.factor_velocidad_nave *= self.escala_aceleracion
        self.balas_factor_velocidad *= self.escala_aceleracion
        self.alien_speed_factor *= self.escala_aceleracion

        self.puntos_alien = int(self.puntos_alien * self.escala_puntaje)
