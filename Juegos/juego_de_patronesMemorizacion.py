import pygame
import random
import sys

# 1. Inicialización de Pygame
pygame.init()

# 2. Configuración de la Pantalla
ANCHO, ALTO = 800, 600
PANTALLA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego de Memoria - Simón Dice")

# 3. Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
AMARILLO = (255, 255, 0)

# Colores y posiciones de los botones
COLORES_BOTONES = {
    "rojo": (ROJO, pygame.Rect(ANCHO // 4 - 50, ALTO // 2 - 150, 100, 100)),
    "verde": (VERDE, pygame.Rect(ANCHO // 2 - 50, ALTO // 2 - 150, 100, 100)),
    "azul": (AZUL, pygame.Rect(ANCHO // 4 * 3 - 50, ALTO // 2 - 150, 100, 100)),
    "amarillo": (AMARILLO, pygame.Rect(ANCHO // 2 - 50, ALTO // 2 - 50, 100, 100))
}

# 4. Variables del Juego
patron_actual = []
indice_jugador = 0
modo_juego = "inicio"  # "inicio", "countdown", "simon_turno_mostrando", "jugador_turno", "fin_juego"
juego_activo = True
nivel = 1

# 5. Fuente (para texto)
FUENTE = pygame.font.Font(None, 74)
FUENTE_GRANDE = pygame.font.Font(None, 200)

# 6. Funciones del Juego
def generar_nuevo_patron():
    colores = list(COLORES_BOTONES.keys())
    patron_actual.append(random.choice(colores))

def mostrar_patron():
    global modo_juego, indice_jugador
    modo_juego = "simon_turno_mostrando"
    pygame.time.wait(500)

    dibujar_botones()
    pygame.display.flip()

    for color_nombre in patron_actual:
        color_original, rect = COLORES_BOTONES.get(color_nombre)

        # Iluminar el botón
        pygame.draw.rect(PANTALLA, BLANCO, rect)
        pygame.display.flip()
        pygame.time.wait(500)

        # Volver a su color original
        pygame.draw.rect(PANTALLA, color_original, rect)
        pygame.display.flip()
        pygame.time.wait(250)

    modo_juego = "jugador_turno"
    indice_jugador = 0

def dibujar_botones():
    for color_nombre, (color_rgb, rect) in COLORES_BOTONES.items():
        pygame.draw.rect(PANTALLA, color_rgb, rect)

def dibujar_pantalla_inicio():
    PANTALLA.fill(NEGRO)
    texto_titulo = FUENTE.render("Simón Dice", True, BLANCO)
    texto_inicio = FUENTE.render("Presiona ESPACIO para iniciar", True, BLANCO)
    PANTALLA.blit(texto_titulo, (ANCHO // 2 - texto_titulo.get_width() // 2, ALTO // 2 - 100))
    PANTALLA.blit(texto_inicio, (ANCHO // 2 - texto_inicio.get_width() // 2, ALTO // 2 + 20))
    pygame.display.flip()

def dibujar_pantalla_fin():
    PANTALLA.fill(NEGRO)
    texto_fin = FUENTE.render("¡Game Over!", True, ROJO)
    texto_nivel = FUENTE.render(f"Nivel Alcanzado: {nivel}", True, BLANCO)
    PANTALLA.blit(texto_fin, (ANCHO // 2 - texto_fin.get_width() // 2, ALTO // 2 - 50))
    PANTALLA.blit(texto_nivel, (ANCHO // 2 - texto_nivel.get_width() // 2, ALTO // 2 + 20))
    pygame.display.flip()

def ejecutar_cuenta_regresiva():
    global modo_juego

    for i in range(3, 0, -1):
        PANTALLA.fill(NEGRO)
        dibujar_botones()
        texto_cuenta = FUENTE_GRANDE.render(str(i), True, BLANCO)
        PANTALLA.blit(texto_cuenta, (ANCHO // 2 - texto_cuenta.get_width() // 2, ALTO // 2 - texto_cuenta.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(1000)

    generar_nuevo_patron()
    mostrar_patron()

# 7. Bucle Principal del Juego
def main_game_loop():
    global modo_juego, indice_jugador, juego_activo, nivel, patron_actual

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and modo_juego == "inicio":
                    juego_activo = True
                    patron_actual = []
                    nivel = 1
                    modo_juego = "countdown"

            if juego_activo and evento.type == pygame.MOUSEBUTTONDOWN and modo_juego == "jugador_turno":
                mouse_pos = evento.pos
                for color_nombre, (color_rgb, rect) in COLORES_BOTONES.items():
                    if rect.collidepoint(mouse_pos):
                        if color_nombre == patron_actual[indice_jugador]:
                            indice_jugador += 1
                            if indice_jugador == len(patron_actual):
                                nivel += 1
                                pygame.time.wait(500)
                                modo_juego = "countdown"
                        else:
                            juego_activo = False
                            modo_juego = "fin_juego"

        # Dibujar pantalla
        PANTALLA.fill(NEGRO)
        dibujar_botones()

        if modo_juego == "inicio":
            dibujar_pantalla_inicio()
        elif modo_juego == "countdown":
            ejecutar_cuenta_regresiva()
        elif modo_juego == "fin_juego":
            dibujar_pantalla_fin()
        elif juego_activo:
            texto_nivel = FUENTE.render(f"Nivel: {nivel}", True, BLANCO)
            PANTALLA.blit(texto_nivel, (10, 10))

        pygame.display.flip()

if __name__ == "__main__":
    main_game_loop()
