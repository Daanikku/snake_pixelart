"""Configuración global y rutas del juego.

Extraído de `SnakeF.py` (sección 1: CONFIGURACIÓN Y CONSTANTES).
Todos los valores son idénticos a los originales; solo se añaden
constantes para valores mágicos y rutas absolutas (independientes
del directorio de trabajo).
"""
from pathlib import Path
from typing import Literal

# =================================================================
# Resolución y tablero
# =================================================================
WIDTH, HEIGHT = 1280, 720
CELL = 40                         # Tamaño de cada cuadro de la cuadrícula
BORDER = 60                       # Margen para elementos de interfaz (HUD)

# Cálculo de área de juego (asegura que quepan celdas completas)
PLAY_WIDTH, PLAY_HEIGHT = WIDTH - 2 * BORDER, HEIGHT - 2 * BORDER
GRID_W, GRID_H = PLAY_WIDTH // CELL, PLAY_HEIGHT // CELL
REAL_PLAY_WIDTH, REAL_PLAY_HEIGHT = GRID_W * CELL, GRID_H * CELL
OFFSET_X, OFFSET_Y = (WIDTH - REAL_PLAY_WIDTH) // 2, (HEIGHT - REAL_PLAY_HEIGHT) // 2

# =================================================================
# Ritmo del juego
# =================================================================
FPS = 60                          # Tasa de refresco visual
MOVE_DELAY = 120                  # Velocidad base (ms entre movimientos)

# =================================================================
# Efectos (power-ups)
# =================================================================
FAST_DELAY = 60                   # ms entre movimientos con speed_up
SLOW_DELAY = 200                  # ms entre movimientos con slow
SPEED_EFFECT_DURATION = 5000      # Duración en ms de speed_up / slow
GROW_EFFECT_DURATION = 3000       # Duración en ms de grow

# =================================================================
# Reglas de juego
# =================================================================
MIN_SNAKE_LENGTH = 3              # Longitud mínima de la serpiente
TOP_SCORES = 5                    # Tamaño del ranking persistido
MAX_NAME_LEN = 10                 # Longitud máxima del nombre

# =================================================================
# Rutas (resueltas desde la ubicación del paquete)
# =================================================================
BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = BASE_DIR / "assets"
BACKGROUND_DIR = ASSETS_DIR / "background"
SNAKE_DIR = ASSETS_DIR / "snake"
FOOD_DIR = ASSETS_DIR / "food"
SOUND_DIR = ASSETS_DIR / "sound"
FONTS_DIR = ASSETS_DIR / "fonts"
SCORE_FILE = BASE_DIR / "ranking.json"

# =================================================================
# Tipos
# =================================================================
EffectName = Literal["Crecimiento", "Velocidad", "Lentitud"]
GameState = Literal["menu", "game", "config", "death", "name_input"]