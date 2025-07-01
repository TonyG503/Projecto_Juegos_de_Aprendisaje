# Importa las librerías necesarias
import pygame
import random

# Inicializa Pygame
pygame.init()

# Define colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
FONDO = (30, 40, 50)  # Fondo moderno

# Define dimensiones de la pantalla
ANCHO_PANTALLA = 600
ALTO_PANTALLA = 400
pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption("Serpiente Alfabetica")

# Define tamaño de la serpiente y la comida
TAMANO_SERPIENTE = 20
TAMANO_COMIDA = 20

# Fuente para el texto
fuente = pygame.font.SysFont(None, 28)

# Reloj para controlar la velocidad del juego
reloj = pygame.time.Clock()

# Clase para la serpiente
class Serpiente(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.tamano = TAMANO_SERPIENTE
        self.imagen = pygame.Surface((self.tamano, self.tamano))
        self.imagen.fill(VERDE)
        self.rect = self.imagen.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direccion = 0  # 0: derecha, 1: arriba, 2: izquierda, 3: abajo
        self.cuerpo = []

    def mover(self):
        nuevo_cabezal = [self.rect.x, self.rect.y]
        self.cuerpo.append(nuevo_cabezal)
        if len(self.cuerpo) > 1:
            self.cuerpo.pop(0)
        
        if self.direccion == 0:
            self.rect.x += TAMANO_SERPIENTE
        elif self.direccion == 1:
            self.rect.y -= TAMANO_SERPIENTE
        elif self.direccion == 2:
            self.rect.x -= TAMANO_SERPIENTE
        elif self.direccion == 3:
            self.rect.y += TAMANO_SERPIENTE
        
    def cambiar_direccion(self, direccion):
        if direccion == 0 and self.direccion != 2:
            self.direccion = 0
        elif direccion == 1 and self.direccion != 3:
            self.direccion = 1
        elif direccion == 2 and self.direccion != 0:
            self.direccion = 2
        elif direccion == 3 and self.direccion != 1:
            self.direccion = 3

# Clase para la comida
class Comida(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.tamano = TAMANO_COMIDA
        self.imagen = pygame.Surface((self.tamano, self.tamano))
        self.imagen.fill(ROJO)
        self.rect = self.imagen.get_rect()
        self.generar_posicion()

    def generar_posicion(self):
        self.rect.x = random.randrange(0, ANCHO_PANTALLA - TAMANO_COMIDA, TAMANO_SERPIENTE)
        self.rect.y = random.randrange(0, ALTO_PANTALLA - TAMANO_COMIDA, TAMANO_SERPIENTE)

# Función para mostrar el texto en la pantalla
def mostrar_texto(superficie, texto, color, x, y):
    texto_superficie = fuente.render(texto, True, color)
    texto_rect = texto_superficie.get_rect(center=(x, y))
    superficie.blit(texto_superficie, texto_rect)

# Inicializa la serpiente y la comida
serpiente = Serpiente(ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2)
comida = Comida()

# Grupo de sprites
todos_los_sprites = pygame.sprite.Group()
todos_los_sprites.add(serpiente)
todos_los_sprites.add(comida)

# Bucle principal del juego
ejecutando = True
while ejecutando:
    # Maneja los eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_RIGHT:
                serpiente.cambiar_direccion(0)
            if evento.key == pygame.K_UP:
                serpiente.cambiar_direccion(1)
            if evento.key == pygame.K_LEFT:
                serpiente.cambiar_direccion(2)
            if evento.key == pygame.K_DOWN:
                serpiente.cambiar_direccion(3)

    # Actualiza la serpiente
    serpiente.mover()

    # Verifica si la serpiente come la comida
    if serpiente.rect.x == comida.rect.x and serpiente.rect.y == comida.rect.y:
        comida.generar_posicion()
        # Aqui es donde agregarías el sonido de la mordida a la manzana

    # Verifica si la serpiente se sale de la pantalla
    if serpiente.rect.x < 0 or serpiente.rect.x > ANCHO_PANTALLA - TAMANO_SERPIENTE or \
       serpiente.rect.y < 0 or serpiente.rect.y > ALTO_PANTALLA - TAMANO_SERPIENTE:
        mostrar_texto(pantalla, "GAME OVER", ROJO, ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2)
        pygame.display.flip()
        pygame.time.wait(2000)
        ejecutando = False

    # Verifica si la serpiente se golpea a sí misma
    for segmento in serpiente.cuerpo[:-1]:
        if serpiente.rect.x == segmento[0] and serpiente.rect.y == segmento[1]:
            mostrar_texto(pantalla, "GAME OVER", ROJO, ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2)
            pygame.display.flip()
            pygame.time.wait(2000)
            ejecutando = False

    # Dibuja la pantalla
    pantalla.fill(FONDO)
    todos_los_sprites.draw(pantalla)
    mostrar_texto(pantalla, "Controles: Flechas", BLANCO, ANCHO_PANTALLA // 2, 20) # Instrucciones
    pygame.display.flip()

    # Controla la velocidad del juego
    reloj.tick(10)

# Sale de Pygame
pygame.quit()