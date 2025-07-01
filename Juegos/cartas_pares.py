import pygame
import random
import sys # Necesario para sys.exit()

# Inicializar Pygame
pygame.init()

# --- Constantes del Juego ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CARD_SIZE_W = 100  # Ancho de la tarjeta
CARD_SIZE_H = 120  # Alto de la tarjeta
GAP_SIZE = 15      # Espacio entre tarjetas
ROWS = 4           # Número de filas
COLS = 4           # Número de columnas
NUM_CARDS = ROWS * COLS

# Asegurarse de que el número de tarjetas sea par
if NUM_CARDS % 2 != 0:
    print("Error: El número total de tarjetas debe ser par.")
    pygame.quit()
    sys.exit()

NUM_PAIRS = NUM_CARDS // 2

# Colores (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200) # Color para el texto
CARD_HIDDEN_COLOR = (60, 100, 200)  # Azul para tarjetas ocultas
CARD_REVEALED_COLOR = (220, 220, 220) # Gris claro para tarjetas reveladas
CARD_MATCHED_COLOR = (144, 238, 144) # Verde claro para pares encontrados
BACKGROUND_COLOR = (40, 40, 60) # Fondo oscuro

# Fuente para el texto en las tarjetas y mensajes
try:
    FONT_SIZE_CARD = 40
    FONT_CARD = pygame.font.Font(None, FONT_SIZE_CARD) # Fuente por defecto, tamaño 40
    FONT_SIZE_MESSAGE = 50
    FONT_MESSAGE = pygame.font.Font(None, FONT_SIZE_MESSAGE)
except pygame.error as e:
    print(f"Error al cargar la fuente: {e}. Usando fuente de sistema por defecto.")
    # Fallback si la fuente no se carga (poco común con None)
    FONT_CARD = pygame.font.SysFont("arial", FONT_SIZE_CARD)
    FONT_MESSAGE = pygame.font.SysFont("arial", FONT_SIZE_MESSAGE)


# --- Configuración de la Pantalla ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Juego de Memoria - Encuentra los Pares")

# --- Funciones Auxiliares ---
def generate_cards():
    """Genera la lista de figuras y las baraja."""
    symbols = []
    # Usaremos letras como "figuras"
    # Genera NUM_PAIRS de símbolos únicos (A, B, C, ...)
    for i in range(NUM_PAIRS):
        symbols.append(chr(ord('A') + i)) # chr(65) = 'A', chr(66) = 'B', etc.

    # Duplica los símbolos para tener pares y los baraja
    card_symbols = symbols * 2
    random.shuffle(card_symbols)
    return card_symbols

def create_board(card_symbols):
    """Crea el tablero con las tarjetas, sus posiciones y estados."""
    board = []
    # Calcular márgenes para centrar el tablero
    total_grid_width = COLS * CARD_SIZE_W + (COLS - 1) * GAP_SIZE
    total_grid_height = ROWS * CARD_SIZE_H + (ROWS - 1) * GAP_SIZE
    margin_x = (SCREEN_WIDTH - total_grid_width) // 2
    margin_y = (SCREEN_HEIGHT - total_grid_height) // 2

    if margin_x < 0 or margin_y < 0:
        print("Advertencia: El tablero es demasiado grande para la pantalla. Ajusta el tamaño de las tarjetas, el espacio o el número de filas/columnas.")
        # Podrías ajustar dinámicamente aquí o simplemente continuar

    for row in range(ROWS):
        for col in range(COLS):
            index = row * COLS + col
            if index < len(card_symbols): # Asegurarse de no exceder los símbolos disponibles
                symbol = card_symbols[index]
                # Posición de la tarjeta
                x = margin_x + col * (CARD_SIZE_W + GAP_SIZE)
                y = margin_y + row * (CARD_SIZE_H + GAP_SIZE)
                
                card_rect = pygame.Rect(x, y, CARD_SIZE_W, CARD_SIZE_H)
                
                # Diccionario para cada tarjeta
                card_info = {
                    'symbol': symbol,
                    'rect': card_rect,
                    'revealed': False, # Inicialmente oculta
                    'matched': False,  # Inicialmente no emparejada
                    'id': index        # Un identificador único para la tarjeta en el tablero
                }
                board.append(card_info)
    return board

def draw_card(surface, card_info):
    """Dibuja una tarjeta individual."""
    rect = card_info['rect']
    
    if card_info['matched']:
        pygame.draw.rect(surface, CARD_MATCHED_COLOR, rect, border_radius=10)
        # Dibuja el símbolo
        symbol_surface = FONT_CARD.render(card_info['symbol'], True, BLACK)
        symbol_rect = symbol_surface.get_rect(center=rect.center)
        surface.blit(symbol_surface, symbol_rect)
    elif card_info['revealed']:
        pygame.draw.rect(surface, CARD_REVEALED_COLOR, rect, border_radius=10)
        # Dibuja el símbolo
        symbol_surface = FONT_CARD.render(card_info['symbol'], True, BLACK)
        symbol_rect = symbol_surface.get_rect(center=rect.center)
        surface.blit(symbol_surface, symbol_rect)
    else: # Oculta
        pygame.draw.rect(surface, CARD_HIDDEN_COLOR, rect, border_radius=10)
        # Podrías dibujar un patrón o "?" en la tarjeta oculta si quieres
        # question_mark = FONT_CARD.render("?", True, WHITE)
        # qm_rect = question_mark.get_rect(center=rect.center)
        # surface.blit(question_mark, qm_rect)

def draw_board(surface, board):
    """Dibuja todas las tarjetas en el tablero."""
    for card_info in board:
        draw_card(surface, card_info)

def draw_message(surface, text, duration=0):
    """Muestra un mensaje en el centro de la pantalla."""
    message_surface = FONT_MESSAGE.render(text, True, WHITE, BACKGROUND_COLOR) # Fondo para mejor legibilidad
    message_rect = message_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    surface.blit(message_surface, message_rect)
    pygame.display.flip() # Actualiza la pantalla para mostrar el mensaje
    if duration > 0:
        pygame.time.wait(duration) # Espera si se especifica una duración

# --- Inicialización del Juego ---
card_symbols = generate_cards()
board = create_board(card_symbols)

revealed_cards_indices = [] # Lista para guardar los índices de las tarjetas reveladas temporalmente
matched_pairs_count = 0
game_active = True # Para controlar el flujo principal del juego
game_won = False
first_click_time = None # Para el temporizador de volteo si no son par
DELAY_BEFORE_HIDE = 750 # Milisegundos para mostrar las tarjetas antes de ocultarlas si no son par

# --- Bucle Principal del Juego ---
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN and game_active and not game_won:
            mouse_pos = pygame.mouse.get_pos()
            
            # Solo procesar clic si hay menos de 2 tarjetas reveladas (o si estamos esperando para ocultar)
            if len(revealed_cards_indices) < 2:
                for i, card in enumerate(board):
                    if card['rect'].collidepoint(mouse_pos) and not card['revealed'] and not card['matched']:
                        card['revealed'] = True
                        revealed_cards_indices.append(i)
                        if len(revealed_cards_indices) == 1:
                            first_click_time = None # Resetea el tiempo de espera si es la primera de un nuevo par
                        break # Solo una tarjeta por clic

    # --- Lógica del Juego ---
    if game_active and not game_won:
        if len(revealed_cards_indices) == 2:
            # Dos tarjetas han sido reveladas, verificar si son un par
            card1_index = revealed_cards_indices[0]
            card2_index = revealed_cards_indices[1]
            
            card1 = board[card1_index]
            card2 = board[card2_index]

            if card1['symbol'] == card2['symbol']:
                # ¡Es un par!
                card1['matched'] = True
                card2['matched'] = True
                matched_pairs_count += 1
                revealed_cards_indices = [] # Limpiar para el siguiente par
                first_click_time = None

                if matched_pairs_count == NUM_PAIRS:
                    game_won = True # Todas las parejas encontradas
            else:
                # No es un par, esperar un poco y luego ocultarlas
                if first_click_time is None:
                    first_click_time = pygame.time.get_ticks() # Marca el tiempo actual

                if pygame.time.get_ticks() - first_click_time > DELAY_BEFORE_HIDE:
                    card1['revealed'] = False
                    card2['revealed'] = False
                    revealed_cards_indices = []
                    first_click_time = None
    
    # --- Dibujado ---
    screen.fill(BACKGROUND_COLOR) # Limpiar la pantalla
    draw_board(screen, board)

    if game_won:
        game_active = False # Detener la lógica principal del juego
        # Mostrar mensaje de victoria
        win_text_surface = FONT_MESSAGE.render("¡Felicidades, Ganaste!", True, CARD_MATCHED_COLOR)
        win_text_rect = win_text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        
        # Pequeño fondo para el mensaje de victoria
        padding = 20
        bg_rect = pygame.Rect(win_text_rect.left - padding, win_text_rect.top - padding,
                              win_text_rect.width + 2 * padding, win_text_rect.height + 2 * padding)
        pygame.draw.rect(screen, BLACK, bg_rect, border_radius=15)
        pygame.draw.rect(screen, GRAY, bg_rect, width=3, border_radius=15) # Borde
        screen.blit(win_text_surface, win_text_rect)

        # Opción de reiniciar o salir
        restart_text = FONT_CARD.render("Presiona 'R' para reiniciar o 'Q' para salir", True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        screen.blit(restart_text, restart_rect)

        # Manejar reinicio o salida post-victoria
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            # Reiniciar el juego
            card_symbols = generate_cards()
            board = create_board(card_symbols)
            revealed_cards_indices = []
            matched_pairs_count = 0
            game_active = True
            game_won = False
            first_click_time = None
        elif keys[pygame.K_q]:
            running = False


    pygame.display.flip() # Actualizar la pantalla completa
    clock.tick(30) # Limitar a 30 FPS

# --- Salir de Pygame ---
pygame.quit()
sys.exit()
