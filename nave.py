import pygame
from pygame.sprite import Sprite


class Nave(Sprite):
    """Sirve para gestionar el comportamiento de la nave"""

    def __init__(self, ai_configuracion, pantalla):
        """inicializa la nave y establece su posición de partida"""
        super(Nave, self).__init__()
        self.pantalla = pantalla
        self.ai_configuracion = ai_configuracion

        # Carga la imagen de la nave y obtiene su rect(rectángulo)
        self.image = pygame.image.load("./imagenes/F16.png")
        self.rect = self.image.get_rect()
        self.pantalla_rect = pantalla.get_rect()

        # Empieza cada nueva nave en la parte inferior central de la pantalla
        self.rect.centerx = self.pantalla_rect.centerx
        self.rect.bottom = self.pantalla_rect.bottom

        # Almacena un valor decimal para el centro de la nave
        self.center = float(self.rect.centerx)

        # Banderas de movimiento
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Actualiza la posición de la nave según las banderas de movimiento"""
        if self.moving_right and self.rect.right < self.pantalla_rect.right:
            self.center += self.ai_configuracion.factor_velocidad_nave

        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_configuracion.factor_velocidad_nave

        # Actualiza el objeto  rect desde self.center
        self.rect.centerx = self.center

    def blitme(self):
        """Dibuja la nave en su ubicación actual"""
        self.pantalla.blit(self.image, self.rect)

    def centrar_nave(self):
        """Centra la nave en la pantalla"""
        self.center = self.pantalla_rect.centerx
