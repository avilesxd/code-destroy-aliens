import pygame
from pygame.sprite import Group
from configuracion import configuracion
from estadisticas import Estadisticas
from marcador import Marcador
from button import Button
from nave import Nave
from musica import musica
import funciones_juego as fj


# Icono de la ventana del juego
icono = pygame.image.load("./imagenes/icono.png")
pygame.display.set_icon(icono)


def runGame():
    # Inicializar el juego, las configuraciones y crear un objeto pantalla
    pygame.init()
    # Función para ejecutar la música
    musica()
    ai_configuracion = configuracion()
    pantalla = pygame.display.set_mode(
        (ai_configuracion.screen_width, ai_configuracion.screen_height))
    pygame.display.set_caption("Invasión alienígena")

    # Crea el botón Play
    play_button = Button(ai_configuracion, pantalla, "Jugar")

    # crea una instancia para almacenar estadísticas del juego y crea un marcador
    estadisticas = Estadisticas(ai_configuracion)
    marcador = Marcador(ai_configuracion, pantalla, estadisticas)

    # Crea una nave, un grupo de balas y un grupo de aliens
    nave = Nave(ai_configuracion, pantalla)
    balas = Group()
    aliens = Group()

    # Crea la flota de alienígenas
    fj.crear_flota(ai_configuracion, pantalla, nave, aliens)

    # Iniciar el bucle principal del juego
    while True:
        # Escuchar los eventos del teclado o del ratón
        fj.verificar_eventos(ai_configuracion, pantalla, estadisticas,
                             marcador, play_button, nave, aliens, balas)

        if estadisticas.game_active:
            nave.update()
            fj.update_balas(ai_configuracion, pantalla,
                            estadisticas, marcador, nave, aliens, balas)
            fj.update_aliens(ai_configuracion, estadisticas,
                             pantalla, marcador, nave, aliens, balas)

        fj.actualizar_pantalla(ai_configuracion, pantalla,
                               estadisticas, marcador, nave, aliens, balas, play_button)


runGame()
