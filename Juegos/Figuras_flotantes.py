import pygame
import random
import math

def iniciar_juego():
    pygame.init()
    ANCHO, ALTO = 800, 600
    screen = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Arrastrar Formas - Versión Mejorada")
    fuente = pygame.font.SysFont(None, 48)
    fuente_chica = pygame.font.SysFont(None, 32)

    # Paleta de colores mejorada
    COLOR_FONDO = (245, 248, 252)
    COLOR_SOMBRA = (180, 190, 200)
    COLOR_SOMBRA_HOVER = (160, 170, 180)
    COLORES = [
        (255, 65, 54),    # Rojo coral
        (46, 204, 113),   # Verde esmeralda
        (52, 152, 219),   # Azul cielo
        (155, 89, 182),   # Púrpura
        (241, 196, 15),   # Amarillo dorado
        (26, 188, 156),   # Turquesa
        (230, 126, 34),   # Naranja
        (52, 73, 94)      # Azul oscuro
    ]

    figuras_disponibles = ["circulo", "cuadrado", "triangulo", "rectangulo", "estrella", "rombo", "gota", "media_luna"]
    nivel = 1

    class Figura:
        def __init__(self, tipo, color, pos, size):
            self.tipo = tipo
            self.color = color
            self.pos = list(pos)
            self.size = size
            self.dragging = False
            self.correcta = False
            self.hover = False
            self.escala_anim = 1.0
            self.rotacion = 0

        def draw(self):
            x, y = self.pos[0], self.pos[1]
            s = int(self.size * self.escala_anim)
            
            # Efecto de hover
            color_actual = self.color
            if self.hover and not self.correcta:
                # Hacer el color un poco más brillante
                color_actual = tuple(min(255, c + 30) for c in self.color)
            
            if self.tipo == "circulo":
                pygame.draw.circle(screen, color_actual, (int(x), int(y)), s)
                # Borde sutil
                pygame.draw.circle(screen, tuple(max(0, c - 40) for c in color_actual), (int(x), int(y)), s, 2)
                
            elif self.tipo == "cuadrado":
                rect = pygame.Rect(x - s, y - s, s * 2, s * 2)
                pygame.draw.rect(screen, color_actual, rect)
                pygame.draw.rect(screen, tuple(max(0, c - 40) for c in color_actual), rect, 2)
                
            elif self.tipo == "triangulo":
                puntos = [(x, y - s), (x - s, y + s), (x + s, y + s)]
                pygame.draw.polygon(screen, color_actual, puntos)
                pygame.draw.polygon(screen, tuple(max(0, c - 40) for c in color_actual), puntos, 2)
                
            elif self.tipo == "rectangulo":
                rect = pygame.Rect(x - s, y - s//2, s * 2, s)
                pygame.draw.rect(screen, color_actual, rect)
                pygame.draw.rect(screen, tuple(max(0, c - 40) for c in color_actual), rect, 2)
                
            elif self.tipo == "estrella":
                puntos = [(x, y - s), (x + s * 0.3, y - s * 0.3), (x + s, y - s * 0.3),
                          (x + s * 0.5, y + s * 0.1), (x + s * 0.6, y + s),
                          (x, y + s * 0.5), (x - s * 0.6, y + s), (x - s * 0.5, y + s * 0.1),
                          (x - s, y - s * 0.3), (x - s * 0.3, y - s * 0.3)]
                pygame.draw.polygon(screen, color_actual, puntos)
                pygame.draw.polygon(screen, tuple(max(0, c - 40) for c in color_actual), puntos, 2)
                
            elif self.tipo == "rombo":
                puntos = [(x, y - s), (x + s, y), (x, y + s), (x - s, y)]
                pygame.draw.polygon(screen, color_actual, puntos)
                pygame.draw.polygon(screen, tuple(max(0, c - 40) for c in color_actual), puntos, 2)
                
            elif self.tipo == "gota":
                puntos = [(x, y - s), (x + s, y), (x, y + s), (x - s, y)]
                pygame.draw.polygon(screen, color_actual, puntos)
                pygame.draw.circle(screen, color_actual, (int(x), int(y - s * 0.5)), int(s * 0.5))
                pygame.draw.polygon(screen, tuple(max(0, c - 40) for c in color_actual), puntos, 2)
                pygame.draw.circle(screen, tuple(max(0, c - 40) for c in color_actual), (int(x), int(y - s * 0.5)), int(s * 0.5), 2)
                
            elif self.tipo == "media_luna":
                pygame.draw.circle(screen, color_actual, (int(x), int(y)), s)
                pygame.draw.circle(screen, COLOR_FONDO, (int(x + s//2), int(y)), s * 3 // 4)
                pygame.draw.circle(screen, tuple(max(0, c - 40) for c in color_actual), (int(x), int(y)), s, 2)

        def draw_sombra(self):
            x, y = self.pos[0], self.pos[1]
            s = self.size
            color_sombra = COLOR_SOMBRA_HOVER if self.hover else COLOR_SOMBRA
            
            # Sombra con patrón de líneas punteadas
            if self.tipo == "circulo":
                for i in range(0, 360, 20):
                    start_angle = math.radians(i)
                    end_angle = math.radians(i + 10)
                    start_pos = (x + s * math.cos(start_angle), y + s * math.sin(start_angle))
                    end_pos = (x + s * math.cos(end_angle), y + s * math.sin(end_angle))
                    pygame.draw.line(screen, color_sombra, start_pos, end_pos, 3)
                    
            elif self.tipo == "cuadrado":
                # Dibujar líneas punteadas para el contorno
                rect = pygame.Rect(x - s, y - s, s * 2, s * 2)
                dash_length = 10
                # Línea superior
                for i in range(rect.left, rect.right, dash_length * 2):
                    pygame.draw.line(screen, color_sombra, (i, rect.top), (min(i + dash_length, rect.right), rect.top), 3)
                # Línea inferior
                for i in range(rect.left, rect.right, dash_length * 2):
                    pygame.draw.line(screen, color_sombra, (i, rect.bottom), (min(i + dash_length, rect.right), rect.bottom), 3)
                # Línea izquierda
                for i in range(rect.top, rect.bottom, dash_length * 2):
                    pygame.draw.line(screen, color_sombra, (rect.left, i), (rect.left, min(i + dash_length, rect.bottom)), 3)
                # Línea derecha
                for i in range(rect.top, rect.bottom, dash_length * 2):
                    pygame.draw.line(screen, color_sombra, (rect.right, i), (rect.right, min(i + dash_length, rect.bottom)), 3)
                    
            else:
                # Para otras formas, usar el método anterior pero más sutil
                old_color = self.color
                self.color = color_sombra
                temp_size = self.size
                self.size = int(self.size * 0.9)  # Hacer la sombra un poco más pequeña
                self.draw()
                self.size = temp_size
                self.color = old_color

        def is_hovered(self, mouse_pos):
            return math.hypot(self.pos[0] - mouse_pos[0], self.pos[1] - mouse_pos[1]) < self.size + 15

        def colisiona_con(self, otra):
            return math.hypot(self.pos[0] - otra.pos[0], self.pos[1] - otra.pos[1]) < self.size * 1.8

        def update_animation(self):
            if self.dragging:
                self.escala_anim = min(1.2, self.escala_anim + 0.05)
            else:
                self.escala_anim = max(1.0, self.escala_anim - 0.05)

    def generar_posiciones_aleatorias(cantidad, zona_top, zona_bottom, size_promedio):
        """Genera posiciones aleatorias sin colisiones"""
        posiciones = []
        intentos = 0
        max_intentos = 1000
        
        while len(posiciones) < cantidad and intentos < max_intentos:
            x = random.randint(size_promedio + 20, ANCHO - size_promedio - 20)
            y = random.randint(zona_top + size_promedio + 20, zona_bottom - size_promedio - 20)
            
            # Verificar que no colisione con posiciones existentes
            valida = True
            for pos_existente in posiciones:
                distancia = math.hypot(x - pos_existente[0], y - pos_existente[1])
                if distancia < (size_promedio * 2.5):  # Margen de separación
                    valida = False
                    break
            
            if valida:
                posiciones.append([x, y])
            
            intentos += 1
        
        return posiciones

    def generar_formas(nivel):
        cantidad = min(3 + nivel - 1, len(figuras_disponibles), 8)  # Limitamos a 8 para mejor experiencia
        seleccion = random.sample(figuras_disponibles, cantidad)
        formas, siluetas = [], []
        
        size_promedio = 35

        # Generar posiciones aleatorias para las siluetas en la zona superior
        posiciones_siluetas = generar_posiciones_aleatorias(cantidad, 50, 350, size_promedio)
        
        # Si no se pudieron generar suficientes posiciones aleatorias, usar distribución regular
        if len(posiciones_siluetas) < cantidad:
            posiciones_siluetas = []
            espacio_total = ANCHO - 100
            separacion = espacio_total // cantidad
            inicio_x = 50 + separacion // 2
            
            for i in range(cantidad):
                x_pos = inicio_x + i * separacion
                y_pos = random.randint(80, 250)
                posiciones_siluetas.append([x_pos, y_pos])

        # Posiciones para las formas (parte inferior, organizadas)
        espacio_total = ANCHO - 100
        separacion = espacio_total // cantidad
        inicio_x = 50 + separacion // 2

        for i, tipo in enumerate(seleccion):
            size = random.randint(30, 40)
            color = random.choice(COLORES)
            
            # Forma arrastrable en la parte inferior
            x_pos = inicio_x + i * separacion
            y_pos = ALTO - 100 + random.randint(-15, 15)  # Pequeña variación vertical
            
            figura = Figura(tipo, color, [x_pos, y_pos], size)
            
            # Silueta en posición aleatoria en la parte superior
            silueta = Figura(tipo, COLOR_SOMBRA, posiciones_siluetas[i], size)
            
            formas.append(figura)
            siluetas.append(silueta)

        return formas, siluetas

    def dibujar_fondo():
        # Fondo con gradiente sutil
        for y in range(ALTO):
            color_r = 245 + int((252 - 245) * y / ALTO)
            color_g = 248 + int((255 - 248) * y / ALTO)
            color_b = 252 + int((255 - 252) * y / ALTO)
            pygame.draw.line(screen, (color_r, color_g, color_b), (0, y), (ANCHO, y))

    def dibujar_botones():
        botones = {
            "reiniciar": pygame.Rect(10, ALTO - 50, 180, 40),
            "menu": pygame.Rect(210, ALTO - 50, 180, 40)
        }
        
        for key, rect in botones.items():
            # Botón con gradiente
            color_base = (70, 130, 180) if key == "reiniciar" else (180, 70, 70)
            pygame.draw.rect(screen, color_base, rect, border_radius=8)
            pygame.draw.rect(screen, tuple(c + 30 for c in color_base), 
                           pygame.Rect(rect.x, rect.y, rect.width, rect.height//2), border_radius=8)
            pygame.draw.rect(screen, (255, 255, 255), rect, 2, border_radius=8)
            
            texto = fuente_chica.render("Reiniciar Nivel" if key == "reiniciar" else "Volver al Menú", True, (255, 255, 255))
            screen.blit(texto, (rect.x + 10, rect.y + 10))
        
        return botones

    def dibujar_flecha():
        # Flecha más elegante
        base_color = (46, 204, 113)
        puntos = [(730, 280), (760, 300), (730, 320), (730, 310), (700, 310), (700, 290), (730, 290)]
        pygame.draw.polygon(screen, base_color, puntos)
        pygame.draw.polygon(screen, (255, 255, 255), puntos, 2)
        
        texto = fuente_chica.render("Siguiente", True, (46, 204, 113))
        screen.blit(texto, (675, 325))
        return pygame.Rect(700, 280, 60, 40)

    def dibujar_nivel(nivel):
        texto_nivel = fuente.render(f"Nivel {nivel}", True, (52, 73, 94))
        screen.blit(texto_nivel, (20, 20))

    def dibujar_particulas_exito():
        # Efecto de partículas cuando se completa el nivel
        for i in range(20):
            x = random.randint(0, ANCHO)
            y = random.randint(0, ALTO//2)
            size = random.randint(2, 6)
            color = random.choice(COLORES)
            pygame.draw.circle(screen, color, (x, y), size)

    formas, siluetas = generar_formas(nivel)
    figura_activa = None
    reloj = pygame.time.Clock()
    mostrar_particulas = False
    tiempo_particulas = 0

    while True:
        dibujar_fondo()
        mouse_pos = pygame.mouse.get_pos()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if flecha_rect and flecha_rect.collidepoint(evento.pos):
                    nivel += 1
                    formas, siluetas = generar_formas(nivel)
                    mostrar_particulas = False
                    continue

                if botones["reiniciar"].collidepoint(evento.pos):
                    formas, siluetas = generar_formas(nivel)
                    mostrar_particulas = False
                    continue
                if botones["menu"].collidepoint(evento.pos):
                    return

                for forma in reversed(formas):
                    if forma.is_hovered(evento.pos) and not forma.correcta:
                        figura_activa = forma
                        figura_activa.dragging = True
                        break

            elif evento.type == pygame.MOUSEBUTTONUP:
                if figura_activa:
                    figura_activa.dragging = False
                    for silueta in siluetas:
                        if figura_activa.tipo == silueta.tipo and not figura_activa.correcta:
                            if figura_activa.colisiona_con(silueta):
                                figura_activa.pos = silueta.pos[:]
                                figura_activa.correcta = True
                                # Activar efecto de partículas si se completa el nivel
                                if all(f.correcta for f in formas):
                                    mostrar_particulas = True
                                    tiempo_particulas = pygame.time.get_ticks()
                    figura_activa = None

            elif evento.type == pygame.MOUSEMOTION and figura_activa:
                figura_activa.pos = list(evento.pos)

        # Actualizar estado de hover
        for forma in formas:
            forma.hover = forma.is_hovered(mouse_pos) and not forma.correcta
            forma.update_animation()

        for silueta in siluetas:
            silueta.hover = any(f.tipo == silueta.tipo and f.colisiona_con(silueta) and not f.correcta for f in formas)

        # Dibujar siluetas
        for silueta in siluetas:
            silueta.draw_sombra()

        # Dibujar formas
        for forma in formas:
            forma.draw()

        # Dibujar UI
        dibujar_nivel(nivel)
        botones = dibujar_botones()
        flecha_rect = None

        # Verificar si se completó el nivel
        if all(f.correcta for f in formas):
            if mostrar_particulas:
                dibujar_particulas_exito()
            
            texto = fuente.render("¡Excelente!", True, (46, 204, 113))
            shadow_texto = fuente.render("¡Excelente!", True, (200, 200, 200))
            screen.blit(shadow_texto, (ANCHO // 2 - texto.get_width() // 2 + 2, ALTO // 2 - 28))
            screen.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 2 - 30))
            flecha_rect = dibujar_flecha()

        pygame.display.flip()
        reloj.tick(60)