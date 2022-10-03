import pygame


def musica():
    # Inicializa la función para que se pueda empezar a reproducir la música
    pygame.mixer.init()
    # Variable para poder definir la música para el juego
    sonido = pygame.mixer.Sound("./musica/musica.mp3")
    # Configuración del volumen de la música
    sonido.set_volume(0.5)
    # Valor "-1" para poder reproducir la música infinitamente
    pygame.mixer.Sound.play(sonido, -1)
