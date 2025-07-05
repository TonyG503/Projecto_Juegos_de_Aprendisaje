import pygame
import random
import sys

def iniciar_juego():
    pygame.init()

    # Obtener el tamaño actual de la ventana del menú
    info = pygame.display.Info()
    current_surface = pygame.display.get_surface()
    if current_surface:
        ANCHO, ALTO = current_surface.get_size()
    else:
        ANCHO, ALTO = 1200, 800

    # Configuración de ventana escalable
    ANCHO_MIN, ALTO_MIN = 800, 600
    screen = pygame.display.set_mode((ANCHO, ALTO), pygame.RESIZABLE)
    pygame.display.set_caption("Juego de Mecanografía")
    
    # Cargar imágenes del corazón (con manejo de errores)
    try:
        corazon_lleno_orig = pygame.image.load("IMAGENES/Corazon.png").convert_alpha()
        corazon_vacio_orig = pygame.image.load("IMAGENES/Corazon_Vacio.png").convert_alpha()
    except pygame.error:
        # Crear corazones simples si no se encuentran las imágenes
        corazon_lleno_orig = pygame.Surface((32, 32), pygame.SRCALPHA)
        corazon_vacio_orig = pygame.Surface((32, 32), pygame.SRCALPHA)
        pygame.draw.polygon(corazon_lleno_orig, (255, 0, 0), [(16, 5), (25, 12), (30, 20), (16, 30), (2, 20), (7, 12)])
        pygame.draw.polygon(corazon_vacio_orig, (100, 100, 100), [(16, 5), (25, 12), (30, 20), (16, 30), (2, 20), (7, 12)], 2)

    # Colores modernos
    COLOR_FONDO = (25, 30, 45)
    COLOR_CORRECTO = (46, 204, 113)
    COLOR_INCORRECTO = (231, 76, 60)
    COLOR_TEXTO = (255, 255, 255)
    COLOR_BOTON = (52, 73, 94)
    COLOR_BOTON_HOVER = (74, 94, 114)
    COLOR_SECUNDARIO = (149, 165, 166)

    # Variables de juego
    letras = [chr(i) for i in range(65, 91)] + [chr(i) for i in range(97, 123)]  # A-Z y a-z
    letra_actual = random.choice(letras)
    color_actual = COLOR_TEXTO
    aciertos = 0
    fallos = 0
    total_para_ganar = 10
    vidas_max = 3

    def calcular_tamaños(ancho, alto):
        """Calcula los tamaños de fuente y elementos según el tamaño de ventana"""
        # Tamaños de fuente escalables
        fuente_letra_size = max(80, min(200, ancho // 6))
        fuente_texto_size = max(24, min(48, ancho // 25))
        fuente_boton_size = max(20, min(36, ancho // 30))
        
        # Tamaño de corazones
        corazon_size = max(24, min(48, ancho // 30))
        
        return fuente_letra_size, fuente_texto_size, fuente_boton_size, corazon_size

    def crear_fuentes(ancho, alto):
        """Crea las fuentes con tamaños apropiados"""
        fuente_letra_size, fuente_texto_size, fuente_boton_size, corazon_size = calcular_tamaños(ancho, alto)
        
        fuente_grande = pygame.font.SysFont("Arial", fuente_letra_size, bold=True)
        fuente_pequena = pygame.font.SysFont("Arial", fuente_texto_size, bold=True)
        fuente_boton = pygame.font.SysFont("Arial", fuente_boton_size, bold=True)
        
        return fuente_grande, fuente_pequena, fuente_boton, corazon_size

    def escalar_corazones(size):
        """Escala los corazones al tamaño apropiado"""
        corazon_lleno = pygame.transform.smoothscale(corazon_lleno_orig, (size, size))
        corazon_vacio = pygame.transform.smoothscale(corazon_vacio_orig, (size, size))
        return corazon_lleno, corazon_vacio

    def dibujar_gradiente(surface, color_top, color_bottom, rect):
        """Dibuja un gradiente vertical"""
        for y in range(rect.height):
            ratio = y / rect.height
            r = int(color_top[0] * (1 - ratio) + color_bottom[0] * ratio)
            g = int(color_top[1] * (1 - ratio) + color_bottom[1] * ratio)
            b = int(color_top[2] * (1 - ratio) + color_bottom[2] * ratio)
            pygame.draw.line(surface, (r, g, b), 
                           (rect.x, rect.y + y), (rect.x + rect.width, rect.y + y))

    def mostrar_letra(letra, color, ancho, alto):
        # Crear fuentes y elementos según el tamaño actual
        fuente_grande, fuente_pequena, fuente_boton, corazon_size = crear_fuentes(ancho, alto)
        corazon_lleno, corazon_vacio = escalar_corazones(corazon_size)
        
        # Fondo con gradiente
        color_fondo_top = (35, 40, 55)
        color_fondo_bottom = (25, 30, 45)
        dibujar_gradiente(screen, color_fondo_top, color_fondo_bottom, pygame.Rect(0, 0, ancho, alto))
        
        # Título del juego
        titulo = fuente_pequena.render("Juego de Mecanografía", True, COLOR_TEXTO)
        titulo_rect = titulo.get_rect(center=(ancho // 2, 50))
        screen.blit(titulo, titulo_rect)

        # Letra principal (centrada)
        texto_letra = fuente_grande.render(letra, True, color)
        letra_rect = texto_letra.get_rect(center=(ancho // 2, alto // 2))
        
        # Sombra para la letra
        sombra = fuente_grande.render(letra, True, (0, 0, 0, 50))
        sombra_rect = sombra.get_rect(center=(ancho // 2 + 3, alto // 2 + 3))
        screen.blit(sombra, sombra_rect)
        screen.blit(texto_letra, letra_rect)

        # Panel de información superior
        panel_info_height = 80
        panel_rect = pygame.Rect(20, 90, ancho - 40, panel_info_height)
        pygame.draw.rect(screen, (40, 45, 60, 180), panel_rect, border_radius=10)
        pygame.draw.rect(screen, COLOR_SECUNDARIO, panel_rect, 2, border_radius=10)

        # Progreso
        progreso_texto = fuente_pequena.render(f"Progreso: {aciertos}/{total_para_ganar}", True, COLOR_TEXTO)
        screen.blit(progreso_texto, (40, 110))

        # Barra de progreso
        barra_ancho = 200
        barra_alto = 20
        barra_x = 40
        barra_y = 140
        
        # Fondo de la barra
        pygame.draw.rect(screen, (60, 60, 60), (barra_x, barra_y, barra_ancho, barra_alto), border_radius=10)
        
        # Progreso actual
        progreso_actual = (aciertos / total_para_ganar) * barra_ancho
        if progreso_actual > 0:
            pygame.draw.rect(screen, COLOR_CORRECTO, (barra_x, barra_y, progreso_actual, barra_alto), border_radius=10)

        # Corazones (alineados a la derecha)
        corazones_start_x = ancho - 40 - (vidas_max * (corazon_size + 10))
        for i in range(vidas_max):
            img = corazon_lleno if i < (vidas_max - fallos) else corazon_vacio
            x = corazones_start_x + i * (corazon_size + 10)
            y = 110
            screen.blit(img, (x, y))

        # Botón de volver al menú (en la parte inferior)
        mouse = pygame.mouse.get_pos()
        boton_ancho = min(200, ancho // 4)
        boton_alto = 50
        boton_x = (ancho - boton_ancho) // 2
        boton_y = alto - boton_alto - 30
        
        boton_rect = pygame.Rect(boton_x, boton_y, boton_ancho, boton_alto)
        color_boton = COLOR_BOTON_HOVER if boton_rect.collidepoint(mouse) else COLOR_BOTON
        
        # Sombra del botón
        sombra_rect = pygame.Rect(boton_x + 2, boton_y + 2, boton_ancho, boton_alto)
        pygame.draw.rect(screen, (0, 0, 0, 50), sombra_rect, border_radius=10)
        
        # Botón principal
        pygame.draw.rect(screen, color_boton, boton_rect, border_radius=10)
        pygame.draw.rect(screen, COLOR_SECUNDARIO, boton_rect, 2, border_radius=10)
        
        texto_boton = fuente_boton.render("Volver al Menú", True, COLOR_TEXTO)
        texto_rect = texto_boton.get_rect(center=boton_rect.center)
        screen.blit(texto_boton, texto_rect)

        # Instrucciones
        instrucciones = fuente_boton.render("Presiona la tecla que aparece en pantalla", True, COLOR_SECUNDARIO)
        instr_rect = instrucciones.get_rect(center=(ancho // 2, alto - 120))
        screen.blit(instrucciones, instr_rect)

        pygame.display.flip()
        return boton_rect

    def mostrar_mensaje_final(mensaje, color, ancho, alto):
        """Muestra mensaje de victoria o derrota"""
        fuente_grande, fuente_pequena, fuente_boton, _ = crear_fuentes(ancho, alto)
        
        # Overlay semitransparente
        overlay = pygame.Surface((ancho, alto), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))
        
        # Panel central
        panel_ancho = min(400, ancho - 100)
        panel_alto = min(200, alto - 100)
        panel_x = (ancho - panel_ancho) // 2
        panel_y = (alto - panel_alto) // 2
        
        panel_rect = pygame.Rect(panel_x, panel_y, panel_ancho, panel_alto)
        pygame.draw.rect(screen, COLOR_FONDO, panel_rect, border_radius=20)
        pygame.draw.rect(screen, color, panel_rect, 4, border_radius=20)
        
        # Mensaje
        texto = fuente_pequena.render(mensaje, True, color)
        texto_rect = texto.get_rect(center=(ancho // 2, alto // 2))
        screen.blit(texto, texto_rect)
        
        pygame.display.flip()

    # Inicializar variables de pantalla
    fuente_grande, fuente_pequena, fuente_boton, corazon_size = crear_fuentes(ANCHO, ALTO)
    boton_rect = mostrar_letra(letra_actual, color_actual, ANCHO, ALTO)
    
    reloj = pygame.time.Clock()
    esperar = 0
    running = True

    while running:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                running = False
                return (ANCHO, ALTO)  # Retorna el tamaño actual

            if evento.type == pygame.VIDEORESIZE:
                ANCHO = max(evento.w, ANCHO_MIN)
                ALTO = max(evento.h, ALTO_MIN)
                screen = pygame.display.set_mode((ANCHO, ALTO), pygame.RESIZABLE)
                boton_rect = mostrar_letra(letra_actual, color_actual, ANCHO, ALTO)

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_rect.collidepoint(evento.pos):
                    running = False
                    return (ANCHO, ALTO)  # Retorna el tamaño actual

            if evento.type == pygame.KEYDOWN and esperar == 0:
                # Ignorar teclas especiales
                if evento.key in [
                    pygame.K_LSHIFT, pygame.K_RSHIFT, pygame.K_CAPSLOCK,
                    pygame.K_LCTRL, pygame.K_RCTRL, pygame.K_LALT, pygame.K_RALT,
                    pygame.K_TAB, pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_SPACE]:
                    continue

                tecla = evento.unicode

                if tecla == letra_actual:
                    color_actual = COLOR_CORRECTO
                    aciertos += 1
                    if aciertos >= total_para_ganar:
                        mostrar_mensaje_final("¡Excelente! ¡Completaste el nivel!", COLOR_CORRECTO, ANCHO, ALTO)
                        pygame.time.wait(2000)
                        aciertos = 0
                        fallos = 0
                        color_actual = COLOR_TEXTO
                    letra_actual = random.choice(letras)
                else:
                    color_actual = COLOR_INCORRECTO
                    fallos += 1
                    if fallos >= vidas_max:
                        mostrar_mensaje_final("¡Perdiste! Inténtalo de nuevo", COLOR_INCORRECTO, ANCHO, ALTO)
                        pygame.time.wait(2000)
                        aciertos = 0
                        fallos = 0
                        color_actual = COLOR_TEXTO
                    letra_actual = random.choice(letras)

                boton_rect = mostrar_letra(letra_actual, color_actual, ANCHO, ALTO)
                esperar = 30  # Frames de espera

        if esperar > 0:
            esperar -= 1
            if esperar == 0:
                color_actual = COLOR_TEXTO
                boton_rect = mostrar_letra(letra_actual, color_actual, ANCHO, ALTO)

        reloj.tick(60)
    
    return (ANCHO, ALTO)  # Retorna el tamaño actual