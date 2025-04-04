import pygame
from src.utils import resource_path

def musica():
    # Inicializa la función para que se pueda empezar a reproducir la música
    pygame.mixer.init()
    
    # Usar resource_path() para obtener la ruta correcta de la música
    musica_path = resource_path("src/musica/musica.mp3")
    
    # Variable para poder definir la música para el juego
    sonido = pygame.mixer.Sound(musica_path)
    
    # Configuración del volumen de la música
    sonido.set_volume(0.5)
    
    # Pasamos la variable con la música y agregamos el valor "-1" para poder reproducir la música infinitamente
    pygame.mixer.Sound.play(sonido, -1)
