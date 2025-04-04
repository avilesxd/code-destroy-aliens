import pygame
from pygame.sprite import Sprite
from src.utils import resource_path

class Alien(Sprite):
    """Sirve para representar a un solo alienígena en la flota"""

    def __init__(self, ai_configuracion, pantalla):
        """Inicializa el alien y establece su posición inicial"""
        super(Alien, self).__init__()

        self.pantalla = pantalla
        self.ai_configuracion = ai_configuracion

        # Usamos resource_path() para obtener la ruta correcta de la imagen del alien
        imagen_path = resource_path("src/imagenes/alien.bmp")
        
        # Carga la imagen del alien y establece su atributo rect
        self.image = pygame.image.load(imagen_path)
        self.rect = self.image.get_rect()

        # Inicia cada nuevo alien cerca de la parte superior izquierda de la pantalla
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Almacena la posición exacta del alien
        self.x = float(self.rect.x)

    def blitme(self):
        """Dibuja el alien en su ubicación actual"""
        self.pantalla.blit(self.image, self.rect)

    def check_edges(self):
        """Devuelve verdadero si el alien esta en el borde de la pantalla"""
        screen_rect = self.pantalla.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """Mueve el alien a la derecha"""
        self.x += (self.ai_configuracion.alien_speed_factor *
                   self.ai_configuracion.fleet_direction)
        self.rect.x = self.x
