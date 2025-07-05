import pygame
import sys
import os
import math
import Balones, Teclado_Mecanografia, Figuras_flotantes, Contador, balloon_pop

pygame.init()

# Configuración de ventana
ANCHO_MIN, ALTO_MIN = 800, 600
ANCHO_DEFAULT, ALTO_DEFAULT = 1200, 800
screen = pygame.display.set_mode((ANCHO_DEFAULT, ALTO_DEFAULT), pygame.RESIZABLE)
pygame.display.set_caption("Menú Principal - Juegos Educativos")

# Fuentes
fuente_titulo = pygame.font.SysFont("Arial", 48, bold=True)
fuente_juego = pygame.font.SysFont("Arial", 24, bold=True)
fuente_icono = pygame.font.SysFont("Arial", 60)

# Colores modernos
COLOR_FONDO_GRADIENT_TOP = (45, 52, 70)
COLOR_FONDO_GRADIENT_BOTTOM = (25, 30, 45)
COLOR_CARD = (255, 255, 255)
COLOR_CARD_HOVER = (245, 245, 245)
COLOR_TEXTO = (50, 50, 50)
COLOR_TEXTO_HOVER = (0, 120, 215)
COLOR_SOMBRA = (0, 0, 0, 30)
COLOR_FLECHA = (100, 100, 100)
COLOR_FLECHA_HOVER = (0, 120, 215)
COLOR_TITULO = (255, 255, 255)

# Configuración de juegos
juegos = [
    {"nombre": "Juego de las Canicas", "imagen": "IMAGENES/balls.png", "icono": "⚽", "activo": True},
    {"nombre": "Juego de Mecanografía", "imagen": "IMAGENES/teclado.png", "icono": "⌨️", "activo": True},
    {"nombre": "Juego de Formas", "imagen": "IMAGENES/formas.png", "icono": "🔷", "activo": True},
    {"nombre": "Juego de Contar", "imagen": "IMAGENES/cuentas.png", "icono": "🔢", "activo": True},
    {"nombre": "Explota los Globos", "imagen": "IMAGENES/rebienta_globos.png", "icono": "🎈", "activo": True},
    {"nombre": "Juego de Contar Difícil", "imagen": "", "icono": "🧮", "activo": True},
    {"nombre": "Sigue el Patrón", "imagen": "", "icono": "🔄", "activo": True},
    {"nombre": "Memoria Visual", "imagen": "", "icono": "🧠", "activo": True},
    {"nombre": "Laberinto", "imagen": "", "icono": "🌀", "activo": True},
    {"nombre": "Rompecabezas", "imagen": "", "icono": "🧩", "activo": True}
]

# Variables de estado
pagina_actual = 0
juegos_por_pagina = 6
total_paginas = math.ceil(len([j for j in juegos if j["activo"]]) / juegos_por_pagina)
hover_card = -1
hover_flecha = None
animacion_card = {}

class MenuJuego:
    def __init__(self):
        self.ancho = ANCHO_DEFAULT
        self.alto = ALTO_DEFAULT
        self.imagenes_cache = {}
        self.imagenes_escaladas_cache = {}  # Cache para imágenes escaladas
        self.cargar_imagenes()
        
    def cargar_imagenes(self):
        """Carga las imágenes originales sin redimensionar"""
        for juego in juegos:
            if juego["imagen"] and os.path.isfile(juego["imagen"]):
                try:
                    img = pygame.image.load(juego["imagen"]).convert_alpha()
                    self.imagenes_cache[juego["imagen"]] = img
                except pygame.error:
                    print(f"Error cargando imagen: {juego['imagen']}")
    
    def escalar_imagen_suave(self, imagen, nuevo_ancho, nuevo_alto):
        """Escala una imagen usando algoritmo de suavizado mejorado"""
        # Obtener dimensiones originales
        ancho_orig, alto_orig = imagen.get_size()
        
        # Si las dimensiones son las mismas, no hacer nada
        if ancho_orig == nuevo_ancho and alto_orig == nuevo_alto:
            return imagen
        
        # Calcular la relación de aspecto
        ratio_orig = ancho_orig / alto_orig
        ratio_nuevo = nuevo_ancho / nuevo_alto
        
        # Ajustar para mantener la relación de aspecto
        if ratio_orig > ratio_nuevo:
            # La imagen es más ancha, ajustar por ancho
            ancho_final = nuevo_ancho
            alto_final = int(nuevo_ancho / ratio_orig)
        else:
            # La imagen es más alta, ajustar por alto
            alto_final = nuevo_alto
            ancho_final = int(nuevo_alto * ratio_orig)
        
        # Usar smoothscale para mejor calidad
        try:
            imagen_escalada = pygame.transform.smoothscale(imagen, (ancho_final, alto_final))
        except ValueError:
            # Fallback si smoothscale falla
            imagen_escalada = pygame.transform.scale(imagen, (ancho_final, alto_final))
        
        return imagen_escalada
    
    def actualizar_dimensiones(self, ancho, alto):
        """Actualiza las dimensiones cuando se redimensiona la ventana"""
        self.ancho = max(ancho, ANCHO_MIN)
        self.alto = max(alto, ALTO_MIN)
    
    def dibujar_gradiente(self, surface, color_top, color_bottom, rect):
        """Dibuja un gradiente vertical"""
        for y in range(rect.height):
            ratio = y / rect.height
            r = int(color_top[0] * (1 - ratio) + color_bottom[0] * ratio)
            g = int(color_top[1] * (1 - ratio) + color_bottom[1] * ratio)
            b = int(color_top[2] * (1 - ratio) + color_bottom[2] * ratio)
            pygame.draw.line(surface, (r, g, b), 
                           (rect.x, rect.y + y), (rect.x + rect.width, rect.y + y))
    
    def dibujar_sombra(self, surface, rect, offset=5):
        """Dibuja una sombra suave"""
        shadow_surf = pygame.Surface((rect.width + offset*2, rect.height + offset*2), pygame.SRCALPHA)
        pygame.draw.rect(shadow_surf, COLOR_SOMBRA, 
                        (offset, offset, rect.width, rect.height), border_radius=15)
        surface.blit(shadow_surf, (rect.x - offset, rect.y - offset))
    
    def obtener_juegos_activos(self):
        """Obtiene solo los juegos activos"""
        return [juego for juego in juegos if juego["activo"]]
    
    def obtener_juegos_pagina(self):
        """Obtiene los juegos de la página actual"""
        juegos_activos = self.obtener_juegos_activos()
        inicio = pagina_actual * juegos_por_pagina
        fin = inicio + juegos_por_pagina
        return juegos_activos[inicio:fin]
    
    def calcular_layout(self):
        """Calcula el diseño responsivo de las cards"""
        padding = 60
        area_util_ancho = self.ancho - 2 * padding
        area_util_alto = self.alto - 180  # Espacio para título y navegación
        
        # Calcular tamaño de cards
        cols = 3
        rows = 2
        
        espacio_h = area_util_ancho // cols
        espacio_v = area_util_alto // rows
        
        card_ancho = min(espacio_h - 20, 250)
        card_alto = min(espacio_v - 20, 200)
        
        # Centrar la grilla
        total_ancho = cols * card_ancho + (cols - 1) * 20
        total_alto = rows * card_alto + (rows - 1) * 20
        
        inicio_x = (self.ancho - total_ancho) // 2
        inicio_y = 120 + (area_util_alto - total_alto) // 2
        
        return card_ancho, card_alto, inicio_x, inicio_y
    
    def dibujar_flecha(self, surface, direccion, rect, hover=False):
        """Dibuja una flecha moderna"""
        color = COLOR_FLECHA_HOVER if hover else COLOR_FLECHA
        centro = rect.center
        
        # Fondo circular
        pygame.draw.circle(surface, (255, 255, 255, 100), centro, 25)
        pygame.draw.circle(surface, color, centro, 25, 3)
        
        # Flecha
        if direccion == "izquierda":
            puntos = [
                (centro[0] + 8, centro[1] - 10),
                (centro[0] - 8, centro[1]),
                (centro[0] + 8, centro[1] + 10)
            ]
        else:  # derecha
            puntos = [
                (centro[0] - 8, centro[1] - 10),
                (centro[0] + 8, centro[1]),
                (centro[0] - 8, centro[1] + 10)
            ]
        
        pygame.draw.polygon(surface, color, puntos)
    
    def dibujar_card(self, surface, juego, rect, index):
        """Dibuja una card moderna para cada juego"""
        # Animación de hover
        if index in animacion_card:
            animacion_card[index] = min(animacion_card[index] + 0.1, 1.0)
        else:
            animacion_card[index] = 0.0
        
        hover = hover_card == index
        if hover and index not in animacion_card:
            animacion_card[index] = 0.0
        
        # Efecto de elevación
        elevacion = int(animacion_card[index] * 10) if hover else 0
        card_rect = pygame.Rect(rect.x, rect.y - elevacion, rect.width, rect.height)
        
        # Sombra
        self.dibujar_sombra(surface, card_rect, 8 + elevacion)
        
        # Fondo de la card
        color_fondo = COLOR_CARD_HOVER if hover else COLOR_CARD
        pygame.draw.rect(surface, color_fondo, card_rect, border_radius=15)
        
        # Borde sutil
        pygame.draw.rect(surface, (200, 200, 200), card_rect, 2, border_radius=15)
        
        # Área de imagen/icono
        icono_rect = pygame.Rect(card_rect.x + 20, card_rect.y + 20, 
                                card_rect.width - 40, card_rect.height - 80)
        
        # Imagen o icono
        if juego["imagen"] and juego["imagen"] in self.imagenes_cache:
            img_original = self.imagenes_cache[juego["imagen"]]
            
            # Crear clave única para el cache basada en tamaño
            cache_key = f"{juego['imagen']}_{icono_rect.width}x{icono_rect.height}"
            
            # Verificar si ya tenemos esta imagen escalada en cache
            if cache_key not in self.imagenes_escaladas_cache:
                # Escalar con algoritmo de suavizado
                img_scaled = self.escalar_imagen_suave(img_original, icono_rect.width, icono_rect.height)
                self.imagenes_escaladas_cache[cache_key] = img_scaled
            else:
                img_scaled = self.imagenes_escaladas_cache[cache_key]
            
            # Centrar la imagen en el área disponible
            img_rect = img_scaled.get_rect()
            img_rect.center = icono_rect.center
            
            # Dibujar la imagen escalada
            surface.blit(img_scaled, img_rect)
        else:
            # Mostrar icono emoji
            icono_surface = fuente_icono.render(juego["icono"], True, COLOR_TEXTO_HOVER)
            icono_pos = (icono_rect.centerx - icono_surface.get_width() // 2,
                        icono_rect.centery - icono_surface.get_height() // 2)
            surface.blit(icono_surface, icono_pos)
        
        # Título del juego
        color_texto = COLOR_TEXTO_HOVER if hover else COLOR_TEXTO
        texto = fuente_juego.render(juego["nombre"], True, color_texto)
        
        # Texto multi-línea si es necesario
        palabras = juego["nombre"].split()
        if len(palabras) > 2:
            linea1 = " ".join(palabras[:2])
            linea2 = " ".join(palabras[2:])
            
            texto1 = fuente_juego.render(linea1, True, color_texto)
            texto2 = fuente_juego.render(linea2, True, color_texto)
            
            y_texto = card_rect.bottom - 50
            surface.blit(texto1, (card_rect.centerx - texto1.get_width() // 2, y_texto))
            surface.blit(texto2, (card_rect.centerx - texto2.get_width() // 2, y_texto + 25))
        else:
            y_texto = card_rect.bottom - 40
            surface.blit(texto, (card_rect.centerx - texto.get_width() // 2, y_texto))
    
    def dibujar_menu(self):
        """Dibuja el menú principal"""
        global hover_card, hover_flecha
        
        # Fondo con gradiente
        self.dibujar_gradiente(screen, COLOR_FONDO_GRADIENT_TOP, COLOR_FONDO_GRADIENT_BOTTOM, 
                              pygame.Rect(0, 0, self.ancho, self.alto))
        
        # Título
        titulo = fuente_titulo.render("Juegos Educativos", True, COLOR_TITULO)
        titulo_rect = titulo.get_rect(center=(self.ancho // 2, 50))
        screen.blit(titulo, titulo_rect)
        
        # Indicador de página
        if total_paginas > 1:
            indicador = f"Página {pagina_actual + 1} de {total_paginas}"
            texto_indicador = fuente_juego.render(indicador, True, COLOR_TITULO)
            screen.blit(texto_indicador, (self.ancho // 2 - texto_indicador.get_width() // 2, 85))
        
        # Calcular layout
        card_ancho, card_alto, inicio_x, inicio_y = self.calcular_layout()
        
        # Dibujar cards de juegos
        juegos_pagina = self.obtener_juegos_pagina()
        mouse_pos = pygame.mouse.get_pos()
        hover_card = -1
        
        for i, juego in enumerate(juegos_pagina):
            fila = i // 3
            col = i % 3
            
            x = inicio_x + col * (card_ancho + 20)
            y = inicio_y + fila * (card_alto + 20)
            
            card_rect = pygame.Rect(x, y, card_ancho, card_alto)
            
            # Detectar hover
            if card_rect.collidepoint(mouse_pos):
                hover_card = i
            
            self.dibujar_card(screen, juego, card_rect, i)
        
        # Flechas de navegación
        hover_flecha = None
        if total_paginas > 1:
            flecha_size = 50
            
            # Flecha izquierda
            if pagina_actual > 0:
                flecha_izq_rect = pygame.Rect(30, self.alto // 2 - flecha_size // 2, 
                                            flecha_size, flecha_size)
                hover_izq = flecha_izq_rect.collidepoint(mouse_pos)
                if hover_izq:
                    hover_flecha = "izquierda"
                self.dibujar_flecha(screen, "izquierda", flecha_izq_rect, hover_izq)
            
            # Flecha derecha
            if pagina_actual < total_paginas - 1:
                flecha_der_rect = pygame.Rect(self.ancho - 80, self.alto // 2 - flecha_size // 2, 
                                            flecha_size, flecha_size)
                hover_der = flecha_der_rect.collidepoint(mouse_pos)
                if hover_der:
                    hover_flecha = "derecha"
                self.dibujar_flecha(screen, "derecha", flecha_der_rect, hover_der)
        
        pygame.display.flip()
    
    def obtener_rect_cards(self):
        """Obtiene los rectangulos de las cards para detección de clics"""
        card_ancho, card_alto, inicio_x, inicio_y = self.calcular_layout()
        rects = []
        
        juegos_pagina = self.obtener_juegos_pagina()
        for i in range(len(juegos_pagina)):
            fila = i // 3
            col = i % 3
            
            x = inicio_x + col * (card_ancho + 20)
            y = inicio_y + fila * (card_alto + 20)
            
            rects.append(pygame.Rect(x, y, card_ancho, card_alto))
        
        return rects
    
    def obtener_rect_flechas(self):
        """Obtiene los rectangulos de las flechas para detección de clics"""
        flecha_size = 50
        flechas = {}
        
        if total_paginas > 1:
            if pagina_actual > 0:
                flechas["izquierda"] = pygame.Rect(30, self.alto // 2 - flecha_size // 2, 
                                                 flecha_size, flecha_size)
            if pagina_actual < total_paginas - 1:
                flechas["derecha"] = pygame.Rect(self.ancho - 80, self.alto // 2 - flecha_size // 2, 
                                               flecha_size, flecha_size)
        
        return flechas

# Funciones de juegos
def juego_balls():
    Balones.iniciar_juego()

def juego_teclado():
    # Obtener el tamaño actual de la ventana
    resultado = Teclado_Mecanografia.iniciar_juego()
    if resultado:  # Si el juego retorna un tamaño
        ancho, alto = resultado
        # Redimensionar la ventana del menú al tamaño que tenía el juego
        global screen, menu
        screen = pygame.display.set_mode((ancho, alto), pygame.RESIZABLE)
        menu.actualizar_dimensiones(ancho, alto)

def juego_figuras():
    Figuras_flotantes.iniciar_juego()

def juego_contar():
    Contador.iniciar_juego()

def juego_balloon_pop():
    balloon_pop.draw_background()

def juego_placeholder():
    print("Juego no implementado aún")

# Mapeo de funciones por índice global
funciones_juego = {
    0: juego_balls,
    1: juego_teclado,
    2: juego_figuras,
    3: juego_contar,
    4: juego_balloon_pop,
    5: juego_placeholder,
    6: juego_placeholder,
    7: juego_placeholder,
    8: juego_placeholder,
    9: juego_placeholder
}

# Inicializar menú
menu = MenuJuego()
clock = pygame.time.Clock()

# Bucle principal
running = True
while running:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            running = False
        
        elif evento.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((evento.w, evento.h), pygame.RESIZABLE)
            menu.actualizar_dimensiones(evento.w, evento.h)
        
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:  # Click izquierdo
                pos_click = evento.pos
                
                # Verificar click en cards
                card_rects = menu.obtener_rect_cards()
                for i, rect in enumerate(card_rects):
                    if rect.collidepoint(pos_click):
                        # Obtener índice global del juego
                        juegos_activos = menu.obtener_juegos_activos()
                        juego_index = juegos.index(juegos_activos[pagina_actual * juegos_por_pagina + i])
                        
                        if juego_index in funciones_juego:
                            funciones_juego[juego_index]()
                        break
                
                # Verificar click en flechas
                flecha_rects = menu.obtener_rect_flechas()
                if "izquierda" in flecha_rects and flecha_rects["izquierda"].collidepoint(pos_click):
                    pagina_actual = max(0, pagina_actual - 1)
                elif "derecha" in flecha_rects and flecha_rects["derecha"].collidepoint(pos_click):
                    pagina_actual = min(total_paginas - 1, pagina_actual + 1)
        
        elif evento.type == pygame.KEYDOWN:
            # Navegación con teclado
            if evento.key == pygame.K_LEFT:
                pagina_actual = max(0, pagina_actual - 1)
            elif evento.key == pygame.K_RIGHT:
                pagina_actual = min(total_paginas - 1, pagina_actual + 1)
    
    # Actualizar animaciones
    for key in list(animacion_card.keys()):
        if hover_card != key:
            animacion_card[key] = max(animacion_card[key] - 0.1, 0.0)
            if animacion_card[key] <= 0:
                del animacion_card[key]
    
    menu.dibujar_menu()
    clock.tick(60)

pygame.quit()
sys.exit()