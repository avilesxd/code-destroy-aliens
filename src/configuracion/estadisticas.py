class Estadisticas():
    """Seguimiento de las estadísticas de Invasión alienígena"""

    def __init__(self, ai_configuracion):
        """Inicializa las estadísticas"""
        self.ai_configuracion = ai_configuracion
        self.reset_stats()

        # Inicia Invasión alienígena en un estado activo
        self.game_active = False

        # La puntuación alta nunca debe restablecerse
        self.alto_puntaje = 0

    def reset_stats(self):
        """Inicializa estadísticas que pueden cambiar durante el juego"""
        self.nave_restantes = self.ai_configuracion.cantidad_naves
        self.puntaje = 0
        self.nivel = 1
