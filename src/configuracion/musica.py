import pygame


def musica():
    # Inicializa la función para que se pueda empezar a reproducir la música
    pygame.mixer.init()
    # Variable para poder definir la música para el juego
    sonido = pygame.mixer.Sound("./src/musica/musica.mp3")
    # Configuración del volumen de la música
    sonido.set_volume(0.5)
    # Pasamos la variable con la musica y agregamos el valor "-1" para poder reproducir la música infinitamente
    pygame.mixer.Sound.play(sonido, -1)
