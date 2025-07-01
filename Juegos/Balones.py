import pygame
import random
import sys
import math

def iniciar_juego():
    pygame.init()
    ANCHO, ALTO = 1000, 700
    screen = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Balls - Juego Educativo Mejorado")
    
    # Fuentes mejoradas
    fuente_grande = pygame.font.SysFont('comicsansms', 52, bold=True)
    fuente = pygame.font.SysFont('comicsansms', 40, bold=True)
    fuente_chica = pygame.font.SysFont('comicsansms', 28)
    fuente_nivel = pygame.font.SysFont('comicsansms', 36, bold=True)

    # Colores mejorados con gradientes y efectos
    COLOR_FONDO = (245, 250, 255)
    COLOR_BANNER = (60, 80, 120)
    COLOR_BOTON = (100, 150, 200)
    COLOR_BOTON_HOVER = (120, 170, 220)
    COLOR_TEXTO = (255, 255, 255)
    COLOR_TEXTO_OSCURO = (40, 40, 60)
    COLOR_SOMBRA = (200, 200, 200)
    
    # Colores más vibrantes y atractivos
    COLORES = [
        ("Rojo", (255, 80, 80)), 
        ("Verde", (80, 200, 80)), 
        ("Azul", (80, 150, 255)),
        ("Amarillo", (255, 220, 60)), 
        ("Morado", (180, 100, 255)), 
        ("Naranja", (255, 160, 60)),
        ("Rosa", (255, 120, 180)),
        ("Cian", (80, 200, 200))
    ]

    RADIO_BOLA = 25
    RADIO_DESTINO = 55
    ALTURA_BANNER = 80
    MARGEN_SEPARACION = 15  # Margen mínimo entre elementos

    nivel = 1
    juego_ganado = False
    particulas = []  # Para efectos visuales

    class Particula:
        def __init__(self, x, y, color):
            self.x = x
            self.y = y
            self.vx = random.uniform(-3, 3)
            self.vy = random.uniform(-5, -1)
            self.color = color
            self.vida = 30
            self.vida_max = 30
            
        def update(self):
            self.x += self.vx
            self.y += self.vy
            self.vy += 0.2  # Gravedad
            self.vida -= 1
            
        def draw(self, screen):
            if self.vida > 0:
                alpha = self.vida / self.vida_max
                size = max(1, int(6 * alpha))
                color_con_alpha = [min(255, int(c * alpha)) for c in self.color[:3]]
                pygame.draw.circle(screen, color_con_alpha, (int(self.x), int(self.y)), size)

    class Bola:
        def __init__(self, color, pos):
            self.color = color
            self.pos = pos
            self.original_pos = pos.copy()
            self.dragging = False
            self.correcta = False
            self.hover = False
            self.bounce_offset = 0
            self.bounce_speed = 0.1

        def draw(self, screen):
            # Efecto de rebote sutil
            if self.hover and not self.dragging:
                self.bounce_offset = math.sin(pygame.time.get_ticks() * 0.01) * 3
            else:
                self.bounce_offset = 0
                
            pos_actual = (self.pos[0], self.pos[1] + self.bounce_offset)
            
            # Sombra
            sombra_pos = (pos_actual[0] + 3, pos_actual[1] + 3)
            pygame.draw.circle(screen, COLOR_SOMBRA, sombra_pos, RADIO_BOLA, 0)
            
            # Bola principal con efecto de brillo
            pygame.draw.circle(screen, self.color, pos_actual, RADIO_BOLA)
            
            # Efecto de brillo
            brillo_pos = (pos_actual[0] - 8, pos_actual[1] - 8)
            brillo_color = tuple(min(255, c + 80) for c in self.color)
            pygame.draw.circle(screen, brillo_color, brillo_pos, RADIO_BOLA // 3)
            
            # Borde si está siendo arrastrada
            if self.dragging:
                pygame.draw.circle(screen, (255, 255, 255), pos_actual, RADIO_BOLA + 2, 3)

        def is_hovered(self, mouse_pos):
            dx = self.pos[0] - mouse_pos[0]
            dy = self.pos[1] - mouse_pos[1]
            return dx ** 2 + dy ** 2 <= RADIO_BOLA ** 2

    def distancia(p1, p2):
        return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

    def verificar_solapamiento(nueva_pos, elementos_existentes, radio_nuevo, radio_existente=None):
        """Verifica si una nueva posición se solapa con elementos existentes"""
        for elemento in elementos_existentes:
            if isinstance(elemento, dict):
                pos_existente = elemento["pos"]
                radio_elem = radio_existente or RADIO_DESTINO
            else:
                pos_existente = elemento.pos
                radio_elem = RADIO_BOLA
                
            distancia_minima = radio_nuevo + radio_elem + MARGEN_SEPARACION
            if distancia(nueva_pos, pos_existente) < distancia_minima:
                return True
        return False

    def generar_posicion_valida(elementos_existentes, radio, area_juego, intentos_max=100):
        """Genera una posición válida que no se solape con elementos existentes"""
        for _ in range(intentos_max):
            nueva_pos = [
                random.randint(area_juego['x_min'], area_juego['x_max']),
                random.randint(area_juego['y_min'], area_juego['y_max'])
            ]
            
            if not verificar_solapamiento(nueva_pos, elementos_existentes, radio):
                return nueva_pos
        
        # Fallback: posición aleatoria si no se encuentra válida
        return [
            random.randint(area_juego['x_min'], area_juego['x_max']),
            random.randint(area_juego['y_min'], area_juego['y_max'])
        ]

    def crear_destinos(colores):
        """Crea destinos sin solapamiento usando el nuevo sistema"""
        destinos = []
        area_destinos = {
            'x_min': RADIO_DESTINO + 20,
            'x_max': ANCHO - RADIO_DESTINO - 20,
            'y_min': ALTO // 2 + 50,
            'y_max': ALTO - ALTURA_BANNER - RADIO_DESTINO - 20
        }
        
        for _, color in colores:
            pos = generar_posicion_valida(destinos, RADIO_DESTINO, area_destinos)
            destinos.append({"color": color, "pos": pos})
            
        return destinos

    def crear_bolas(colores_usados, destinos, num_bolas):
        """Crea bolas sin solapamiento"""
        bolas = []
        area_bolas = {
            'x_min': RADIO_BOLA + 20,
            'x_max': ANCHO - RADIO_BOLA - 20,
            'y_min': 120,
            'y_max': ALTO // 2 - 20
        }
        
        for _ in range(num_bolas):
            color = random.choice(colores_usados)[1]
            # Combinar destinos y bolas existentes para verificar solapamiento
            elementos_existentes = destinos + bolas
            pos = generar_posicion_valida(elementos_existentes, RADIO_BOLA, area_bolas)
            bolas.append(Bola(color, pos))
            
        return bolas

    def nueva_partida(nivel):
        """Crea una nueva partida con mejor distribución de elementos"""
        num_colores = min(3 + (nivel - 1), len(COLORES))
        colores_usados = random.sample(COLORES, num_colores)
        
        # Crear destinos sin solapamiento
        destinos = crear_destinos(colores_usados)
        
        # Calcular número de bolas basado en el nivel
        num_bolas = random.randint(8 + nivel * 2, 12 + nivel * 3)
        
        # Crear bolas sin solapamiento
        bolas = crear_bolas(colores_usados, destinos, num_bolas)
        
        return bolas, destinos, colores_usados

    def agregar_particulas(x, y, color):
        """Agrega partículas para efectos visuales"""
        for _ in range(8):
            particulas.append(Particula(x, y, color))

    def mostrar_mensaje_ganaste():
        # Fondo semi-transparente
        overlay = pygame.Surface((ANCHO, ALTO))
        overlay.set_alpha(100)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Mensaje principal con sombra
        texto_sombra = fuente_grande.render("¡GANASTE!", True, (50, 50, 50))
        texto = fuente_grande.render("¡GANASTE!", True, (100, 255, 100))
        
        x_center = ANCHO // 2
        y_center = ALTO // 2 - 60
        
        screen.blit(texto_sombra, (x_center - texto_sombra.get_width() // 2 + 3, y_center + 3))
        screen.blit(texto, (x_center - texto.get_width() // 2, y_center))

    def dibujar_flecha():
        # Flecha más atractiva con gradiente
        base_color = (100, 200, 100)
        highlight_color = (150, 255, 150)
        
        # Cuerpo de la flecha
        flecha_pts = [(850, 320), (820, 300), (820, 310), (780, 310), (780, 330), (820, 330), (820, 340)]
        pygame.draw.polygon(screen, base_color, flecha_pts)
        pygame.draw.polygon(screen, highlight_color, flecha_pts, 3)
        
        # Texto con mejor estilo
        texto = fuente_chica.render("Siguiente Nivel", True, COLOR_TEXTO_OSCURO)
        screen.blit(texto, (760, 350))

    def clic_en_flecha(pos):
        return 780 <= pos[0] <= 860 and 300 <= pos[1] <= 350

    def dibujar_banner():
        # Banner con gradiente mejorado
        pygame.draw.rect(screen, COLOR_BANNER, (0, ALTO - ALTURA_BANNER, ANCHO, ALTURA_BANNER))
        pygame.draw.rect(screen, (80, 100, 140), (0, ALTO - ALTURA_BANNER, ANCHO, 5))
        
        # Información del nivel
        texto_nivel = fuente_nivel.render(f"Nivel {nivel}", True, COLOR_TEXTO)
        screen.blit(texto_nivel, (20, ALTO - 60))
        
        # Botones mejorados
        botones = [
            {"texto": "Reiniciar Nivel", "x": 200, "ancho": 180, "accion": "reiniciar"},
            {"texto": "Volver al Menú", "x": 400, "ancho": 180, "accion": "menu"}
        ]
        
        for boton in botones:
            rect = pygame.Rect(boton["x"], ALTO - 55, boton["ancho"], 40)
            mouse = pygame.mouse.get_pos()
            color = COLOR_BOTON_HOVER if rect.collidepoint(mouse) else COLOR_BOTON
            
            # Botón con bordes redondeados simulados
            pygame.draw.rect(screen, color, rect, border_radius=8)
            pygame.draw.rect(screen, (255, 255, 255), rect, 2, border_radius=8)
            
            texto = fuente_chica.render(boton["texto"], True, COLOR_TEXTO)
            texto_rect = texto.get_rect(center=rect.center)
            screen.blit(texto, texto_rect)
            
        return botones

    def dibujar_destino(destino):
        """Dibuja un destino con efectos visuales mejorados"""
        pos = destino["pos"]
        color = destino["color"]
        
        # Sombra del destino
        pygame.draw.circle(screen, COLOR_SOMBRA, (pos[0] + 2, pos[1] + 2), RADIO_DESTINO, 8)
        
        # Anillo exterior con gradiente simulado
        for i in range(8, 0, -1):
            alpha = i / 8.0
            color_fade = tuple(int(c * alpha + COLOR_FONDO[j] * (1 - alpha)) for j, c in enumerate(color))
            pygame.draw.circle(screen, color_fade, pos, RADIO_DESTINO, i)
        
        # Círculo interior más claro
        color_claro = tuple(min(255, c + 40) for c in color)
        pygame.draw.circle(screen, color_claro, pos, RADIO_DESTINO - 15, 3)

    # Inicializar juego
    bolas, destinos, colores_usados = nueva_partida(nivel)
    reloj = pygame.time.Clock()
    bola_activa = None

    while True:
        # Degradado de fondo
        for y in range(ALTO):
            color_y = [COLOR_FONDO[i] + int((220 - COLOR_FONDO[i]) * y / ALTO) for i in range(3)]
            pygame.draw.line(screen, color_y, (0, y), (ANCHO, y))

        # Manejo de eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if juego_ganado and clic_en_flecha(evento.pos):
                    nivel += 1
                    bolas, destinos, colores_usados = nueva_partida(nivel)
                    juego_ganado = False
                    particulas.clear()
                    continue

                botones = dibujar_banner()
                for boton in botones:
                    rect = pygame.Rect(boton["x"], ALTO - 55, boton["ancho"], 40)
                    if rect.collidepoint(evento.pos):
                        if boton["accion"] == "reiniciar":
                            bolas, destinos, colores_usados = nueva_partida(nivel)
                            juego_ganado = False
                            particulas.clear()
                        elif boton["accion"] == "menu":
                            pygame.quit()
                            return
                        break

                for bola in reversed(bolas):
                    if bola.is_hovered(evento.pos):
                        bola.dragging = True
                        bola_activa = bola
                        break

            elif evento.type == pygame.MOUSEBUTTONUP:
                if bola_activa:
                    bola_activa.dragging = False
                    colocada = False
                    
                    for destino in destinos:
                        if (distancia(bola_activa.pos, destino["pos"]) <= RADIO_DESTINO and 
                            bola_activa.color == destino["color"]):
                            bola_activa.pos = destino["pos"]
                            bola_activa.correcta = True
                            colocada = True
                            agregar_particulas(destino["pos"][0], destino["pos"][1], bola_activa.color)
                            break
                    
                    if not colocada and bola_activa.correcta:
                        # Si estaba correcta pero se movió, resetear
                        bola_activa.correcta = False
                        
                    bola_activa = None

            elif evento.type == pygame.MOUSEMOTION:
                # Actualizar hover de las bolas
                mouse_pos = evento.pos
                for bola in bolas:
                    bola.hover = bola.is_hovered(mouse_pos) and not bola.correcta
                
                if bola_activa and bola_activa.dragging:
                    bola_activa.pos = list(evento.pos)

        # Actualizar y dibujar partículas
        particulas = [p for p in particulas if p.vida > 0]
        for particula in particulas:
            particula.update()
            particula.draw(screen)

        # Dibujar destinos
        for destino in destinos:
            dibujar_destino(destino)

        # Dibujar bolas
        for bola in bolas:
            bola.draw(screen)

        # Verificar victoria
        if all(b.correcta for b in bolas):
            juego_ganado = True
            mostrar_mensaje_ganaste()
            dibujar_flecha()

        # Dibujar título
        titulo = fuente.render("🎯 Balls - Juego Educativo", True, COLOR_TEXTO_OSCURO)
        screen.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, 20))
        
        # Instrucciones
        instruccion = fuente_chica.render("Arrastra las pelotas a los aros del mismo color", True, COLOR_TEXTO_OSCURO)
        screen.blit(instruccion, (ANCHO // 2 - instruccion.get_width() // 2, 70))

        dibujar_banner()
        pygame.display.flip()
        reloj.tick(60)

if __name__ == "__main__":
    iniciar_juego()