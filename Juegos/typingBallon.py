import pygame
import random
import sys
import time

# Inicialización
pygame.init()
ANCHO, ALTO = 800, 600
PANTALLA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Explota los Globos")
FUENTE = pygame.font.SysFont("arial", 32)
RELOJ = pygame.time.Clock()

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (200, 0, 0)
AZUL = (0, 120, 255)

# Palabras configurables
PALABRAS = ["cielo", "mar", "sol", "nube", "árbol", "flor", "río", "pez", "luz", "estrella", "angel", "ala", "jungla", "Barco", "tierra", "luna"]

# Configuración del juego
globo_velocidad = 1.5
zona_peligro = 80  # Línea de peligro arriba
globo_intervalo = 2000  # ms
ultimo_globo = pygame.time.get_ticks()
palabra_actual = ""
records = []

# Cargar records
def cargar_records():
    try:
        with open("records.txt", "r") as f:
            return [line.strip().split(",") for line in f.readlines()]
    except:
        return []

# Guardar records
def guardar_records():
    with open("records.txt", "w") as f:
        for nombre, tiempo in records:
            f.write(f"{nombre},{tiempo}\n")

# Clase Globo
class Globo:
    def __init__(self, palabra):
        self.palabra = palabra
        self.x = random.randint(50, ANCHO - 150)
        self.y = -50
        self.ancho = 120
        self.alto = 60
        self.toques_peligro = 0

    def puede_bajar(self, globos):
        if self.y + self.alto >= ALTO:
            return False
        for otro in globos:
            if otro == self:
                continue
            distancia_x = abs(self.x - otro.x)
            distancia_y = (self.y + self.alto) - otro.y
            if distancia_x < self.ancho and 0 <= distancia_y < globo_velocidad + 2:
                return False
        return True

    def mover(self, globos):
        if self.puede_bajar(globos):
            self.y += globo_velocidad
        else:
            if self.y + self.alto > ALTO:
                self.y = ALTO - self.alto
            for otro in globos:
                if otro == self:
                    continue
                if abs(self.x - otro.x) < self.ancho:
                    if abs((self.y + self.alto) - otro.y) < globo_velocidad + 2:
                        self.y = otro.y - self.alto

    def dibujar(self):
        texto = FUENTE.render(self.palabra, True, NEGRO)
        pygame.draw.ellipse(PANTALLA, AZUL, (self.x, self.y, self.ancho, self.alto))
        PANTALLA.blit(texto, (self.x + 10, self.y + 15))

    def esta_en_peligro(self):
        return self.y <= zona_peligro

# Lista de globos
globos = []

# Función para mostrar texto centrado
def mostrar_texto(texto, y, tam=40, color=NEGRO):
    fuente = pygame.font.SysFont("arial", tam)
    texto_render = fuente.render(texto, True, color)
    rect = texto_render.get_rect(center=(ANCHO // 2, y))
    PANTALLA.blit(texto_render, rect)

# Función principal
def juego():
    global palabra_actual, records, ultimo_globo
    globos.clear()
    palabra_actual = ""
    inicio_tiempo = time.time()
    corriendo = True
    ultimo_globo = pygame.time.get_ticks()

    while corriendo:
        PANTALLA.fill(BLANCO)
        tiempo_actual = time.time()
        tiempo_jugado = round(tiempo_actual - inicio_tiempo, 1)

        # Generar globos cada cierto tiempo
        ahora = pygame.time.get_ticks()
        if ahora - ultimo_globo >= globo_intervalo:
            palabra = random.choice(PALABRAS)
            globos.append(Globo(palabra))
            ultimo_globo = ahora

        # Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_BACKSPACE:
                    palabra_actual = palabra_actual[:-1]
                elif evento.key == pygame.K_RETURN:
                    for globo in globos:
                        if globo.palabra == palabra_actual:
                            globos.remove(globo)
                            break
                    palabra_actual = ""
                else:
                    if len(palabra_actual) < 20:
                        palabra_actual += evento.unicode

        # Mover y dibujar globos
        for globo in globos:
            globo.mover(globos)
            globo.dibujar()

            if globo.esta_en_peligro():
                globo.toques_peligro += 1
                if globo.toques_peligro >= 2:
                    corriendo = False

        # Línea de peligro
        pygame.draw.line(PANTALLA, ROJO, (0, zona_peligro), (ANCHO, zona_peligro), 3)

        # Mostrar palabra escrita
        entrada = FUENTE.render(palabra_actual, True, NEGRO)
        PANTALLA.blit(entrada, (10, ALTO - 40))

        # Mostrar tiempo
        tiempo_render = FUENTE.render(f"Tiempo: {tiempo_jugado}s", True, NEGRO)
        PANTALLA.blit(tiempo_render, (ANCHO - 250, 10))

        pygame.display.flip()
        RELOJ.tick(60)

    # Fin del juego - guardar récord si aplica
    records = cargar_records()
    if len(records) < 3 or tiempo_jugado > float(records[-1][1]):
        nombre = ""
        escribiendo = True
        while escribiendo:
            PANTALLA.fill(BLANCO)
            mostrar_texto("¡Nuevo récord!", 150)
            mostrar_texto("Ingresa tu nombre (máx. 7 letras):", 220)
            mostrar_texto(nombre, 300)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_RETURN and nombre:
                        escribiendo = False
                    elif evento.key == pygame.K_BACKSPACE:
                        nombre = nombre[:-1]
                    else:
                        if len(nombre) < 7:
                            nombre += evento.unicode.upper()

            pygame.display.flip()
            RELOJ.tick(60)

        records.append((nombre, str(tiempo_jugado)))
        records = sorted(records, key=lambda x: float(x[1]), reverse=True)[:3]
        guardar_records()

    mostrar_pantalla_final(tiempo_jugado)

# Pantalla de final con records
def mostrar_pantalla_final(tiempo_final):
    mostrar = True
    while mostrar:
        PANTALLA.fill(BLANCO)
        mostrar_texto("Juego Terminado", 120)
        mostrar_texto(f"Tiempo sobrevivido: {tiempo_final}s", 180)
        mostrar_texto("Top 3:", 250)
        for i, (nombre, tiempo) in enumerate(records):
            mostrar_texto(f"{i+1}. {nombre} - {tiempo}s", 300 + i*40)

        mostrar_texto("Presiona ESPACIO para volver a jugar", 500)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    juego()

        pygame.display.flip()
        RELOJ.tick(60)

# Iniciar el juego
juego()
