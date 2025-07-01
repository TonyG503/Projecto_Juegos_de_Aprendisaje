import pygame
import sys
import os
import Balones, Teclado_Mecanografia, Figuras_flotantes, Contador, balloon_pop

pygame.init()

# Configuración de ventana
ANCHO, ALTO = 900, 900
screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Menú Principal")
fuente = pygame.font.SysFont(None, 40)
COLOR_FONDO = (230, 230, 230)
COLOR_TEXTO = (20, 20, 20)
MARGEN = 40
CUADRO_ANCHO = 150
CUADRO_ALTO = 150

# Juegos configurables (hasta 4)
juegos = [
    {"nombre": "Balls", "imagen": "balls.png", "activo": True},
    {"nombre": "Teclado", "imagen": "teclado.png", "activo": True},
    {"nombre": "Formas", "imagen": "formas.png", "activo": True},
    {"nombre": "Contar", "imagen": "cuentas.png", "activo": True},
    {"nombre": "Ballon pop", "imagen": "rebienta_globos.png", "activo": True},
    {"nombre": "", "imagen": "", "activo": False}
]

# Cargar imágenes y definir posiciones
def cargar_imagen(path):
    if os.path.isfile(path):
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, (CUADRO_ANCHO, CUADRO_ALTO))
    return None

imagenes = []
posiciones = []

for i, juego in enumerate(juegos):
    fila = i // 2
    col = i % 2
    x = MARGEN + col * (CUADRO_ANCHO + 2 * MARGEN)
    y = MARGEN + fila * (CUADRO_ALTO + 80)
    posiciones.append(pygame.Rect(x, y, CUADRO_ANCHO, CUADRO_ALTO))
    imagen = cargar_imagen(juego["imagen"]) if juego["activo"] else None
    imagenes.append(imagen)

# Dibujar menú visual
def dibujar_menu():
    screen.fill(COLOR_FONDO)
    for i, juego in enumerate(juegos):
        if not juego["activo"]:
            continue
        rect = posiciones[i]
        img = imagenes[i]
        if img:
            screen.blit(img, rect.topleft)
        texto = fuente.render(juego["nombre"], True, COLOR_TEXTO)
        screen.blit(texto, (rect.x + CUADRO_ANCHO // 2 - texto.get_width() // 2, rect.bottom + 5))
    pygame.display.flip()

# Funciones ficticias para lanzar juegos (reemplazar luego)
def juego_balls():
    Balones.iniciar_juego()

def juego_teclado():
    Teclado_Mecanografia.iniciar_juego()

def juego_Figuras():
    Figuras_flotantes.iniciar_juego()

def juego_Contar():
    Contador.iniciar_juego()

def juego_BallonPop():
    balloon_pop.draw_background()

# Mapeo de funciones por índice
funciones_juego = {
    0: juego_balls,
    1: juego_teclado,
    2: juego_Figuras,
    3: juego_Contar,
    4: juego_BallonPop
}

# Bucle principal del menú
while True:
    dibujar_menu()

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif evento.type == pygame.MOUSEBUTTONDOWN:
            pos_click = evento.pos
            for i, rect in enumerate(posiciones):
                if rect.collidepoint(pos_click) and juegos[i]["activo"]:
                    if i in funciones_juego:
                        funciones_juego[i]()  # Ejecuta el juego correspondiente
