import pygame
import random
import sys

def iniciar_juego():
    pygame.init()

    # Configuración
    ANCHO, ALTO = 800, 600
    screen = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Juego del Teclado")
    fuente_grande = pygame.font.SysFont(None, 140)
    fuente_pequena = pygame.font.SysFont(None, 48)
    fuente_vida = pygame.font.SysFont(None, 40)

    # Cargar imágenes del corazón y redimensionarlas
    corazon_lleno = pygame.transform.scale(
        pygame.image.load("Corazon.png").convert_alpha(), (32, 32))
    corazon_vacio = pygame.transform.scale(
        pygame.image.load("Corazon_Vacio.png").convert_alpha(), (32, 32))

    # Colores
    COLOR_FONDO = (30, 30, 30)
    COLOR_CORRECTO = (0, 200, 0)
    COLOR_INCORRECTO = (200, 0, 0)
    COLOR_TEXTO = (255, 255, 255)
    COLOR_BOTON = (100, 100, 100)
    COLOR_BOTON_HOVER = (150, 150, 150)

    # Variables de juego
    letras = [chr(i) for i in range(65, 91)] + [chr(i) for i in range(97, 123)]  # A-Z y a-z
    letra_actual = random.choice(letras)
    color_actual = COLOR_TEXTO
    aciertos = 0
    fallos = 0
    total_para_ganar = 5
    vidas_max = 3

    def mostrar_letra(letra, color):
        screen.fill(COLOR_FONDO)

        # Letra
        texto = fuente_grande.render(letra, True, color)
        screen.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 2 - texto.get_height() // 2))

        # Aciertos
        texto_pequeno = fuente_pequena.render(f"Aciertos: {aciertos}/{total_para_ganar}", True, COLOR_TEXTO)
        screen.blit(texto_pequeno, (10, 10))

        # Corazones
        for i in range(vidas_max):
            img = corazon_lleno if i < (vidas_max - fallos) else corazon_vacio
            x = ANCHO - (vidas_max - i) * (32 + 10)
            y = 10
            screen.blit(img, (x, y))

        # Botón de volver al menú
        mouse = pygame.mouse.get_pos()
        boton_rect = pygame.Rect(10, 60, 180, 40)
        color_boton = COLOR_BOTON_HOVER if boton_rect.collidepoint(mouse) else COLOR_BOTON
        pygame.draw.rect(screen, color_boton, boton_rect)
        texto_boton = fuente_pequena.render("Volver al menú", True, COLOR_TEXTO)
        screen.blit(texto_boton, (20, 65))

        pygame.display.flip()

    reloj = pygame.time.Clock()
    mostrar_letra(letra_actual, color_actual)
    esperar = 0

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return  # Regresa al menú

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if pygame.Rect(10, 60, 180, 40).collidepoint(evento.pos):
                    return  # Botón "Volver al menú"

            if evento.type == pygame.KEYDOWN and esperar == 0:
                if evento.key in [
                    pygame.K_LSHIFT, pygame.K_RSHIFT, pygame.K_CAPSLOCK,
                    pygame.K_LCTRL, pygame.K_RCTRL, pygame.K_LALT, pygame.K_RALT,
                    pygame.K_TAB, pygame.K_ESCAPE, pygame.K_RETURN]:
                    continue

                tecla = evento.unicode

                if tecla == letra_actual:
                    color_actual = COLOR_CORRECTO
                    aciertos += 1
                    if aciertos >= total_para_ganar:
                        screen.fill(COLOR_FONDO)
                        texto = fuente_pequena.render("¡Muy bien!", True, COLOR_CORRECTO)
                        screen.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 2 - texto.get_height() // 2))
                        pygame.display.flip()
                        pygame.time.wait(2000)
                        aciertos = 0
                        fallos = 0
                    letra_actual = random.choice(letras)
                else:
                    color_actual = COLOR_INCORRECTO
                    fallos += 1
                    if fallos >= vidas_max:
                        screen.fill(COLOR_FONDO)
                        texto = fuente_pequena.render("¡Perdiste!", True, COLOR_INCORRECTO)
                        screen.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 2 - texto.get_height() // 2))
                        pygame.display.flip()
                        pygame.time.wait(2000)
                        aciertos = 0
                        fallos = 0
                    letra_actual = random.choice(letras)

                mostrar_letra(letra_actual, color_actual)
                esperar = 20

        if esperar > 0:
            esperar -= 1
            if esperar == 0:
                color_actual = COLOR_TEXTO
                mostrar_letra(letra_actual, color_actual)

        reloj.tick(60)
