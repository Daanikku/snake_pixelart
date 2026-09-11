"""Vista: encapsula todo el renderizado en pantalla."""
import logging

import pygame

from snake_game import config

logger = logging.getLogger(__name__)


class View:
    """Encapsula toda la lógica de dibujo en pantalla."""

    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.font = self._load_font()
        self._init_assets()

    def _load_font(self) -> pygame.font.Font:
        """Carga la fuente empaquetada; si falla, usa una fuente del sistema."""
        font_path = config.FONTS_DIR / "arcade.ttf"
        try:
            return pygame.font.Font(str(font_path), 24)
        except Exception as e:
            logger.warning("Fuente %s no disponible (%s); usando SysFont.", font_path, e)
            return pygame.font.SysFont("ArcadeClassic", 24)

    def _init_assets(self) -> None:
        """Carga y escala imágenes. Usa fallbacks si no existen."""
        # Fondos
        self.bg_menu = self._load_img(config.BACKGROUND_DIR / "bg_menu.png", (config.WIDTH, config.HEIGHT))
        self.bg_config = self._load_img(config.BACKGROUND_DIR / "bg_config.png", (config.WIDTH, config.HEIGHT))
        self.bg_death = self._load_img(config.BACKGROUND_DIR / "bg_death.png", (config.WIDTH, config.HEIGHT))
        self.bg_name_input = self._load_img(config.BACKGROUND_DIR / "bg_name_input.png", (config.WIDTH, config.HEIGHT))

        # Sprites Cabeza (según dirección)
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        paths = ["head_right", "head_left", "head_down", "head_up"]
        self.heads = {
            d: self._load_img(config.SNAKE_DIR / f"{p}.png", (config.CELL, config.CELL))
            for d, p in zip(directions, paths)
        }

        # Cuerpo y Comida
        self.body_dark = self._load_img(config.SNAKE_DIR / "body_dark.png", (config.CELL, config.CELL))
        self.body_light = self._load_img(config.SNAKE_DIR / "body_light.png", (config.CELL, config.CELL))

        food_types = ["normal", "speed_up", "slow", "grow", "shrink", "bonus"]
        self.food_imgs = {
            t: self._load_img(config.FOOD_DIR / f"{t}.png", (config.CELL, config.CELL))
            for t in food_types
        }

    def _load_img(self, path, size) -> pygame.Surface:
        try:
            img = pygame.image.load(str(path)).convert_alpha()
            return pygame.transform.scale(img, size)
        except Exception as e:
            # Crea una superficie de color sólido si falla la carga
            logger.warning("Imagen %s no disponible (%s); usando fallback.", path, e)
            surf = pygame.Surface(size)
            surf.fill((100, 100, 100))
            return surf

    def draw_game(self, snake, food, score, effect, effect_time) -> None:
        """Dibuja el estado activo del juego."""
        self.screen.fill((40, 30, 20))  # Bordes/HUD

        # Dibujar Tablero (Grid de dos colores)
        for y in range(config.GRID_H):
            for x in range(config.GRID_W):
                rect = (config.OFFSET_X + x * config.CELL, config.OFFSET_Y + y * config.CELL, config.CELL, config.CELL)
                color = (240, 180, 70) if (x + y) % 2 == 0 else (230, 160, 60)
                pygame.draw.rect(self.screen, color, rect)

        # Dibujar Serpiente
        for i, pos in enumerate(snake.body):
            px, py = config.OFFSET_X + pos[0] * config.CELL, config.OFFSET_Y + pos[1] * config.CELL
            if i == 0:
                self.screen.blit(self.heads[snake.direction], (px, py))
            else:
                sprite = self.body_dark if i % 2 == 0 else self.body_light
                self.screen.blit(sprite, (px, py))

        # Dibujar Comida
        self.screen.blit(
            self.food_imgs[food.type],
            (config.OFFSET_X + food.pos[0] * config.CELL, config.OFFSET_Y + food.pos[1] * config.CELL),
        )

        # HUD
        self._render_text(f"SCORE: {score}", 30, 20)
        if effect:
            self._render_text(f"EFFECT: {effect.upper()} ({effect_time // 1000}s)", 30, 55, (255, 50, 50))

    def _render_text(self, txt, x, y, color=(255, 203, 11)) -> None:
        img = self.font.render(txt, True, color)
        self.screen.blit(img, (x, y))

    # --- Métodos de Menú ---
    def draw_menu(self, scores) -> None:
        self.screen.blit(self.bg_menu, (0, 0))
        y_offset = 465
        for s in scores:
            y_offset += 30
            self._render_text(f"{s['name'][:10]:<12} {s['score']:>5}", 88, y_offset)

    def draw_config(self, sound_enabled) -> None:
        self.screen.blit(self.bg_config, (0, 0))
        status = "ON" if sound_enabled else "OFF"
        self._render_text(status, 696, 275)

    def draw_death(self) -> None:
        self.screen.blit(self.bg_death, (0, 0))

    def draw_name_input(self, name, score) -> None:
        self.screen.blit(self.bg_name_input, (0, 0))
        self._render_text(f"{score}", 580, 300, (255, 255, 255))
        self._render_text(name + "_", 600, 350, (255, 203, 11))