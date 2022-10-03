import pygame.font


class Button():
    """Clase para botones"""

    def __init__(self, ai_configuracion, pantalla, msg):
        """Inicializa atributos de botón"""
        self.pantalla = pantalla
        self.pantalla_rect = pantalla.get_rect()

        # Establece las dimensiones y propiedades del botón
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Construye el objeto rect del botón y lo centra
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.pantalla_rect.center

        # El mensaje del botón debe prepararse solo una vez
        self.prep_msg(msg)

    def prep_msg(self, msg):
        """Convierte el msg en una imagen renderizada y centra el texto en  el botón"""
        self.msg_image = self.font.render(
            msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # Dibuja el botón en blanco y luego dibuja el mensaje
        self.pantalla.fill(self.button_color, self.rect)
        self.pantalla.blit(self.msg_image, self.msg_image_rect)
