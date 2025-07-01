import pygame
import random
import platform
import math
import sys

# Inicialización de Pygame con manejo de errores
try:
    pygame.init()
    pygame.mixer.init()
except Exception as e:
    print(f"Error inicializando Pygame: {e}")
    sys.exit(1)

# Configuración de la ventana
WIDTH, HEIGHT = 800, 600
try:
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("🎈 Balloon Pop Adventure 🎈")
except Exception as e:
    print(f"Error configurando la ventana: {e}")
    sys.exit(1)

FPS = 60
clock = pygame.time.Clock()

# Colores modernos y vibrantes
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY_BLUE = (135, 206, 235)
DEEP_SKY = (0, 191, 255)
GLOW_PINK = (255, 20, 147)
GLOW_GREEN = (50, 205, 50)
GLOW_YELLOW = (255, 215, 0)
GLOW_PURPLE = (138, 43, 226)
GLOW_ORANGE = (255, 140, 0)
GLOW_CYAN = (0, 255, 255)
DARK_RED = (139, 0, 0)
GOLD = (255, 215, 0)

# Colores para efectos
COLORS_PALETTE = [GLOW_PINK, GLOW_GREEN, GLOW_YELLOW, GLOW_PURPLE, GLOW_ORANGE, GLOW_CYAN]

# Fuentes
try:
    font_large = pygame.font.SysFont('comicsans', 48, bold=True)
    font_medium = pygame.font.SysFont('comicsans', 32, bold=True)
    font_small = pygame.font.SysFont('comicsans', 24)
except Exception as e:
    print(f"Error cargando fuente: {e}")
    font_large = pygame.font.Font(None, 48)
    font_medium = pygame.font.Font(None, 32)
    font_small = pygame.font.Font(None, 24)

# Fondos mejorados
BACKGROUNDS = [
    [(25, 25, 112), (135, 206, 235), (255, 182, 193)],  # Atardecer
    [(0, 100, 0), (34, 139, 34), (144, 238, 144)],      # Bosque
    [(70, 130, 180), (135, 206, 235), (255, 255, 255)], # Cielo
    [(25, 25, 112), (72, 61, 139), (147, 112, 219)]     # Noche
]

# Variables globales del juego
current_background = 0
background_timer = 0
game_speed_multiplier = 1.0

# Clase para los globos mejorada
class Balloon:
    def __init__(self):
        self.x = random.randint(60, WIDTH - 60)
        self.y = random.randint(-100, -50)
        self.letter = random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
        self.color = random.choice(COLORS_PALETTE)
        self.speed = random.uniform(0.8, 2.5) * game_speed_multiplier
        self.radius = 35
        self.bounce_offset = 0
        self.bounce_speed = random.uniform(0.1, 0.3)
        self.glow_intensity = 0
        self.glow_direction = 1
        self.rotation = 0
        self.size_pulse = 0
        
    def draw(self):
        try:
            # Efecto de movimiento flotante
            float_y = self.y + math.sin(self.bounce_offset) * 3
            
            # Efecto de respiración en el tamaño
            current_radius = self.radius + math.sin(self.size_pulse) * 2
            
            # Dibujar sombra del globo
            shadow_color = (100, 100, 100, 100)
            pygame.draw.circle(screen, (80, 80, 80), (int(self.x + 3), int(float_y + 3)), int(current_radius))
            
            # Dibujar globo principal con gradiente simulado
            for i in range(5):
                color_factor = 1 - (i * 0.15)
                gradient_color = tuple(int(c * color_factor) for c in self.color)
                pygame.draw.circle(screen, gradient_color, 
                                 (int(self.x), int(float_y)), 
                                 int(current_radius - i * 2))
            
            # Efecto de brillo
            highlight_color = tuple(min(255, c + 50) for c in self.color)
            pygame.draw.circle(screen, highlight_color, 
                             (int(self.x - 8), int(float_y - 8)), 6)
            
            # Borde del globo
            pygame.draw.circle(screen, WHITE, (int(self.x), int(float_y)), int(current_radius), 2)
            
            # Hilo del globo
            pygame.draw.line(screen, (139, 69, 19), 
                           (int(self.x), int(float_y + current_radius)), 
                           (int(self.x), int(float_y + current_radius + 20)), 3)
            
            # Letra con efecto de sombra
            letter_surface = font_medium.render(self.letter, True, BLACK)
            screen.blit(letter_surface, (self.x - 12, float_y - 17))
            letter_surface = font_medium.render(self.letter, True, WHITE)
            screen.blit(letter_surface, (self.x - 15, float_y - 20))
            
        except Exception as e:
            print(f"Error dibujando globo: {e}")

    def update(self):
        self.y += self.speed
        self.bounce_offset += self.bounce_speed
        self.size_pulse += 0.05
        self.rotation += 1
        
        # El globo se considera "perdido" si sale completamente de la pantalla
        return self.y < HEIGHT + self.radius

    def is_lost(self):
        return self.y > HEIGHT + self.radius

# Clase para los dardos mejorada
class Dart:
    def __init__(self, x, y, target_x, target_y):
        self.x = x
        self.y = y
        self.target_x = target_x
        self.target_y = target_y
        self.speed = 12
        self.trail = []
        try:
            angle = math.atan2(target_y - y, target_x - x)
            self.dx = math.cos(angle) * self.speed
            self.dy = math.sin(angle) * self.speed
        except Exception as e:
            print(f"Error calculando trayectoria del dardo: {e}")
            self.dx = 0
            self.dy = 0

    def draw(self):
        try:
            # Dibujar estela del dardo
            for i, pos in enumerate(self.trail):
                alpha = int(255 * (i / len(self.trail)) * 0.5)
                trail_color = (255, 100, 100)
                pygame.draw.circle(screen, trail_color, (int(pos[0]), int(pos[1])), max(1, 3 - i))
            
            # Dardo principal con mejor diseño
            dart_length = 15
            dart_width = 4
            
            # Cuerpo del dardo
            pygame.draw.line(screen, (139, 69, 19), 
                           (self.x, self.y), 
                           (self.x + dart_length, self.y), dart_width)
            
            # Punta del dardo
            pygame.draw.circle(screen, (220, 20, 60), (int(self.x + dart_length), int(self.y)), 6)
            pygame.draw.circle(screen, (255, 255, 255), (int(self.x + dart_length), int(self.y)), 6, 2)
            
            # Pluma del dardo
            feather_points = [
                (self.x - 5, self.y - 3),
                (self.x - 10, self.y),
                (self.x - 5, self.y + 3)
            ]
            pygame.draw.polygon(screen, (255, 215, 0), feather_points)
            
        except Exception as e:
            print(f"Error dibujando dardo: {e}")

    def update(self):
        self.trail.append((self.x, self.y))
        if len(self.trail) > 8:
            self.trail.pop(0)
            
        self.x += self.dx
        self.y += self.dy
        
        try:
            return (self.x < WIDTH + 50 and self.x > -50 and 
                   self.y < HEIGHT + 50 and self.y > -50)
        except Exception as e:
            print(f"Error actualizando dardo: {e}")
            return False

# Clase para el confeti mejorada
class Confetti:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = random.choice(COLORS_PALETTE + [WHITE, GOLD])
        self.dx = random.uniform(-4, 4)
        self.dy = random.uniform(-3, 1)
        self.size = random.randint(4, 8)
        self.lifetime = 90
        self.max_lifetime = 90
        self.rotation = 0
        self.rotation_speed = random.uniform(-5, 5)

    def draw(self):
        try:
            alpha = self.lifetime / self.max_lifetime
            current_size = int(self.size * alpha)
            
            if current_size > 0:
                # Dibujar confeti con rotación
                points = []
                for i in range(4):
                    angle = self.rotation + (i * 90)
                    px = self.x + math.cos(math.radians(angle)) * current_size
                    py = self.y + math.sin(math.radians(angle)) * current_size
                    points.append((px, py))
                
                if len(points) >= 3:
                    pygame.draw.polygon(screen, self.color, points)
                    
        except Exception as e:
            print(f"Error dibujando confeti: {e}")

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.dy += 0.1  # Gravedad
        self.rotation += self.rotation_speed
        self.lifetime -= 1
        return self.lifetime > 0

# Clase para efectos de texto flotante
class FloatingText:
    def __init__(self, x, y, text, color, size=24):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.lifetime = 60
        self.dy = -2
        self.font = pygame.font.SysFont('comicsans', size, bold=True)
        
    def draw(self):
        try:
            alpha = self.lifetime / 60
            if alpha > 0:
                text_surface = self.font.render(self.text, True, self.color)
                screen.blit(text_surface, (int(self.x), int(self.y)))
        except Exception as e:
            print(f"Error dibujando texto flotante: {e}")
    
    def update(self):
        self.y += self.dy
        self.lifetime -= 1
        return self.lifetime > 0

# Estado global del juego
balloons = []
darts = []
confetti = []
floating_texts = []
score = 0
high_score = 0

def draw_background():
    try:
        background = BACKGROUNDS[current_background]
        if len(background) == 3:  # Gradiente de 3 colores
            for y in range(HEIGHT):
                if y < HEIGHT // 2:
                    t = y / (HEIGHT // 2)
                    r = int(background[0][0] * (1 - t) + background[1][0] * t)
                    g = int(background[0][1] * (1 - t) + background[1][1] * t)
                    b = int(background[0][2] * (1 - t) + background[1][2] * t)
                else:
                    t = (y - HEIGHT // 2) / (HEIGHT // 2)
                    r = int(background[1][0] * (1 - t) + background[2][0] * t)
                    g = int(background[1][1] * (1 - t) + background[2][1] * t)
                    b = int(background[1][2] * (1 - t) + background[2][2] * t)
                pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))
        
        # Agregar nubes decorativas
        for i in range(3):
            cloud_x = (i * 250 + 100 + (background_timer // 2) % 100) % (WIDTH + 100)
            cloud_y = 50 + i * 30
            draw_cloud(cloud_x, cloud_y)
            
    except Exception as e:
        print(f"Error dibujando fondo: {e}")
        screen.fill(SKY_BLUE)

def draw_cloud(x, y):
    cloud_color = (255, 255, 255, 180)
    pygame.draw.circle(screen, (220, 220, 220), (int(x), int(y)), 25)
    pygame.draw.circle(screen, (220, 220, 220), (int(x + 20), int(y)), 35)
    pygame.draw.circle(screen, (220, 220, 220), (int(x + 40), int(y)), 25)
    pygame.draw.circle(screen, (220, 220, 220), (int(x + 10), int(y - 15)), 20)
    pygame.draw.circle(screen, (220, 220, 220), (int(x + 30), int(y - 15)), 20)

def draw_ui():
    # Panel de información con fondo semi-transparente
    ui_surface = pygame.Surface((WIDTH, 80))
    ui_surface.set_alpha(200)
    ui_surface.fill((0, 0, 0))
    screen.blit(ui_surface, (0, 0))
    
    # Puntaje actual con efectos
    score_text = font_large.render(f"Score: {score}", True, GOLD)
    score_shadow = font_large.render(f"Score: {score}", True, BLACK)
    screen.blit(score_shadow, (12, 12))
    screen.blit(score_text, (10, 10))
    
    # Puntaje máximo
    high_score_text = font_small.render(f"Best: {high_score}", True, WHITE)
    screen.blit(high_score_text, (10, 50))
    
    # Nivel de velocidad
    speed_text = font_small.render(f"Speed: {game_speed_multiplier:.1f}x", True, WHITE)
    screen.blit(speed_text, (WIDTH - 120, 50))
    
    # Instrucciones
    if score == 0:  # Solo mostrar al inicio
        instruction_text = font_small.render("Press letter keys to pop balloons!", True, WHITE)
        screen.blit(instruction_text, (WIDTH // 2 - 150, HEIGHT - 30))

def setup():
    global balloons, score, high_score
    balloons = [Balloon() for _ in range(2)]
    if score > high_score:
        high_score = score
    score = 0

def main():
    global score, balloons, darts, confetti, floating_texts, current_background, background_timer, game_speed_multiplier, high_score

    setup()
    running = True
    balloon_spawn_timer = 0

    while running:
        background_timer += 1
        
        # Cambiar fondo cada 30 segundos
        if background_timer % (30 * FPS) == 0:
            current_background = (current_background + 1) % len(BACKGROUNDS)
        
        # Aumentar velocidad gradualmente
        game_speed_multiplier = 1.0 + (score // 100) * 0.2

        # 1) Procesar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and score == 0:  # Reiniciar
                    setup()
                    continue
                    
                key = pygame.key.name(event.key)
                if key in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ':
                    hit_balloon = False
                    for balloon in balloons[:]:
                        if balloon.letter.lower() == key.lower():
                            # Crear dardo hacia el globo
                            darts.append(Dart(WIDTH // 2, HEIGHT - 50, balloon.x, balloon.y))
                            balloons.remove(balloon)
                            score += 10
                            hit_balloon = True
                            
                            # Generar confeti en la posición del globo
                            for _ in range(25):
                                confetti.append(Confetti(balloon.x, balloon.y))
                                
                            # Texto flotante de puntuación
                            floating_texts.append(FloatingText(balloon.x, balloon.y, "+10", GLOW_GREEN, 32))
                            break
                    
                    # Penalización por tecla incorrecta
                    if not hit_balloon and score > 0:
                        score = max(0, score - 2)
                        floating_texts.append(FloatingText(WIDTH // 2, HEIGHT // 2, "-2", DARK_RED, 24))

        # 2) Actualizar objetos
        new_balloons = []
        for balloon in balloons:
            if balloon.update():
                if balloon.is_lost():
                    # Penalización por globo perdido
                    score = max(0, score - 5)
                    floating_texts.append(FloatingText(balloon.x, HEIGHT - 50, "-5", DARK_RED, 28))
                else:
                    new_balloons.append(balloon)
        balloons = new_balloons
        
        darts = [d for d in darts if d.update()]
        confetti = [c for c in confetti if c.update()]
        floating_texts = [ft for ft in floating_texts if ft.update()]

        # 3) Generar nuevos globos
        balloon_spawn_timer += 1
        spawn_rate = max(60, 120 - (score // 50))  # Más globos conforme aumenta el puntaje
        
        if balloon_spawn_timer >= spawn_rate:
            if len(balloons) < 5:  # Máximo 5 globos en pantalla
                balloons.append(Balloon())
            balloon_spawn_timer = 0

        # 4) Dibujar todo
        draw_background()

        # Dibujar objetos del juego
        for balloon in balloons:
            balloon.draw()
        for dart in darts:
            dart.draw()
        for c in confetti:
            c.draw()
        for ft in floating_texts:
            ft.draw()

        # UI
        draw_ui()
        
        # Game Over si el puntaje llega a 0 y hay globos perdidos
        if score <= 0 and len([b for b in balloons if b.y > HEIGHT]) > 0:
            game_over_text = font_large.render("Game Over! Press R to restart", True, DARK_RED)
            game_over_shadow = font_large.render("Game Over! Press R to restart", True, BLACK)
            screen.blit(game_over_shadow, (WIDTH // 2 - 252, HEIGHT // 2 - 22))
            screen.blit(game_over_text, (WIDTH // 2 - 250, HEIGHT // 2 - 20))

        # 5) Actualizar pantalla y controlar FPS
        pygame.display.flip()
        clock.tick(FPS)

    # Cuando termine el bucle, salimos de Pygame
    pygame.quit()
    sys.exit(0)

if __name__ == "__main__":
    main()