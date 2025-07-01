import pygame
import sys
import random
import os
import math
from pygame.locals import *

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
ANCHO = 1200
ALTO = 750
PANTALLA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Aprende a Contar")

# Colores
FONDO = (230, 240, 255)
TEXTO = (40, 40, 40)
BOTON_NORMAL = (100, 180, 255)
BOTON_HOVER = (70, 150, 230)
BOTON_CORRECTO = (100, 230, 100)
BOTON_INCORRECTO = (255, 120, 120)
MENSAJE_GANADOR = (50, 200, 50)
MENSAJE_PERDEDOR = (220, 50, 50)
BOTON_REINICIAR = (255, 200, 50)
BOTON_SALIR = (255, 100, 100)

# Fuentes
FUENTE_GRANDE = pygame.font.SysFont('comicsansms', 48, bold=True)
FUENTE_MEDIANA = pygame.font.SysFont('comicsansms', 36)
FUENTE_PEQUEÑA = pygame.font.SysFont('comicsansms', 28)

# Clase para los botones
class Boton:
    def __init__(self, x, y, ancho, alto, texto, color_normal=BOTON_NORMAL):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.texto = texto
        self.color_normal = color_normal
        self.color = color_normal
        self.hover = False
        self.resaltado = False
        
    def dibujar(self, pantalla):
        pygame.draw.rect(pantalla, self.color, self.rect, border_radius=15)
        pygame.draw.rect(pantalla, (30, 30, 30), self.rect, 3, border_radius=15)
        
        texto = FUENTE_MEDIANA.render(self.texto, True, TEXTO)
        texto_rect = texto.get_rect(center=self.rect.center)
        pantalla.blit(texto, texto_rect)
        
    def verificar_mouse(self, pos):
        self.hover = self.rect.collidepoint(pos)
        self.color = BOTON_HOVER if self.hover else self.color_normal
        return self.hover
    
    def verificar_clic(self, pos):
        return self.rect.collidepoint(pos)

# Clase para los objetos contables
class Objeto:
    def __init__(self, tipo, x, y):
        self.tipo = tipo
        self.x = x
        self.y = y
        self.tamanio = random.randint(40, 70)
        
        # Crear formas simples
        self.forma = self.crear_forma()
        
    def crear_forma(self):
        superficie = pygame.Surface((self.tamanio, self.tamanio), pygame.SRCALPHA)
        
        if self.tipo == "carro":
            color = (random.randint(150, 255), random.randint(50, 150), random.randint(50, 150))
            pygame.draw.rect(superficie, color, (5, 15, self.tamanio-10, self.tamanio-25), border_radius=8)
            pygame.draw.rect(superficie, (30, 30, 40), (8, 8, self.tamanio-16, 10), border_radius=5)
            pygame.draw.circle(superficie, (40, 40, 40), (15, self.tamanio-10), 8)
            pygame.draw.circle(superficie, (40, 40, 40), (self.tamanio-15, self.tamanio-10), 8)
        
        elif self.tipo == "animal":
            color = (random.randint(100, 200), random.randint(150, 220), random.randint(100, 180))
            pygame.draw.ellipse(superficie, color, (5, 5, self.tamanio-10, self.tamanio-15))
            pygame.draw.circle(superficie, color, (self.tamanio//2, 0), self.tamanio//3)
            pygame.draw.circle(superficie, (240, 240, 240), (self.tamanio//2-8, -5), 5)
            pygame.draw.circle(superficie, (240, 240, 240), (self.tamanio//2+8, -5), 5)
            pygame.draw.circle(superficie, (30, 30, 30), (self.tamanio//2-8, -5), 2)
            pygame.draw.circle(superficie, (30, 30, 30), (self.tamanio//2+8, -5), 2)
            
        elif self.tipo == "fruta":
            color = (random.randint(200, 255), random.randint(50, 150), random.randint(50, 150))
            pygame.draw.circle(superficie, color, (self.tamanio//2, self.tamanio//2), self.tamanio//3)
            pygame.draw.rect(superficie, (100, 200, 50), (self.tamanio//2-3, 5, 6, 15))
            
        return superficie
        
    def dibujar(self, pantalla):
        pantalla.blit(self.forma, (self.x - self.tamanio//2, self.y - self.tamanio//2))
    
    def get_rect(self):
        """Retorna el rectángulo de colisión del objeto"""
        return pygame.Rect(self.x - self.tamanio//2, self.y - self.tamanio//2, self.tamanio, self.tamanio)

# Función para verificar si dos objetos se solapan
def objetos_se_solapan(obj1, obj2, margen=10):
    """
    Verifica si dos objetos se solapan considerando un margen adicional
    """
    distancia = math.sqrt((obj1.x - obj2.x)**2 + (obj1.y - obj2.y)**2)
    distancia_minima = (obj1.tamanio + obj2.tamanio) // 2 + margen
    return distancia < distancia_minima

# Función para encontrar una posición válida para un objeto
def encontrar_posicion_valida(objetos_existentes, area_juego, intentos_maximos=50):
    """
    Encuentra una posición válida para un nuevo objeto que no se solape con los existentes
    """
    for _ in range(intentos_maximos):
        x = random.randint(area_juego['x_min'], area_juego['x_max'])
        y = random.randint(area_juego['y_min'], area_juego['y_max'])
        
        # Crear objeto temporal para verificar colisiones
        objeto_temp = type('temp', (), {'x': x, 'y': y, 'tamanio': random.randint(40, 70)})()
        
        # Verificar si se solapa con algún objeto existente
        posicion_valida = True
        for obj_existente in objetos_existentes:
            if objetos_se_solapan(objeto_temp, obj_existente):
                posicion_valida = False
                break
        
        if posicion_valida:
            return x, y, objeto_temp.tamanio
    
    # Si no se encuentra posición válida después de muchos intentos, 
    # usar una posición aleatoria (fallback)
    return (random.randint(area_juego['x_min'], area_juego['x_max']), 
            random.randint(area_juego['y_min'], area_juego['y_max']), 
            random.randint(40, 70))

# Función para crear un nuevo nivel
def crear_nivel():
    global objetos, respuesta_correcta, opciones, botones, mensaje, mensaje_color, nivel, flecha_visible, botones_fin
    
    nivel += 1
    # Limpiar objetos anteriores
    objetos = []
    
    # Determinar cantidad de objetos (entre 1 y 15)
    cantidad = random.randint(1, 15)
    respuesta_correcta = cantidad
    
    # Definir área de juego (donde se pueden colocar objetos)
    area_juego = {
        'x_min': 80,
        'x_max': ANCHO - 80,
        'y_min': 150,
        'y_max': ALTO // 2 + 50
    }
    
    # Crear objetos sin solapamiento
    tipo_objeto = random.choice(["carro", "animal", "fruta"])
    
    for i in range(cantidad):
        # Si tenemos muchos objetos, reducir el área gradualmente para evitar bucles infinitos
        if i > 8:  # Después de 8 objetos, hacer el área más flexible
            area_juego['x_min'] = max(60, area_juego['x_min'] - 5)
            area_juego['x_max'] = min(ANCHO - 60, area_juego['x_max'] + 5)
            area_juego['y_min'] = max(130, area_juego['y_min'] - 5)
            area_juego['y_max'] = min(ALTO // 2 + 70, area_juego['y_max'] + 5)
        
        # Encontrar posición válida
        x, y, tamanio = encontrar_posicion_valida(objetos, area_juego)
        
        # Crear objeto con posición y tamaño específicos
        nuevo_objeto = Objeto(tipo_objeto, x, y)
        nuevo_objeto.tamanio = tamanio
        nuevo_objeto.forma = nuevo_objeto.crear_forma()  # Recrear forma con nuevo tamaño
        
        objetos.append(nuevo_objeto)
    
    # Crear opciones de respuesta
    opciones = [respuesta_correcta]
    
    # Añadir opciones incorrectas (números cercanos pero diferentes)
    while len(opciones) < 5:
        opcion = respuesta_correcta + random.randint(-3, 3)
        if opcion != respuesta_correcta and opcion > 0 and opcion <= 20 and opcion not in opciones:
            opciones.append(opcion)
    
    # Mezclar opciones
    random.shuffle(opciones)
    
    # Crear botones para las opciones
    botones = []
    for i, opcion in enumerate(opciones):
        x = 50 + i * 170
        y = ALTO - 120
        botones.append(Boton(x, y, 150, 70, str(opcion)))
    
    # Reiniciar estado del juego
    mensaje = ""
    mensaje_color = TEXTO
    flecha_visible = False
    botones_fin = []

# Función para dibujar la flecha de siguiente nivel
def dibujar_flecha():
    puntos = [(ANCHO - 60, ALTO // 2 - 20), 
              (ANCHO - 30, ALTO // 2), 
              (ANCHO - 60, ALTO // 2 + 20)]
    pygame.draw.polygon(PANTALLA, (50, 200, 50), puntos)
    pygame.draw.polygon(PANTALLA, (0, 0, 0), puntos, 3)

# Función para reiniciar el juego completo
def reiniciar_juego():
    global nivel
    nivel = 0
    crear_nivel()

def iniciar_juego():
    global nivel, flecha_visible, mensaje, mensaje_color, botones_fin, objetos, respuesta_correcta, opciones, botones
    
    nivel = 0
    flecha_visible = False
    mensaje = ""
    mensaje_color = TEXTO
    botones_fin = []  # Botones de reinicio y salir
    crear_nivel()

    # Crear botones de reinicio y salir (inicialmente ocultos)
    boton_reiniciar = Boton(ANCHO//2 - 180, ALTO//2 + 50, 150, 60, "Reiniciar", BOTON_REINICIAR)
    boton_salir = Boton(ANCHO//2 + 30, ALTO//2 + 50, 150, 60, "Salir", BOTON_SALIR)

    # Bucle principal del juego
    reloj = pygame.time.Clock()
    ejecutando = True

    while ejecutando:
        mouse_pos = pygame.mouse.get_pos()
        
        # Manejo de eventos
        for evento in pygame.event.get():
            if evento.type == QUIT:
                ejecutando = False
                pygame.quit()
                return
            
            if evento.type == MOUSEBUTTONDOWN:
                # Verificar clic en botones de opciones (solo si no hay mensaje de resultado)
                if not mensaje:
                    for boton in botones:
                        if boton.verificar_clic(mouse_pos):
                            seleccion = int(boton.texto)
                            
                            # Resaltar todos los botones
                            for b in botones:
                                b.resaltado = True
                            
                            # Verificar respuesta
                            if seleccion == respuesta_correcta:
                                mensaje = "¡Ganador!"
                                mensaje_color = MENSAJE_GANADOR
                                flecha_visible = True
                            else:
                                mensaje = "¡No ganamos!"
                                mensaje_color = MENSAJE_PERDEDOR
                                # Mostrar botones de reinicio y salir
                                botones_fin = [boton_reiniciar, boton_salir]
                
                # Verificar clic en flecha para siguiente nivel
                if flecha_visible:
                    if (ANCHO - 60 <= mouse_pos[0] <= ANCHO - 30 and 
                        ALTO // 2 - 20 <= mouse_pos[1] <= ALTO // 2 + 20):
                        crear_nivel()
                
                # Verificar clic en botones de fin
                for boton in botones_fin:
                    if boton.verificar_clic(mouse_pos):
                        if boton == boton_reiniciar:
                            reiniciar_juego()
                        elif boton == boton_salir:
                            ejecutando = False
        
        # Actualizar estado de botones (hover)
        for boton in botones:
            boton.verificar_mouse(mouse_pos)
        
        for boton in botones_fin:
            boton.verificar_mouse(mouse_pos)
        
        # Dibujar
        PANTALLA.fill(FONDO)
        
        # Dibujar título
        titulo = FUENTE_GRANDE.render(f"Aprende a Contar - Nivel {nivel}", True, (50, 100, 200))
        PANTALLA.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, 20))
        
        # Dibujar instrucciones
        instrucciones = FUENTE_PEQUEÑA.render("¿Cuántos objetos hay?", True, TEXTO)
        PANTALLA.blit(instrucciones, (ANCHO // 2 - instrucciones.get_width() // 2, 80))
        
        # Dibujar objetos
        for objeto in objetos:
            objeto.dibujar(PANTALLA)
        
        # Dibujar botones de opciones
        for boton in botones:
            boton.dibujar(PANTALLA)
        
        # Dibujar mensaje
        if mensaje:
            mensaje_texto = FUENTE_MEDIANA.render(mensaje, True, mensaje_color)
            PANTALLA.blit(mensaje_texto, (ANCHO // 2 - mensaje_texto.get_width() // 2, ALTO - 200))
        
        # Dibujar flecha para siguiente nivel
        if flecha_visible:
            dibujar_flecha()
            flecha_texto = FUENTE_PEQUEÑA.render("Siguiente", True, (50, 150, 50))
            PANTALLA.blit(flecha_texto, (ANCHO - 110, ALTO // 2 + 40))
        
        # Dibujar botones de fin (reiniciar y salir)
        for boton in botones_fin:
            boton.dibujar(PANTALLA)
        
        pygame.display.flip()
        reloj.tick(60)

# Si se ejecuta este archivo directamente, iniciar el juego
if __name__ == "__main__":
    iniciar_juego()
    pygame.quit()
    sys.exit()